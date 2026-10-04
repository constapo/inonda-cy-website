#!/usr/bin/env python3
"""Check every language file has the same structure as en.py (keys, list lengths, tuple sizes)."""
import importlib.util, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
def load(l, var="T"):
    s = importlib.util.spec_from_file_location(l, os.path.join(D, l + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return getattr(m, var)
def cmp(a, b, path, errs):
    if isinstance(a, dict):
        if not isinstance(b, dict): errs.append(f"{path}: not a dict"); return
        for k in a:
            if k not in b: errs.append(f"{path}.{k}: missing")
            else: cmp(a[k], b[k], f"{path}.{k}", errs)
        for k in b:
            if k not in a and k != "lang_note": errs.append(f"{path}.{k}: extra")
    elif isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)): errs.append(f"{path}: not a list"); return
        if len(a) != len(b) and not path.endswith(("]", "list", "items")):
            errs.append(f"{path}: length {len(b)} != {len(a)}")
        for i, (x, y) in enumerate(zip(a, b)):
            if isinstance(x, (dict, list, tuple)): cmp(x, y, f"{path}[{i}]", errs)
    elif isinstance(a, str) and not isinstance(b, str): errs.append(f"{path}: not text")
en = load("en"); bad = 0
for l in sys.argv[1:] or [f[:-3] for f in os.listdir(D) if f.endswith(".py") and f != "en.py" and not f.startswith("local_")]:
    errs = []; cmp(en, load(l), l, errs)
    print(l, "OK" if not errs else f"{len(errs)} problems"); [print("  ", e) for e in errs[:30]]; bad += len(errs)
# area pages and guides (local_<lang>.py) must match local_en.py
if os.path.exists(os.path.join(D, "local_en.py")):
    len_ = load("local_en", "L")
    for f in sorted(os.listdir(D)):
        if f.startswith("local_") and f.endswith(".py") and f != "local_en.py":
            errs = []; cmp(len_, load(f[:-3], "L"), f[:-3], errs)
            print(f[:-3], "OK" if not errs else f"{len(errs)} problems"); [print("  ", e) for e in errs[:30]]; bad += len(errs)
sys.exit(1 if bad else 0)
