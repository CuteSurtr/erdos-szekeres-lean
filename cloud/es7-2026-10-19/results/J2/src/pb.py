#!/usr/bin/env python3
"""PatternBoost-style loop for task J2 (33 points, no convex 7-gon).

Model: small GPT (causal transformer) over the multi-scale token encoding of
enc.py.  Loop per generation: sample NS sequences (BOS_33, grammar-masked
logits), decode to integer coordinates, run ls33 (exact annealing on the number
of convex 7-gons, ties broken by fewer convex 6-gons), add results to a pool
deduplicated by order type, retrain (fine-tune) on the best pool entries mixed
with the 32-point training sets, repeat.

v2 (env PREFIX=1): each sample keeps a random prefix of a pool set's encoding
(GMIN..31 of its 32 gaps, default 24; the pool set is re-encoded with a random rotation) and
the model completes the suffix; FRAC_UNCOND of samples are unconditional.
MODEL=unigram replaces the transformer by a position-wise unigram model
(token frequencies per position, re-estimated each generation from the same
training mix): the no-context ablation of the same loop.
INIT=path loads transformer weights (skips nothing else).

usage: pb.py OUTDIR HOURS NPROC
"""
import os, sys, json, time, random, glob, math
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enc, common

OUT, HOURS, NPROC = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
NS = int(os.environ.get('NS', 1000))          # samples per generation
ITERS = int(os.environ.get('ITERS', 800))      # ls33 iterations per sample
POOL = int(os.environ.get('POOL', 2000))       # best 33-point sets kept for training
STEPS0 = int(os.environ.get('STEPS0', 3000))   # initial training steps
STEPS = int(os.environ.get('STEPS', 600))      # fine-tune steps per generation
PREFIX = int(os.environ.get('PREFIX', 0))
FRAC_UNCOND = float(os.environ.get('FRAC_UNCOND', 0.2))
MODEL = os.environ.get('MODEL', 'gpt')
GMIN = int(os.environ.get('GMIN', 24))         # min gaps kept from the parent
INIT = os.environ.get('INIT', '')
torch.set_num_threads(NPROC)
torch.manual_seed(0)
rng = random.Random(0)
IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../inputs')
os.makedirs(OUT, exist_ok=True)
T_START = time.time()


class GPT(nn.Module):
    def __init__(self, V=enc.VOCAB, L=enc.SEQ, d=128, nl=4, nh=4):
        super().__init__()
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(L, d)
        layer = nn.TransformerEncoderLayer(d, nh, 4 * d, dropout=0.0, batch_first=True, norm_first=True)
        self.tr = nn.TransformerEncoder(layer, nl)
        self.ln = nn.LayerNorm(d)
        self.head = nn.Linear(d, V)
        self.register_buffer('mask', torch.triu(torch.full((L, L), float('-inf')), 1))

    def forward(self, x):
        T = x.shape[1]
        h = self.tok(x) + self.pos(torch.arange(T))[None]
        h = self.tr(h, mask=self.mask[:T, :T], is_causal=True)
        return self.head(self.ln(h))


# grammar mask: allowed next tokens at each position 1..SEQ-1
GMASK = torch.full((enc.SEQ, enc.VOCAB), float('-inf'))
for p in range(1, enc.SEQ):
    lo, hi = enc.RANGES[(p - 1) % 4]
    GMASK[p, lo:hi] = 0


def batchify(seqs):
    L = max(len(s) for s in seqs)
    x = torch.full((len(seqs), L), 0, dtype=torch.long)
    m = torch.zeros((len(seqs), L), dtype=torch.bool)
    for i, s in enumerate(seqs):
        x[i, :len(s)] = torch.tensor(s)
        m[i, :len(s)] = True
    return x, m


def train(model, opt, sets32, sets33, steps, frac33=0.7, bs=64):
    model.train()
    tot = 0.0
    for st in range(steps):
        seqs = []
        for _ in range(bs):
            P = rng.choice(sets33) if (rng.random() < frac33 or not sets32) else rng.choice(sets32)
            seqs.append(enc.encode(P, rng))
        x, m = batchify(seqs)
        logits = model(x[:, :-1]) + GMASK[1:x.shape[1]][None]
        tgt = x[:, 1:].masked_fill(~m[:, 1:], -100)        # padding (32-point sets) ignored
        loss = F.cross_entropy(logits.reshape(-1, enc.VOCAB), tgt.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tot += loss.item()
    return tot / max(steps, 1)


@torch.no_grad()
def sample(model, n, temp=1.0, bs=250):
    model.eval()
    out = []
    for b0 in range(0, n, bs):
        k = min(bs, n - b0)
        x = torch.full((k, 1), enc.BOS[33], dtype=torch.long)
        for p in range(1, enc.SEQ):
            lg = model(x)[:, -1] / temp + GMASK[p][None]
            nxt = torch.multinomial(F.softmax(lg, -1), 1)
            x = torch.cat([x, nxt], 1)
        out += x.tolist()
    return out


class Unigram:
    def __init__(self):
        self.lp = None

    def fit(self, sets32, sets33, n=20000, frac33=0.7):
        cnt = torch.ones((enc.SEQ, enc.VOCAB))          # add-one smoothing
        for _ in range(n):
            P = rng.choice(sets33) if (rng.random() < frac33 or not sets32) else rng.choice(sets32)
            t = enc.encode(P, rng)
            cnt[torch.arange(len(t)), torch.tensor(t)] += 1
        self.lp = torch.log(cnt / cnt.sum(1, keepdim=True))

    def __call__(self, x):
        return self.lp[:x.shape[1]][None].expand(x.shape[0], -1, -1)

    def eval(self):
        pass


@torch.no_grad()
def sample_cond(model, prefixes, temp=1.0):
    """complete equal-length prefixes to full 33-point sequences"""
    model.eval()
    x = torch.tensor(prefixes, dtype=torch.long)
    for p in range(x.shape[1], enc.SEQ):
        lg = model(x)[:, -1] / temp + GMASK[p][None]
        nxt = torch.multinomial(F.softmax(lg, -1), 1)
        x = torch.cat([x, nxt], 1)
    return x.tolist()


def gen_samples(model, pool_sets):
    if not PREFIX:
        return sample(model, NS)
    nu = int(NS * FRAC_UNCOND)
    out = sample(model, nu) if nu else []
    bs = 50
    for b0 in range(nu, NS, bs):
        k = min(bs, NS - b0)
        g = rng.randint(GMIN, 31)                      # gaps kept from the parent
        pre = [enc.encode(rng.choice(pool_sets), rng)[:1 + 4 * g] for _ in range(k)]
        out += sample_cond(model, pre)
    return out


def main():
    sets32 = []
    for f in sorted(glob.glob(IN + '/distinct_K7*.txt')):
        sets32 += enc.load_sets(f)
    seeds33 = []
    for f in sorted(glob.glob(IN + '/nearfull_p2*.txt')):
        seeds33 += enc.load_sets(f)
    print('train data: %d 32-point, %d 33-point' % (len(sets32), len(seeds33)), flush=True)
    seed_canon = set(common.canon(seeds33))
    pool = {}                                   # canon -> (E7, c6, P)
    seedc6 = {}
    sres = common.run_ls(seeds33, 0, NPROC, seed=0)      # exact (E7, c6) of the seeds
    for c, r in zip(common.canon([r[3] for r in sres]), sres):
        seedc6[c] = r[2]
    for c, P in zip(common.canon(seeds33), seeds33):
        pool[c] = (1, seedc6.get(c, 10 ** 9), P)
    if MODEL == 'unigram':
        model, opt = Unigram(), None
    else:
        model = GPT()
        if INIT:
            model.load_state_dict(torch.load(INIT))
        opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
        print('params', sum(p.numel() for p in model.parameters()), flush=True)
    log = open(os.path.join(OUT, 'generations.jsonl'), 'a')
    timeline = open(os.path.join(OUT, 'timeline.jsonl'), 'a')
    best_ever = None
    gen = 0
    while time.time() - T_START < HOURS * 3600:
        t0 = time.time()
        top = sorted(pool.values(), key=lambda v: (v[0], v[1]))[:POOL]
        if MODEL == 'unigram':
            model.fit(sets32, [v[2] for v in top])
            loss = float('nan')
        else:
            loss = train(model, opt, sets32, [v[2] for v in top], STEPS0 if (gen == 0 and not INIT) else STEPS)
        t1 = time.time()
        seqs = gen_samples(model, [v[2] for v in top])
        dec = [enc.decode(s, rng) for s in seqs]
        dec = [P for P in dec if P is not None]
        t2 = time.time()
        res = common.run_ls(dec, ITERS, NPROC, seed=gen + 1)
        t3 = time.time()
        E0 = np.array([r[0] for r in res])
        E = np.array([r[1] for r in res])
        good = [r for r in res if r[1] <= 1]
        cs = common.canon([r[3] for r in good])
        newc = 0
        for c, r in zip(cs, good):
            if c not in seed_canon:
                newc += 1
            if c not in pool or (r[1], r[2]) < pool[c][:2]:
                pool[c] = (r[1], r[2], r[3])
        zeros = [r for r in res if r[1] == 0]
        for r in zeros:
            with open(os.path.join(OUT, 'ZERO_CANDIDATES.txt'), 'a') as f:
                f.write(common.fmt_set(r[3]) + '\n')
        b = min(res, key=lambda r: (r[1], r[2]))
        if best_ever is None or (b[1], b[2]) < best_ever[:2]:
            best_ever = (b[1], b[2], b[3])
            with open(os.path.join(OUT, 'best.txt'), 'w') as f:
                f.write('# E7=%d c6=%d gen=%d\n' % (b[1], b[2], gen) + '\n'.join('%d %d' % p for p in b[3]) + '\n')
        c6good = sorted(r[2] for r in good)
        rec = dict(gen=gen, wall=round(time.time() - T_START, 1), train_s=round(t1 - t0, 1),
                   sample_s=round(t2 - t1, 1), ls_s=round(t3 - t2, 1), loss=round(loss, 4), n=len(res),
                   decoded_E7_min=int(E0.min()), decoded_E7_med=float(np.median(E0)),
                   decoded_le1=int((E0 <= 1).sum()),
                   E7_min=int(E.min()), E7_q10=float(np.percentile(E, 10)), E7_med=float(np.median(E)),
                   E7_hist={str(k): int((E == k).sum()) for k in range(0, 6)},
                   E7_gt5=int((E > 5).sum()),
                   n_le1=len(good), distinct_ot_le1=len(set(cs)), new_ot_le1_vs_seeds=len(set(cs) - seed_canon),
                   c6_min_le1=c6good[0] if c6good else None,
                   c6_med_le1=c6good[len(c6good) // 2] if c6good else None,
                   pool=len(pool), pool_new_vs_seeds=len(set(pool) - seed_canon),
                   pool_top_c6=sorted(v[1] for v in pool.values())[:3], best_ever=[best_ever[0], best_ever[1]],
                   cpu_self=round(common.self_cpu(), 1), cpu_children=round(common.child_cpu(), 1))
        log.write(json.dumps(rec) + '\n'); log.flush()
        timeline.write(json.dumps(dict(cpu=rec['cpu_self'] + rec['cpu_children'], E7_min_so_far=best_ever[0],
                                       pool_new=len(set(pool) - seed_canon))) + '\n'); timeline.flush()
        print(json.dumps(rec), flush=True)
        if MODEL != 'unigram':
            torch.save(model.state_dict(), os.path.join(OUT, 'model.pt'))
        with open(os.path.join(OUT, 'pool_top.txt'), 'w') as f:
            for v in sorted(pool.values(), key=lambda v: (v[0], v[1]))[:200]:
                f.write('%d %d %s\n' % (v[0], v[1], common.fmt_set(v[2])))
        gen += 1


if __name__ == '__main__':
    main()
