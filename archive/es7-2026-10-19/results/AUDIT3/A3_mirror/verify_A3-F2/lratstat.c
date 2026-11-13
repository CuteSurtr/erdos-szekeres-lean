// lratstat NCNF: read a text LRAT proof on stdin (streamed) and recompute, with the counting rules of
// drat-trim lrat-check.c (2e3b2dc), the three statistics it prints on its last line:
//   added_clauses   = NCNF (every parsed CNF clause goes through addClause) + number of addition lines
//   deleted_clauses = number of deletion ids that were live when deleted (others only print a WARNING)
//   max_live        = maximum of the live count over the run (CNF clauses live from the start)
// Also prints bytes, SHA-256, last id, whether addition ids are contiguous, and the last line's shape.
// The live set is a bitset over clause ids (one bit per id), so memory stays small.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <CommonCrypto/CommonDigest.h>

#define BUF (1 << 24)
static uint8_t *live; static int64_t cap_bits;

static void ensure(int64_t id) {
  if (id < cap_bits) return;
  int64_t nc = cap_bits; while (nc <= id) nc *= 2;
  live = realloc(live, (size_t)(nc / 8 + 1));
  memset(live + cap_bits / 8 + 1, 0, (size_t)(nc / 8 - cap_bits / 8));
  cap_bits = nc; }
static inline int getb(int64_t i) { return (live[i >> 3] >> (i & 7)) & 1; }
static inline void setb(int64_t i) { live[i >> 3] |= (uint8_t)(1u << (i & 7)); }
static inline void clrb(int64_t i) { live[i >> 3] &= (uint8_t)~(1u << (i & 7)); }

enum { START, AFTER_ID, DEL, LITS, HINTS, DONE };

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: lratstat NCNF < proof.lrat\n"); return 2; }
  int64_t ncnf = atoll(argv[1]);
  cap_bits = 1LL << 26; live = calloc((size_t)(cap_bits / 8 + 1), 1);
  ensure(ncnf + 1);
  for (int64_t i = 1; i <= ncnf; i++) setb(i);
  int64_t live_cnt = ncnf, max_live = ncnf, added = ncnf, deleted = 0;
  int64_t n_add = 0, n_del_lines = 0, n_del_ids = 0, warn_del = 0, readd_live = 0, n_empty = 0;
  int64_t last_add_id = ncnf, noncontig = 0, nonincr = 0, first_add_id = -1, empty_id = -1, lines = 0;
  int64_t cur_id = 0, lits_len = 0, hints_len = 0, bad = 0, last_line_id = 0, last_line_lits = -1, last_line_hints = -1;
  int last_line_type = 0;
  unsigned char *buf = malloc(BUF);
  CC_SHA256_CTX sha; CC_SHA256_Init(&sha);
  uint64_t bytes = 0; size_t n;
  int st = START; int64_t num = 0; int neg = 0, innum = 0;
  while ((n = fread(buf, 1, BUF, stdin)) > 0) {
    CC_SHA256_Update(&sha, buf, (CC_LONG)n); bytes += n;
    for (size_t i = 0; i < n; i++) {
      unsigned char ch = buf[i];
      if (ch >= '0' && ch <= '9') { num = num * 10 + (ch - '0'); innum = 1; continue; }
      if (ch == '-') { if (innum) bad++; neg = 1; continue; }
      if (innum) {   // a complete integer token
        int64_t v = neg ? -num : num; num = 0; neg = 0; innum = 0;
        switch (st) {
          case START: cur_id = v; st = AFTER_ID; break;
          case AFTER_ID: if (v == 0) { lits_len = 0; hints_len = 0; st = HINTS; } else { lits_len = 1; hints_len = 0; st = LITS; } break;
          case LITS: if (v == 0) st = HINTS; else lits_len++; break;
          case HINTS:
            if (v != 0) { hints_len++; break; }
            // end of an addition line
            n_add++; added++;
            if (first_add_id < 0) first_add_id = cur_id;
            if (cur_id != last_add_id + 1) noncontig++;
            if (cur_id <= last_add_id) nonincr++;
            last_add_id = cur_id;
            ensure(cur_id);
            if (getb(cur_id)) readd_live++;
            setb(cur_id); live_cnt++; if (live_cnt > max_live) max_live = live_cnt;
            if (lits_len == 0) { n_empty++; empty_id = cur_id; }
            last_line_type = 'a'; last_line_id = cur_id; last_line_lits = lits_len; last_line_hints = hints_len;
            st = DONE; break;
          case DEL:
            if (v == 0) { n_del_lines++; last_line_type = 'd'; last_line_id = cur_id; st = DONE; break; }
            n_del_ids++;
            if (v > 0 && v < cap_bits && getb(v)) { clrb(v); live_cnt--; deleted++; } else warn_del++;
            break;
          case DONE: bad++; break; }
        // fall through to handle the separator character itself
      } else if (neg) { bad++; neg = 0; }
      if (ch == 'd') { if (st == AFTER_ID) st = DEL; else bad++; continue; }
      if (ch == '\n') { lines++; if (st != DONE) bad++; st = START; continue; }
      if (ch == ' ' || ch == '\t' || ch == '\r') continue;
      bad++;
    }
  }
  if (innum || st != START) bad++;
  unsigned char md[CC_SHA256_DIGEST_LENGTH]; CC_SHA256_Final(md, &sha);
  printf("bytes: %llu\nsha256: ", (unsigned long long)bytes);
  for (int i = 0; i < CC_SHA256_DIGEST_LENGTH; i++) printf("%02x", md[i]);
  printf("\nlines: %lld\naddition_lines: %lld\ndeletion_lines: %lld\ndeletion_ids: %lld\n"
         "first_addition_id: %lld\nlast_addition_id: %lld\nnoncontiguous_addition_ids: %lld\nnonincreasing_addition_ids: %lld\n"
         "empty_clauses: %lld (last at id %lld)\nlast_line: type %c id %lld lits %lld hints %lld\n"
         "deletions_of_non_live_ids (lrat-check WARNING): %lld\nadditions_over_live_id: %lld\nparse_anomalies: %lld\n",
         (long long)lines, (long long)n_add, (long long)n_del_lines, (long long)n_del_ids,
         (long long)first_add_id, (long long)last_add_id, (long long)noncontig, (long long)nonincr,
         (long long)n_empty, (long long)empty_id, last_line_type ? last_line_type : '?', (long long)last_line_id,
         (long long)last_line_lits, (long long)last_line_hints, (long long)warn_del, (long long)readd_live, (long long)bad);
  printf("lrat-check-style: Added clauses = %lld.  Deleted clauses = %lld.  Max live clauses = %lld\n",
         (long long)added, (long long)deleted, (long long)max_live);
  printf("final_live: %lld\n", (long long)live_cnt);
  return 0;
}
