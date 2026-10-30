"""r440 item 3 SIGNATURE SWEEP (read only): every function kind_spy.py wraps, the wrapped original's parameters at the
tree given, against the wrapper's parameters in the spy file given. argv: tree spy_file"""
import importlib.machinery
import importlib.util
import inspect
import sys

sys.dont_write_bytecode = True
tree, spy = sys.argv[1], sys.argv[2]
sys.path = [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
sys.path.insert(0, tree)
import interface as IFace  # noqa: E402
import tether  # noqa: E402

orig = {"Agent.perceive": tether.Agent.perceive, "Interface.audit": IFace.Interface.audit,
        "Interface._kind_fallback": IFace.Interface._kind_fallback, "Interface.realise": IFace.Interface.realise,
        "Agent._slot_kind_key": tether.Agent._slot_kind_key}
s = importlib.util.spec_from_file_location("kind_spy_under_test", spy,   # any suffix (the kept .0622d0e9 copy)
                                           loader=importlib.machinery.SourceFileLoader("kind_spy_under_test", spy))
ks = importlib.util.module_from_spec(s)
s.loader.exec_module(ks)       # defines the wrappers; install() is NOT called, so nothing is patched
wrap = {"Agent.perceive": ks.perceive, "Interface.audit": ks.audit, "Interface._kind_fallback": ks.kind_fallback,
        "Interface.realise": ks.realise, "Agent._slot_kind_key": ks.slot_kind_key}
behind = {}
for k in orig:
    po, pw = inspect.signature(orig[k]).parameters, inspect.signature(wrap[k]).parameters
    var_kw = any(p.kind == p.VAR_KEYWORD for p in pw.values())
    var_pos = any(p.kind == p.VAR_POSITIONAL for p in pw.values())
    missing = [n for n, p in po.items() if n not in pw and not (var_kw and p.kind != p.VAR_POSITIONAL)
               and not (var_pos and p.kind == p.VAR_POSITIONAL)]
    if missing:
        behind[k] = missing
    print(f"{k}\n  original: ({', '.join(str(p) for p in po.values())})\n  wrapper:  ({', '.join(str(p) for p in pw.values())})"
          f"\n  missing in wrapper: {missing or 'none'}")
# r441: a precheck line -- its last line is what the precheck log shows; any wrapper behind its original is red
print(f"spy_sweep: {len(orig)} wrappers, {len(behind)} behind {behind or ''}")
sys.exit(1 if behind else 0)
