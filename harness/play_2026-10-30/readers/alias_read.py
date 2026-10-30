"""Read-only (the reviewer r268 item 2): each generation file's own aliases (was -> key), how many name an object id
(oN), a 10-name sample, and the overlap of those names with that round's reuse_install terms. Opens only the gen
JSON files (written once, content-addressed), never memory.db. argv: lineage dir, then pairs gen_head:round_dir."""
import json
import re
import sys
import zlib

sys.dont_write_bytecode = True
OBJ = re.compile(r"\bo\d+\b")
LIN = sys.argv[1]
for pair in sys.argv[2:]:
    head, rnd = pair.split(":", 1)
    raw = open(f"{LIN}/gen_{head}.json", "rb").read()
    g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    al = g.get("aliases") or []
    was = [str(a.get("was")) for a in al]
    with_obj = [w for w in was if OBJ.search(w)]
    reuse = set()
    if rnd != "-":
        for ln in open(rnd, encoding="utf-8"):
            if '"reuse_install"' in ln:
                try:
                    reuse.add(json.loads(ln)["detail"]["term"])
                except (ValueError, KeyError):
                    pass
    keys = sorted({k for a in al for k in a})
    print(f"== gen_{head}: aliases {len(al)}; keys {keys}; naming an object id {len(with_obj)}; "
          f"equal to a reuse_install term of {rnd.split('/')[-2] if rnd != '-' else '-'} "
          f"({len(reuse)} terms): {sum(1 for w in was if w in reuse)}")
    for a in al[:: max(1, len(al) // 10)][:10]:
        print(f"   was {str(a.get('was'))[:110]}")
