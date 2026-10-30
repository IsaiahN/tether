import base64, re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.findall(sys.argv[2] + r"[A-Za-z0-9+/=]+", t)
b = max(m, key=len)
print(base64.b64decode(b + "=" * (-len(b) % 4)).decode("utf-8", "replace"))
