"""(B), THE KIND-ROUTE SPY (the reviewer 2026-10-25 15:17 item 3): harness-side, no agent code changed. It OBSERVES calls the
agent already makes and adds no call into agent code (so no cache is warmed at another moment): Interface.realise for asker
goal / hyp_route, Interface._kind_fallback inside it, Interface.audit, Agent._slot_kind_key, Agent.perceive (for the cycle).
Every other read is a read of the interface's own dicts. Writes OUT/kind_spy.jsonl, one JSON row per event:
  start    at the first perceive: the interface table's cell counts (delta, delta_kind, lands_kind) -- the empty-start check
  audit    per audit that touched a kind cell: cycle, action, coord, era (epoch, breaks), and per delta_kind / lands_kind key it
           moved: the key (ctx, kind key incl. the form, rel or value-before), the cell before, the increment, and whether this
           press bore the earlier entry out (E2 (b)'s era_kinds rule, computed here, not by the agent)
  realise  per realise for asker goal / hyp_route (the round's first one also carries the table's cell counts): cycle, asker,
           intent, subject, value, the kind key _kind_fallback returned,
           per offered action the kind cell for that key (this ctx; and every ctx with its rel, n, total), the result (action,
           coord, why), and whether the key is in the spy's era_kinds for the current era
  key      each later cycle's first kind key the agent itself computed for a subject a realise row named
  error    a spy failure (the spy never raises into the agent; each failure is a row)
    install(out_dir) after arc_holdout and tether are importable from the tree."""
import json
import os

import interface as IFace
import tether

I, A = IFace.Interface, tether.Agent
_st = {"agent": None, "out": None, "started": False, "realised": False, "era": None, "era_kinds": set(), "asked": set(),
       "keyed": set(),
       "kf": []}     # kf: a stack, one list per open goal / hyp_route realise (realise re-asks itself without RESET)


def _row(**kw):
    try:
        ag = _st["agent"]
        with open(_st["out"], "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"cycle": getattr(ag, "cycle", None), **kw}, default=repr) + "\n")
    except Exception:  # noqa: BLE001,S110 -- the row writer itself failed: nowhere left to report, and never into the agent
        pass


def _err(where, e):
    _row(event="error", where=where, error=repr(e))


def _cells(iface):
    t = iface.table
    return {"actions": len(t), "delta": sum(len(e.get("delta", {})) for e in t.values()),
            "delta_kind": sum(len(e.get("delta_kind", {})) for e in t.values()),
            "lands_kind": sum(len(e.get("lands_kind", {})) for e in t.values())}


_perceive = A.perceive


def perceive(self, *a, **k):
    _st["agent"] = self
    if not _st["started"]:
        _st["started"] = True
        try:
            _row(event="start", cells=_cells(self.iface))
        except Exception as e:  # noqa: BLE001
            _err("start", e)
    return _perceive(self, *a, **k)


_audit = I.audit


def audit(self, r, before, after, ctx=(), ctx_after=None, own=frozenset(), **kw):
    snap = None
    try:
        e = self.table.get(r.action, {})
        snap = ({k: tuple(v) for k, v in e.get("delta_kind", {}).items()},
                {k: frozenset(v) for k, v in e.get("lands_kind", {}).items()})
    except Exception as ex:  # noqa: BLE001
        _err("audit-before", ex)
    out = _audit(self, r, before, after, ctx, ctx_after, own, **kw)   # reaff=, meant= (10-26)
    if snap is None:
        return out
    try:
        era = (self.epoch, self.breaks)
        if _st["era"] != era:
            _st["era"], _st["era_kinds"] = era, set()
        e = self.table.get(r.action, {})
        moved = []
        for k, v in e.get("delta_kind", {}).items():
            n0, t0 = snap[0].get(k, (0, 0))
            if v[0] != n0:
                dn, dt = v[0] - n0, v[1] - t0
                bore = bool(n0 and t0 * dt > 0)
                if bore:
                    _st["era_kinds"].add(k[1])
                moved.append({"t": "delta_kind", "ctx": k[0], "kind": k[1], "rel": k[2], "before": [n0, t0],
                              "inc": [dn, dt], "bore_out": bore})
        for k, v in e.get("lands_kind", {}).items():
            v0 = snap[1].get(k, frozenset())
            if set(v) != set(v0):
                bore = bool(v0 & set(v))
                if bore:
                    _st["era_kinds"].add(k[1])
                moved.append({"t": "lands_kind", "ctx": k[0], "kind": k[1], "from": k[2], "before": sorted(v0),
                              "after": sorted(v), "bore_out": bore})
        if moved:
            _row(event="audit", action=r.action, coord=list(r.coord) if r.coord else None, era=list(era), moved=moved)
    except Exception as ex:  # noqa: BLE001
        _err("audit-after", ex)
    return out


_kf = I._kind_fallback


def kind_fallback(self, slot, env):
    out = _kf(self, slot, env)
    if _st["kf"]:
        _st["kf"][-1].append(out)
    return out


_re = I.realise


def realise(self, intent, offered, ctx=(), state=None, env=None, withheld=IFace.NO_WITHHELD, cell=True, asker=None,
            split=None):     # split: 1b ASK's (2a8045c), passed through unchanged (the reviewer r440)
    if asker not in ("goal", "hyp_route"):
        return _re(self, intent, offered, ctx, state, env, withheld, cell, asker, split=split)
    _st["kf"].append([])
    try:
        r = _re(self, intent, offered, ctx, state, env, withheld, cell, asker, split=split)
    finally:
        kf = _st["kf"].pop()
    try:
        sub = intent.subject
        key = kf[0] if kf else None
        per = {}
        for a in offered:
            dk = self.table.get(a, {}).get("delta_kind", {})
            cells = [[list(c) if isinstance(c, tuple) else c, rel, v[0], v[1]] for (c, ks, rel), v in dk.items()
                     if key is not None and ks == key]
            here = [x for x in cells if x[0] == (list(ctx) if isinstance(ctx, tuple) else ctx)]
            per[a] = {"here": here, "all": cells}
        if sub:
            _st["asked"].add(sub)
        era = (self.epoch, self.breaks)
        first = {} if _st["realised"] else {"first_realise_cells": _cells(self)}
        _st["realised"] = True
        _row(event="realise", asker=asker, intent=intent.says(), subject=sub, **first,
             value=None if state is None else state.get(sub), kind_key=key, ctx=ctx, kind_cells=per,
             in_era_kinds=bool(key is not None and _st["era"] == era and key in _st["era_kinds"]),
             result=None if r is None else {"action": r.action, "coord": list(r.coord) if r.coord else None, "why": r.why})
    except Exception as ex:  # noqa: BLE001
        _err("realise", ex)
    return r


_sk = A._slot_kind_key


def slot_kind_key(self, slot):
    out = _sk(self, slot)
    try:
        c = getattr(self, "cycle", None)
        if slot in _st["asked"] and (c, slot) not in _st["keyed"]:
            _st["keyed"].add((c, slot))
            _row(event="key", subject=slot, kind_key=out)
    except Exception as ex:  # noqa: BLE001
        _err("key", ex)
    return out


def install(out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    _st["out"] = os.path.join(out_dir, "kind_spy.jsonl")
    A.perceive, I.audit, I._kind_fallback, I.realise, A._slot_kind_key = (perceive, audit, kind_fallback, realise,
                                                                         slot_kind_key)
