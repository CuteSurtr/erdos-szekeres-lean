// cnfstat: read a DIMACS CNF on stdin (streamed, never held in memory).
// Prints: bytes, SHA-256, the comment lines before the header (first 300 chars each), the header values,
// the number of clauses actually present (0-terminated literal lists after the header), empty clauses,
// literal count, max |var|. lrat-check counts *parsed* clauses as "added", while it prints the *header* values on
// its "parsed a formula" line, so both numbers are needed to compare with its log.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <CommonCrypto/CommonDigest.h>

#define BUF (1 << 24)

int main(void) {
  unsigned char *buf = malloc(BUF);
  if (!buf) return 2;
  CC_SHA256_CTX sha; CC_SHA256_Init(&sha);
  uint64_t bytes = 0;
  // states: line-start, in comment, in header, in body
  int at_line_start = 1, in_comment = 0, header_seen = 0;
  char hdr[256]; int hlen = 0, in_header = 0;
  char cmt[301]; int clen = 0;
  int64_t num = 0; int neg = 0, innum = 0;
  uint64_t clauses = 0, empty = 0, lits = 0, cur_len = 0, maxvar = 0, bad = 0, comments_after_header = 0;
  size_t n;
  while ((n = fread(buf, 1, BUF, stdin)) > 0) {
    CC_SHA256_Update(&sha, buf, (CC_LONG)n);
    bytes += n;
    for (size_t i = 0; i < n; i++) {
      unsigned char ch = buf[i];
      if (in_comment) {
        if (ch == '\n') { in_comment = 0; at_line_start = 1;
          if (!header_seen) { cmt[clen] = 0; printf("comment: %s\n", cmt); } clen = 0; }
        else if (!header_seen && clen < 300) cmt[clen++] = ch;
        continue; }
      if (in_header) {
        if (ch == '\n') { in_header = 0; at_line_start = 1; hdr[hlen] = 0; header_seen = 1; printf("header: %s\n", hdr); }
        else if (hlen < 255) hdr[hlen++] = ch;
        continue; }
      if (at_line_start && !innum) {
        if (ch == 'c') { in_comment = 1; at_line_start = 0; if (header_seen) comments_after_header++; continue; }
        if (ch == 'p') { if (header_seen) bad++; in_header = 1; at_line_start = 0; hdr[hlen++] = ch; continue; }
      }
      if (ch >= '0' && ch <= '9') { num = num * 10 + (ch - '0'); innum = 1; at_line_start = 0; continue; }
      if (ch == '-') { if (innum) bad++; neg = 1; at_line_start = 0; continue; }
      // separator
      if (innum) {
        if (!header_seen) bad++;
        if (num == 0) { if (neg) bad++; clauses++; if (cur_len == 0) empty++; cur_len = 0; }
        else { lits++; cur_len++; if ((uint64_t)num > maxvar) maxvar = (uint64_t)num; }
        num = 0; neg = 0; innum = 0; }
      else if (neg) bad++;
      if (ch == '\n') at_line_start = 1;
      else if (ch == ' ' || ch == '\t' || ch == '\r') { }
      else bad++;
    }
  }
  if (innum) { if (num == 0) { clauses++; if (cur_len == 0) empty++; cur_len = 0; } else { lits++; cur_len++; } }
  unsigned char md[CC_SHA256_DIGEST_LENGTH]; CC_SHA256_Final(md, &sha);
  printf("bytes: %llu\nsha256: ", (unsigned long long)bytes);
  for (int i = 0; i < CC_SHA256_DIGEST_LENGTH; i++) printf("%02x", md[i]);
  printf("\nclauses_present: %llu\nempty_clauses: %llu\nliterals: %llu\nmax_var: %llu\n"
         "unterminated_tail_literals: %llu\ncomments_after_header: %llu\nparse_anomalies: %llu\n",
         (unsigned long long)clauses, (unsigned long long)empty, (unsigned long long)lits,
         (unsigned long long)maxvar, (unsigned long long)cur_len, (unsigned long long)comments_after_header,
         (unsigned long long)bad);
  return 0;
}
