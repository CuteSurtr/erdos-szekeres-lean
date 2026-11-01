/* A6 audit: streaming fingerprint of a textual LRAT proof read from stdin.
 * Counts addition lines (and how many are the empty clause), deletion lines and deleted clause IDs, the largest
 * clause ID, malformed lines, and total bytes/lines. Constant memory.
 * Output (one line): bytes lines additions empty_additions first_empty_id last_line_kind deletion_lines deleted_ids
 *                    max_id comment_lines malformed
 * Line grammar (CaDiCaL --lrat --binary=false):  id lit* 0 hint* 0   |   id d id* 0
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    static unsigned char buf[1 << 22];
    unsigned long long bytes = 0, lines = 0, adds = 0, empties = 0, dlines = 0, dids = 0, maxid = 0, comments = 0,
                       malformed = 0, first_empty = 0;
    /* per-line state */
    int tok = 0;          /* tokens completed on this line */
    int is_del = 0, is_comment = 0, phase = 0; /* phase: 0 id, 1 lits/dels, 2 hints, 3 after final 0 */
    long long lits = 0;   /* literals before first 0 */
    int in_num = 0, neg = 0, saw_d = 0;
    unsigned long long val = 0, cur_id = 0;
    int last_kind = 0;    /* 1 add, 2 empty add, 3 delete */
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, stdin)) > 0) {
        bytes += n;
        for (size_t i = 0; i < n; i++) {
            unsigned char ch = buf[i];
            if (is_comment) { if (ch == '\n') { is_comment = 0; lines++; tok = 0; phase = 0; } continue; }
            if (ch >= '0' && ch <= '9') { val = val * 10 + (ch - '0'); in_num = 1; continue; }
            if (ch == '-') { neg = 1; in_num = 1; val = 0; continue; }
            if (ch == 'd' && tok == 1 && !in_num) { saw_d = 1; continue; }
            if (ch == 'c' && tok == 0 && !in_num) { is_comment = 1; comments++; continue; }
            if (ch == ' ' || ch == '\n' || ch == '\t' || ch == '\r') {
                if (saw_d) { saw_d = 0; is_del = 1; tok++; phase = 1; }
                else if (in_num) {
                    /* finished a number token */
                    if (tok == 0) { cur_id = val; if (val > maxid) maxid = val; phase = 1; }
                    else if (is_del) {
                        if (val == 0) phase = 3; else if (phase == 1) dids++; else malformed++;
                    } else {
                        if (phase == 1) { if (val == 0) phase = 2; else lits++; }
                        else if (phase == 2) { if (val == 0) phase = 3; }
                        else malformed++;
                    }
                    tok++; in_num = 0; neg = 0; val = 0;
                }
                if (ch == '\n') {
                    if (tok > 0) {
                        lines++;
                        if (phase != 3) malformed++;
                        else if (is_del) { dlines++; last_kind = 3; }
                        else { adds++; if (lits == 0) { empties++; last_kind = 2; if (!first_empty) first_empty = cur_id; } else last_kind = 1; }
                    }
                    tok = 0; is_del = 0; phase = 0; lits = 0;
                }
                continue;
            }
            malformed++;
        }
    }
    (void)neg;
    printf("%llu %llu %llu %llu %llu %s %llu %llu %llu %llu %llu\n", bytes, lines, adds, empties, first_empty,
           last_kind == 1 ? "add" : last_kind == 2 ? "empty" : last_kind == 3 ? "delete" : "none", dlines, dids, maxid,
           comments, malformed);
    return 0;
}
