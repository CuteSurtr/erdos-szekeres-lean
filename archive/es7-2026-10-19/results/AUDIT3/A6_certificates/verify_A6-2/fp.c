/* verify_A6-2: independent streaming fingerprint of a text LRAT proof or a DIMACS CNF read from stdin.
 * Written for this check (it does not reuse the auditor's lratcount.c). SHA-256 is computed in-process
 * (CommonCrypto), so "zstd -dc ARCHIVE | fp MODE" needs only two processes.
 *
 * usage: fp lrat INPUT_CLAUSES   (INPUT_CLAUSES = clause count of the CNF; used for the live-clause count)
 *        fp cnf
 * Output: key=value lines.
 *
 * LRAT text lines: addition "id lit* 0 hint* 0", deletion "id d id* 0".
 * LRAT counts: bytes, sha256, lines, additions, empty additions, first empty id, min/max addition id, number of
 * non-increasing addition ids, deletion lines, deleted ids, max live clauses (INPUT_CLAUSES + additions so far -
 * deleted ids so far, maximum over the run including the start), kind of the last line, malformed lines.
 * CNF counts: header V C, clauses (zero terminators outside comment lines), max |literal|, comment lines, and the
 * text of the first comment line (first 200 characters).
 */
#define COMMON_DIGEST_FOR_OPENSSL
#include <CommonCrypto/CommonDigest.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFSZ (1 << 24)
static unsigned char buf[BUFSZ];

int main(int argc, char **argv) {
  if (argc < 2 || (strcmp(argv[1], "lrat") && strcmp(argv[1], "cnf"))) {
    fprintf(stderr, "usage: fp lrat INPUT_CLAUSES | fp cnf\n");
    return 2;
  }
  const int lrat = !strcmp(argv[1], "lrat");
  const long long input_clauses = (lrat && argc > 2) ? atoll(argv[2]) : 0;

  CC_SHA256_CTX ctx;
  CC_SHA256_Init(&ctx);
  unsigned long long bytes = 0, lines = 0;

  /* token state */
  int in_tok = 0, tok_is_num = 1, neg = 0;
  long long num = 0;
  char word[8];
  int wlen = 0;

  /* line state */
  long long ntok = 0, line_id = 0, lits = 0, line_dels = 0;
  int comment = 0, del = 0, zeros = 0, bad = 0, header = 0;

  /* LRAT stats */
  unsigned long long additions = 0, empty_add = 0, del_lines = 0, deleted_ids = 0, comments = 0, malformed = 0,
                     nonincr = 0;
  long long first_empty = -1, min_add = -1, max_add = -1, prev_add = -1;
  long long live = input_clauses, max_live = input_clauses;
  const char *last = "none";

  /* CNF stats */
  long long hv = -1, hc = -1, clauses = 0, maxvar = 0;
  char fc[201];
  int fclen = 0, fcdone = 0;

  size_t n;
  while ((n = fread(buf, 1, BUFSZ, stdin)) > 0) {
    CC_SHA256_Update(&ctx, buf, (CC_LONG)n);
    bytes += n;
    for (size_t i = 0; i < n; i++) {
      const unsigned char ch = buf[i];
      const int sep = (ch == ' ' || ch == '\t' || ch == '\n' || ch == '\r');

      if (comment && ch != '\n') { /* inside a comment line */
        if (!fcdone && fclen < 200) fc[fclen++] = (char)ch;
        continue;
      }
      if (!sep) {
        if (!in_tok) {
          if (ntok == 0 && ch == 'c') { /* comment line */
            comment = 1;
            if (!fcdone) { fclen = 0; fc[fclen++] = (char)ch; }
            continue;
          }
          in_tok = 1; tok_is_num = 1; neg = 0; num = 0; wlen = 0;
          if (ch == '-') { neg = 1; continue; }
        }
        if (tok_is_num && ch >= '0' && ch <= '9') { num = num * 10 + (ch - '0'); continue; }
        tok_is_num = 0;
        if (wlen < 7) word[wlen++] = (char)ch;
        continue;
      }
      /* separator: close the current token */
      if (in_tok) {
        if (!tok_is_num) {
          word[wlen] = 0;
          if (lrat) {
            if (ntok == 1 && !strcmp(word, "d")) del = 1; else bad = 1;
          } else {
            if (ntok == 0 && !strcmp(word, "p")) header = 1;
            else if (!(header && ntok == 1 && !strcmp(word, "cnf"))) bad = 1;
          }
        } else {
          const long long v = neg ? -num : num;
          if (lrat) {
            if (ntok == 0) line_id = v;
            else if (del) {
              if (zeros == 0) { if (v == 0) zeros = 1; else { deleted_ids++; line_dels++; } }
              else bad = 1;
            } else {
              if (zeros == 0) { if (v == 0) zeros = 1; else lits++; }
              else if (zeros == 1) { if (v == 0) zeros = 2; }
              else bad = 1;
            }
          } else {
            if (header) { if (ntok == 2) hv = v; else if (ntok == 3) hc = v; else bad = 1; }
            else if (v == 0) clauses++;
            else { const long long a = v < 0 ? -v : v; if (a > maxvar) maxvar = a; }
          }
        }
        ntok++;
        in_tok = 0;
      }
      if (ch == '\n') {
        lines++;
        if (comment) {
          comments++; last = "comment";
          if (!fcdone) { fc[fclen] = 0; fcdone = 1; }
        } else if (lrat && ntok > 0) {
          if (del) {
            if (zeros != 1) bad = 1;
            del_lines++;
            live -= line_dels;
            last = "deletion";
          } else {
            if (zeros != 2) bad = 1;
            additions++;
            if (min_add < 0 || line_id < min_add) min_add = line_id;
            if (line_id > max_add) max_add = line_id;
            if (prev_add >= 0 && line_id <= prev_add) nonincr++;
            prev_add = line_id;
            live++;
            if (live > max_live) max_live = live;
            if (lits == 0) { empty_add++; if (first_empty < 0) first_empty = line_id; last = "empty_addition"; }
            else last = "addition";
          }
          if (bad) malformed++;
        } else if (!lrat && ntok > 0) {
          if (bad) malformed++;
        }
        ntok = 0; line_id = 0; lits = 0; line_dels = 0;
        comment = 0; del = 0; zeros = 0; bad = 0; header = 0;
      }
    }
  }
  if (in_tok || ntok > 0) fprintf(stderr, "warning: input does not end with a newline\n");

  unsigned char md[CC_SHA256_DIGEST_LENGTH];
  CC_SHA256_Final(md, &ctx);
  printf("bytes=%llu\nsha256=", bytes);
  for (int i = 0; i < CC_SHA256_DIGEST_LENGTH; i++) printf("%02x", md[i]);
  printf("\nlines=%llu\n", lines);
  if (lrat) {
    printf("additions=%llu\nempty_additions=%llu\nfirst_empty_id=%lld\nmin_add_id=%lld\nmax_add_id=%lld\n"
           "nonincreasing_add_ids=%llu\ndeletion_lines=%llu\ndeleted_ids=%llu\nmax_live=%lld\ncomment_lines=%llu\n"
           "malformed_lines=%llu\nlast_line=%s\ninput_clauses_arg=%lld\ninput_plus_additions=%lld\n",
           additions, empty_add, first_empty, min_add, max_add, nonincr, del_lines, deleted_ids, max_live, comments,
           malformed, last, input_clauses, input_clauses + (long long)additions);
  } else {
    printf("header_vars=%lld\nheader_clauses=%lld\nclauses=%lld\nmax_var=%lld\ncomment_lines=%llu\nmalformed_lines=%llu\n"
           "first_comment=%s\n",
           hv, hc, clauses, maxvar, comments, malformed, fcdone ? fc : "");
  }
  return 0;
}
