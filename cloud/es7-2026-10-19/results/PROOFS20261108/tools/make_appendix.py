#!/usr/bin/env python3
"""Generate appendix_map.tex (the statement map) from sections/<key>.map.tsv.

Usage: python3 tools/make_appendix.py   (run from the directory that holds proofs.tex)
Each map row is: label, kind, lean_name, file_line, note (tab separated, with a header row).
The maps are ASCII. In the notes, labels become references, identifiers and paths are set in typewriter type with
break points, and ASCII notation (<=, !=, ->, =>, Greek letter names, x^n, R_theta, a*b, a..b) becomes mathematics.
"""
import csv
import re
import sys

KEYS = ['fd', 'll', 'lg', 'oc', 'pc', 'ec', 'sr', 'ar', 'mm', 'mb', 'cb', 'sa']
KINDS = {'theorem': 'Thm.', 'lemma': 'Lem.', 'proposition': 'Prop.', 'corollary': 'Cor.',
         'fact': 'Fact', 'definition': 'Def.', 'remark': 'Rem.'}
FULL = {'theorem': 'Theorem', 'lemma': 'Lemma', 'proposition': 'Proposition', 'corollary': 'Corollary',
        'fact': 'Fact', 'definition': 'Definition', 'remark': 'Remark'}
PLURAL = {'Theorem': 'Theorems', 'Lemma': 'Lemmas', 'Proposition': 'Propositions', 'Corollary': 'Corollaries',
          'Fact': 'Facts', 'Definition': 'Definitions', 'Remark': 'Remarks', 'Section': 'Sections'}
NAME_WORDS = {w: n for n, p in PLURAL.items() for w in (n, p)}
ESC = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '$': r'\$', '&': r'\&', '%': r'\%', '#': r'\#',
       '_': r'\_', '^': r'\textasciicircum{}', '~': r'\textasciitilde{}', '<': r'\textless{}',
       '>': r'\textgreater{}', '|': r'\textbar{}'}
# An identifier or a path, possibly with a line list such as :29,35; with opening brackets before it and closing
# punctuation after it.
IDENT = re.compile(r"^([(\[]*)([A-Za-z0-9][A-Za-z0-9_.'/:+-]*[A-Za-z0-9_'](?:,\d+)*)([)\],;:.]*)$")
# A label of this document, possibly followed by part suffixes such as (a) or (b)(ii).
LABEL_TOK = re.compile(r'^([(\[]*)([a-z]{2}:[A-Za-z0-9:_-]*[A-Za-z0-9])((?:\([a-z0-9]+\))*)([)\],;:.]*)$')
LABEL_KEY = re.compile(r'^(%s):' % '|'.join(KEYS))
LABELS = {}
HEADS = {}

# ASCII notation. Greek letter names (not omega, which in the notes is the Lean tactic), function and relation words,
# and operators, longest first.
GREEK = ['epsilon', 'lambda', 'alpha', 'gamma', 'delta', 'theta', 'kappa', 'sigma', 'beta', 'iota', 'rho', 'tau',
         'phi', 'chi', 'psi', 'pi']
WORDS = {'exp': r'\exp', 'det': r'\det', 'card': r'\operatorname{card}', 'id': r'\mathrm{id}', 'ne': r'\ne',
         'notin': r'\notin'}
OPS = [('<->', r'\leftrightarrow'), ('<=', r'\le'), ('>=', r'\ge'), ('!=', r'\ne'), ('->', r'\to'),
       ('=>', r'\Rightarrow'), ('<', '<'), ('>', '>'), ('=', '='), ('+', '+'), ('-', '-'), ('/', '/'), ('*', '*'),
       ('^', '^'), ('_', '_'), ("'", "'"), ('(', '('), (')', ')'), (',', ','), ('|', '|'),
       ('~', '\\ ')]     # ~ marks a space kept between tokens (see join_math)
STRONG_OPS = {'<->', '<=', '>=', '!=', '->', '=>', '<', '>', '=', '^', '_', '*', '+'}


def esc(s):
    return ''.join(ESC.get(ch, ch) for ch in s)


def check_ascii(s, where):
    bad = sorted({ch for ch in s if ord(ch) > 126})
    if bad:
        sys.exit(f'non-ASCII characters {bad} in {where}; add a translation before generating')


def tt_break(core):
    """Typewriter text that may break after . / _ (never after the last character)."""
    out = []
    for i, ch in enumerate(core):
        out.append(ESC.get(ch, ch))
        if ch in './_' and i < len(core) - 1:
            out.append(r'\allowbreak{}')
    return r'\texttt{' + ''.join(out) + '}'


def lex_math(s):
    """Split s into math lexemes; return None if s contains anything that is not ASCII mathematics."""
    out = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        m = re.match(r'[A-Za-z]+', s[i:])
        if m:
            w = m.group(0)
            if w in GREEK or w in WORDS:
                out.append(('word', w))
            elif len(w) == 1:
                out.append(('letter', w))
            else:
                return None
            i += len(w)
            continue
        m = re.match(r'\d+', s[i:])
        if m:
            d = m.group(0)
            nxt = s[i + len(d):]
            letters = re.match(r'[A-Za-z]+', nxt)
            if letters and letters.group(0) not in GREEK:
                return None          # such as C2P5: a name, not mathematics
            out.append(('num', d))
            i += len(d)
            continue
        for op, _ in OPS:
            if s.startswith(op, i):
                out.append(('op', op))
                i += len(op)
                break
        else:
            return None
    return out


def math_of(lexemes):
    """LaTeX math (without dollars) for a list of lexemes."""
    res = []
    k = 0
    n = len(lexemes)

    def atom(j):
        kind, v = lexemes[j]
        if kind == 'word':
            return WORDS.get(v, '\\' + v)
        return v

    def operand_end(j):
        """Index after the operand that starts at j (a number followed by a Greek word counts as one operand)."""
        if j < n and lexemes[j][0] == 'num' and j + 1 < n and lexemes[j + 1][0] == 'word' \
                and lexemes[j + 1][1] in GREEK:
            return j + 2
        return j + 1

    while k < n:
        kind, v = lexemes[k]
        if kind == 'op' and v in ('^', '_') and k + 1 < n:
            if lexemes[k + 1] == ('op', '('):
                depth, j = 0, k + 1
                while j < n:
                    if lexemes[j] == ('op', '('):
                        depth += 1
                    elif lexemes[j] == ('op', ')'):
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                res.append(v + '{' + math_of(lexemes[k + 2:j]) + '}')
                k = j + 1
            else:
                j = operand_end(k + 1)
                res.append(v + '{' + ''.join(atom(t) for t in range(k + 1, j)) + '}')
                k = j
            continue
        if kind == 'op' and v == '*':
            left = lexemes[k - 1] if k > 0 else None
            right = lexemes[k + 1] if k + 1 < n else None
            if left and left[0] == 'num' and right and right[0] in ('letter', 'word'):
                res.append('')
            else:
                res.append(r'\cdot ')
            k += 1
            continue
        if kind == 'op':
            res.append(dict(OPS)[v])
            k += 1
            continue
        a = atom(k)
        # a control word must not run into a following letter
        if res and re.search(r'\\[A-Za-z]+$', res[-1]) and re.match(r'[A-Za-z]', a):
            res.append(' ')
        res.append(a)
        k += 1
    return ''.join(res)


def strength(tok):
    """'strong' if tok is ASCII mathematics with an operator, a Greek letter or a function word; 'weak' if it is
    ASCII mathematics without one (a letter, a number); None otherwise."""
    lx = lex_math(tok.rstrip(',;:.'))
    if lx is None or not lx:
        return None
    if any(k == 'word' for k, _ in lx) or any(k == 'op' and v in STRONG_OPS for k, v in lx):
        return 'strong'
    if re.fullmatch(r'\|[A-Za-z]\|', tok.strip('(),;:.')):
        return 'strong'
    return 'weak'


def split_punct(text):
    """Split a run of tokens into (pre, core, post): unmatched brackets at the ends and clause punctuation at the end
    stay outside the mathematics."""
    stack, unmatched = [], set()
    for k, ch in enumerate(text):
        if ch in '([':
            stack.append(k)
        elif ch in ')]':
            if stack:
                stack.pop()
            else:
                unmatched.add(k)
    unmatched |= set(stack)
    a = 0
    while a < len(text) and a in unmatched and text[a] in '([':
        a += 1
    b = len(text)
    while b > a and (text[b - 1] in ',;:.' or (b - 1 in unmatched and text[b - 1] in ')]')):
        b -= 1
    return text[:a], text[a:b], text[b:]


def join_math(toks):
    """Join tokens of ASCII mathematics. A space before an opening bracket that follows an operand is kept (as in
    "n = s*k+e (e <= 1"); other spaces are dropped, as in mathematics."""
    out = toks[0]
    for t in toks[1:]:
        if t[0] == '(' and re.match(r"[A-Za-z0-9')]", out[-1]):
            out += '~' + t
        else:
            out += ' ' + t
    return out


def label_ref(tok, prev, plural):
    """For a label token: (text, joined, plural), where joined means that the text is to be attached with ~ to the
    preceding name word (Theorem, Lemmas, ...), whose wording it may correct; or None for any other token."""
    lm = LABEL_TOK.match(tok)
    if not lm or lm.group(2) not in LABELS:
        return None
    pre, label, suffix, post = lm.groups()
    name = LABELS[label]
    tail = esc(suffix) + esc(post)
    prev_word = prev.lstrip('([') if prev is not None else None
    if not pre and prev_word in NAME_WORDS and name is not None:
        if NAME_WORDS[prev_word] != name:
            print(f'warning: a note calls {label} a {prev_word}; it labels a {name}', file=sys.stderr)
        return ('\\ref{%s}' % label + tail, True, prev_word in PLURAL.values())
    if plural and not pre and (prev in ('and', 'or') or (prev.endswith(',') and LABEL_TOK.match(prev))):
        return ('\\ref{%s}' % label + tail, False, True)
    ref = ('%s~\\ref{%s}' % (name, label)) if name else ('\\ref{%s}' % label)
    return (esc(pre) + ref + tail, False, False)


def text_tok(tok):
    """A token that is neither a label nor mathematics."""
    m = IDENT.match(tok)
    if m and ('_' in m.group(2) or '/' in m.group(2) or re.search(r'[a-z]\.[A-Za-z]', m.group(2))
              or re.search(r'[a-z][A-Z]', m.group(2))):
        pre, core, post = m.groups()
        if re.search(r'\w\.\.\w', core):        # a range of identifiers such as closedP1..closedP8
            core_tex = '--'.join(tt_break(part) for part in core.split('..'))
        else:
            core_tex = tt_break(core)
        return esc(pre) + core_tex + esc(post)
    if tok == '...':
        return r'\dots{}'
    out = esc(tok)
    out = re.sub(r'(?<=\w)\.\.(?=\w)', '--', out)            # a range such as certs0..certs126 or 2..6
    # a Greek letter name inside a word such as rotAbout(c,2pi/m)
    out = re.sub(r'(?<![A-Za-z])(%s)(?![A-Za-z])' % '|'.join(GREEK), lambda g: '$\\%s$' % g.group(1), out)
    return out


def note_tex(note):
    """Typeset a free-text note."""
    toks = note.split(' ')
    pieces = []          # (separator before, text)
    plural = False       # inside "Theorems A, B and C"
    i = 0
    while i < len(toks):
        tok = toks[i]
        prev = toks[i - 1] if i > 0 else None
        lr = label_ref(tok, prev, plural)
        if lr:
            text, joined, plural = lr
            if joined:
                word = prev.lstrip('([')
                name = LABELS[LABEL_TOK.match(tok).group(2)]
                fixed = PLURAL[name] if word in PLURAL.values() else name
                last = pieces[-1][1]
                pieces[-1] = (pieces[-1][0], last[:len(last) - len(word)] + fixed + '~' + text)
            else:
                pieces.append((' ', text))
            i += 1
            continue
        if plural and tok not in ('and', 'or'):
            plural = False
        lm = LABEL_TOK.match(tok)
        if lm and LABEL_KEY.match(lm.group(2)):
            sys.exit(f'note refers to an undefined label: {tok}')
        # a run of tokens of ASCII mathematics; a token that ends a clause (; : .) ends the run
        j = i
        kinds = []
        while j < len(toks) and not LABEL_TOK.match(toks[j]):
            st = strength(toks[j])
            if st is None:
                break
            if j > i and toks[j - 1].endswith(',') and st == 'weak':
                break                # after a comma, only an expression with an operator continues the run
            kinds.append(st)
            j += 1
            if re.search(r'[;:.]$', toks[j - 1]):
                break
        run = toks[i:j]
        if run and 'strong' in kinds:
            pre, core, post = split_punct(join_math(run))
            lx = lex_math(core) if core else None
            if lx:
                pieces.append((' ', esc(pre) + '$' + math_of(lx) + '$' + esc(post)))
            else:
                pieces.extend((' ', text_tok(t)) for t in run)
            i = j
            continue
        pieces.append((' ', text_tok(tok)))
        i += 1
    return ''.join((sep if n else '') + text for n, (sep, text) in enumerate(pieces))


def collect_labels():
    """Map every label defined in the section files to the name of what it labels, and keep statement heads."""
    env_re = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|fact|definition|remark)\}'
                        r'(\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\\label\{([^}]*)\}')
    for key in KEYS:
        with open(f'sections/{key}.tex') as fh:
            src = fh.read()
        for kind, head, label in env_re.findall(src):
            LABELS[label] = FULL[kind]
            HEADS[label] = head
        for label in re.findall(r'\\label\{([^}]*)\}', src):
            if label not in LABELS:
                if re.search(r':(sec|ssec|subsec)\b', label) or label.endswith(':sec'):
                    LABELS[label] = 'Section'
                else:
                    LABELS[label] = None


def split_list(s):
    return [x.strip() for x in re.split(r'[;,]\s+', s) if x.strip()]


def clean_note(n):
    """Drop the workflow phrase 'export label' and the items it empties."""
    n = re.sub(r'export label \((with [^;]*)\)', r'\1', n)
    n = re.sub(r'\(export label ', '(', n)
    n = re.sub(r'export label\s*', '', n)
    items = [x.strip() for x in n.split(';')]
    return '; '.join(x for x in items if x)


def lean_cell(label, kind, lean, fl):
    """Each declaration with its file and line below it, indented; or the tag of a row without a declaration."""
    names = [] if lean.strip() in ('-', '') else split_list(lean)
    files = [] if fl.strip() in ('-', '') else split_list(fl)
    if not names:
        head = HEADS.get(label, '')
        if 'written step' in head:
            tag = 'written step'
        elif kind != 'remark' and 'Mathlib' in head:
            tag = 'Mathlib'
        else:
            tag = '--'
        if not files:
            return tag
        names = [None] * len(files)
        tags = [tag] * len(files)
    else:
        tags = None
    if len(files) != len(names):
        return '\\newline '.join(['\\lean{%s}' % x for x in names] + ['\\dirn{%s}' % x for x in files])
    entries = []
    for k, (nm, fi) in enumerate(zip(names, files)):
        first = tags[k] if tags else '\\lean{%s}' % nm
        entries.append('\\hangindent=1em\\hangafter=1 %s\\newline\\dirn{%s}' % (first, fi))
    return '\\par '.join(entries)


def main():
    collect_labels()
    out = []
    out.append('% appendix_map.tex -- generated by tools/make_appendix.py from sections/*.map.tsv; do not edit by hand.\n')
    out.append('\\section{Statement map}\\label{app:map}\n\n')
    out.append('Each row lists a numbered statement of this document, the Lean declarations that it restates, each with\n'
               'its file and line at commit \\texttt{7e32ee259}, and a note. For a remark, the Lean column names the\n'
               'declarations that the remark discusses; a remark does not restate a Lean statement. A path that begins with\n'
               '\\dirn{ErdosSzekeres/}, \\dirn{docs/}, \\dirn{experiments/} or \\dirn{scripts/} is relative to the repository\n'
               'root; every other path is relative to \\dirn{cloud/es7-2026-10-19/results}. A statement introduced only for\n'
               'the written proofs is marked ``written step\'\', one that restates Mathlib definitions or facts is marked\n'
               '``Mathlib\'\', and a remark without a Lean declaration has a dash. Labelled remarks appear where a section\n'
               'lists them. The notes are those of the section maps.\n\n')
    out.append('{\\footnotesize\n')
    out.append('\\begin{longtable}{@{}>{\\raggedright\\arraybackslash}p{0.10\\linewidth}'
               '>{\\raggedright\\arraybackslash}p{0.49\\linewidth}'
               '>{\\raggedright\\arraybackslash}p{0.35\\linewidth}@{}}\n')
    head = '\\toprule\nStatement & Lean declaration; file and line & Note\\\\\n\\midrule\n'
    out.append(head + '\\endfirsthead\n' + head + '\\endhead\n\\bottomrule\n\\endlastfoot\n')
    total = 0
    for key in KEYS:
        with open(f'sections/{key}.map.tsv', newline='') as fh:
            rows = list(csv.reader(fh, delimiter='\t', quoting=csv.QUOTE_NONE))
        if rows[0] != ['label', 'kind', 'lean_name', 'file_line', 'note']:
            sys.exit(f'bad header in {key}.map.tsv: {rows[0]}')
        out.append('\\multicolumn{3}{@{}l}{\\normalsize\\textbf{Section~\\ref{%s:sec}}}\\\\[2pt]\n' % key)
        for r in rows[1:]:
            if len(r) != 5:
                sys.exit(f'{key}.map.tsv: row with {len(r)} fields: {r}')
            label, kind, lean, fl, note = r
            for fld in r:
                check_ascii(fld, f'{key}.map.tsv row {label}')
            if kind not in KINDS:
                sys.exit(f'{key}.map.tsv: unknown kind {kind!r} for {label}')
            if not label.startswith(key + ':'):
                sys.exit(f'{key}.map.tsv: label {label} lacks the prefix {key}:')
            if label not in LABELS:
                sys.exit(f'{key}.map.tsv: label {label} is not defined in sections/{key}.tex')
            stmt = '%s~\\ref{%s}' % (KINDS[kind], label)
            n = clean_note(note.strip())
            note_t = '' if n in ('-', '') else note_tex(n)
            out.append(f'{stmt} & {lean_cell(label, kind, lean, fl)} & {note_t}\\\\\n')
            total += 1
        out.append('\\addlinespace\n')
    out.append('\\end{longtable}}\n')
    with open('appendix_map.tex', 'w') as fh:
        fh.write(''.join(out))
    print(f'appendix_map.tex: {total} rows')


if __name__ == '__main__':
    main()
