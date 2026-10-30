import base64, re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for fid in sys.argv[3:]:
    m = re.findall(r'\?"content\?":\?"([A-Za-z0-9+/=]{200,})\?",\?"id\?":\?"' + re.escape(fid), t)
    if m:
        open(sys.argv[2] + "/" + fid + ".txt", "w", encoding="utf-8").write(base64.b64decode(m[-1]).decode("utf-8", "replace"))
        print(fid, "ok")
    else:
        print(fid, "missing")
