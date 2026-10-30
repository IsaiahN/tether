import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8").replace("\r\n", "\n")
R = [
    ('''        import pickle
        hook["board"], hook["clock"], hook["palette"] = d + "_board.pkl", list(clock), env._palette
        with open(hook["board"], "wb") as fh:       # (r2b): the board at the fault, for a cold step
            pickle.dump(copy.deepcopy(env.w.w), fh)
''',
     '''        b = env.w.w                                 # (r2b): the board at the fault, as fields
        hook["board"] = json.dumps({"pos": list(b.pos), "n": b.n, "calls": list(b.calls),
                                    "state": b._last.state.name})
        hook["clock"], hook["palette"] = list(clock), env._palette
'''),
    ('''import json, pickle, arc_holdout, ledger, tether
''',
     '''import json, arc_holdout, ledger, tether
from test_entry import FakeWrapper, GameState
'''),
    ('''with open(sys.argv[3], "rb") as fh:
    board = pickle.load(fh)
''',
     '''b = json.loads(sys.argv[3])
board = FakeWrapper(script={})
board.pos, board.n, board.calls = b["pos"], b["n"], b["calls"]
board._frame(GameState[b["state"]])
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
