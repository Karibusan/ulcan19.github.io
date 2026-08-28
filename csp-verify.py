#!/usr/bin/env python3
"""Vérifie qu'une page servie porte des hashes CSP corrects.

Usage: python3 csp-verify.py notes/index.html
       curl -s https://yan.kitaribu.xyz/notes/ > /tmp/p.html && python3 csp-verify.py /tmp/p.html

Utile quand une page part en ligne via un éditeur web : coller du HTML peut
normaliser les fins de ligne ou ajouter un retour final, ce qui change le
hash sans rien changer de visible dans le diff.
"""
import base64, hashlib, re, sys

def csp_hash(body: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode() + "'"

for path in sys.argv[1:]:
    html = open(path, encoding="utf-8").read()
    csp = re.search(r'Content-Security-Policy" content="([^"]+)"', html)
    if not csp:
        print(f"{path}: aucune CSP trouvée"); continue
    csp = csp.group(1)
    ok = True
    for tag in ("style", "script"):
        m = re.search(rf"<{tag}>(.*?)</{tag}>", html, re.S)
        if not m:
            continue
        want = csp_hash(m.group(1))
        if want in csp:
            print(f"{path}  {tag:7} MATCH")
        else:
            ok = False
            print(f"{path}  {tag:7} MISMATCH")
            print(f"    la CSP doit contenir : {want}")
    sys.exit(0 if ok else 1)
