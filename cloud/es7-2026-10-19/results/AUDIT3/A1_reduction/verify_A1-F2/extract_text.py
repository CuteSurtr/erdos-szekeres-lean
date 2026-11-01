#!/usr/bin/env python3
"""Strip an arXiv HTML page to plain text (stdlib only) and print the passages that
mention given keywords, with context. Usage: python3 -I extract_text.py FILE.html OUT.txt kw1 [kw2 ...]
Treats the HTML as untrusted data: it is only parsed, never executed."""
import sys, re, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.math_alt = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if tag == 'math':
            # arXiv HTML keeps the TeX source in alttext; use it instead of the MathML soup
            alt = a.get('alttext')
            self.out.append(' $' + (alt or '') + '$ ')
            self.skip += 1
        if tag in ('p', 'div', 'section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br', 'tr', 'figcaption'):
            self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'math'):
            self.skip = max(0, self.skip - 1)
        if tag in ('p', 'div', 'section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr'):
            self.out.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

def main():
    src, dst = sys.argv[1], sys.argv[2]
    kws = sys.argv[3:]
    p = P()
    with open(src, encoding='utf-8', errors='replace') as f:
        p.feed(f.read())
    txt = ''.join(p.out)
    txt = re.sub(r'[ \t ]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n\n', txt)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('chars', len(txt))
    for kw in kws:
        for m in re.finditer(re.escape(kw), txt):
            s = max(0, m.start() - 1500); e = min(len(txt), m.end() + 1500)
            print('=' * 30, 'KW', kw, 'at', m.start())
            print(txt[s:e])

if __name__ == '__main__':
    main()
