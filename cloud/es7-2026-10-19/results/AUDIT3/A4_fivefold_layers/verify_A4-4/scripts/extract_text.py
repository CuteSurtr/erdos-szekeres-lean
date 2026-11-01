# Strip HTML to text and print the passages around given keywords (read-only on the input file).
import sys, re, html
path = sys.argv[1]
kw = [k.lower() for k in sys.argv[2:]]
raw = open(path, encoding='utf-8', errors='replace').read()
# drop scripts/styles and math annotation duplicates
raw = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', raw)
raw = re.sub(r'(?is)<annotation[^>]*>.*?</annotation>', ' ', raw)
raw = re.sub(r'(?is)<annotation-xml[^>]*>.*?</annotation-xml>', ' ', raw)
# keep math alttext if present
raw = re.sub(r'(?is)<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: ' $'+m.group(1)+'$ ', raw)
raw = re.sub(r'(?i)<(br|p|div|section|h[1-6]|li|tr)[^>]*>', '\n', raw)
txt = re.sub(r'<[^>]+>', ' ', raw)
txt = html.unescape(txt)
txt = re.sub(r'[ \t\r\f\v]+', ' ', txt)
txt = re.sub(r'\n\s*\n+', '\n', txt)
paras = [p.strip() for p in txt.split('\n') if p.strip()]
for i, p in enumerate(paras):
    pl = p.lower()
    if any(k in pl for k in kw):
        print(f'[{i}] {p}\n')
