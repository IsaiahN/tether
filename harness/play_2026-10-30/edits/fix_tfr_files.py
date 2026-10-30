import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8").replace("\r\n", "\n")
R = [
    ('''def mask_fold(rows):
''',
     '''def repo_files():
    """the project .py files imported now, as instruments.Attribution.code() takes them"""
    import os
    import sys
    root = os.path.normcase(os.getcwd()) + os.sep
    return sorted({os.path.relpath(os.path.abspath(f)) for m in list(sys.modules.values())
                   if isinstance(f := getattr(m, "__file__", None), str) and f.endswith(".py")
                   and os.path.normcase(os.path.abspath(f)).startswith(root)
                   and ".venv" not in os.path.relpath(f).split(os.sep)})


def mask_fold(rows):
'''),
    ('''            ai, _l = real_wa(ei, game, cfg, li, library, di, clock=clock)
''',
     '''            hook.setdefault("files0", repo_files())
            ai, _l = real_wa(ei, game, cfg, li, library, di, clock=clock)
'''),
    ('''ag, _l = arc_holdout.wire_agent(env, "fake", None, led, None, d,
''',
     '''files = repo_files()
ag, _l = arc_holdout.wire_agent(env, "fake", None, led, None, d,
'''),
    ('''print(json.dumps({"digest": dg, "rows": rows, "cleared": cleared}, default=str))
''',
     '''print(json.dumps({"digest": dg, "rows": rows, "cleared": cleared, "files": files}, default=str))
'''),
    ('''       "prefix_len": len(hook.get("prefix", b"")), "resets": hook.get("resets")}
''',
     '''       "prefix_len": len(hook.get("prefix", b"")), "resets": hook.get("resets"),
       "files0": hook.get("files0")}
'''),
    ('''                     for k in ("modules", "not_loaded", "on", "off")
                     if isinstance(a0.get(k), list)})
''',
     '''                     for k in ("modules", "not_loaded", "on", "off")
                     if isinstance(a0.get(k), list)},
                    {"files": (sorted(set(r["files0"]) - set(c["files"])),
                               sorted(set(c["files"]) - set(r["files0"])))})
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
