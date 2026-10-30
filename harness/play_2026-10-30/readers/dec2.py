import base64, re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for pre, out in (("UmV2aWV3ZXIgLT4gU2VhdCAtLSAyMDI2LTEwLTIzIDE5OjEz", "watson_1913.txt"), ("UmV2aWV3ZXIgLT4gU2VhdCAtLSAyMDI2LTEwLTIzIDE5OjIx", "approved_1921.txt")):
    m = re.findall(pre + r"[A-Za-z0-9+/=]+", t)
    best = max(m, key=len) if m else ""
    open(sys.argv[2] + "/" + out, "w", encoding="utf-8").write(base64.b64decode(best + "=" * (-len(best) % 4)).decode("utf-8", "replace"))
    print(out, len(best))
