"""The library at run time -- ONE store, three layers, one execution path for every entry.

REFERENCE IMPLEMENTATION by the reviewer seat (2026-10-08) at Isaiah's order, for the seat to
adopt, adapt and own. It touches nothing in tether.py; the wiring points are listed in
LIBRARY_SPEC.md. Pure Python, no imports from the agent, self-test at the bottom.

    SEED      library/*.json + index.json   GIVEN, read-only forever (Isaiah 2026-09-22, 2.4)
    RUNTIME   library/runtime.json          what the agent made or carried THIS run, all games
    LEARNINGS library/learnings.json        promoted when proven by the ground, saved apart
    lookup order: learnings -> runtime -> seed; first hit wins. Ablation: wipe learnings, rerun.

HOW AN ENTRY RUNS -- the metaprogramming, so there are not 4,000 functions:
    PRIMITIVE  an agent atom; arc_atoms builds its callable. Named here, never re-implemented.
    GROUNDED   a PERCEPT or RELATION. ONE generator, `candidates()`, turns an entry's `reads`
               into candidate conditions from a small TEMPLATE FAMILY PER READING TYPE. The
               family is the grammar applied to the type -- a DELTA can be nonzero, positive or
               negative; a pair predicate can hold or not; an ordered quantity can be compared
               (Figure 12's comparison) -- so the same few templates serve every entry, preloaded
               or invented. The agent's bargain decides which candidate, if any, the entry
               means on this board; the term is the PAIR (entry, candidate) (Figure 13).
    COMPOSED   a molecule; its operands are entries, its junctions bonds ('?' = UNKNOWN). One
               constructor, bond as a parameter (composer.bind); settled per junction.

HOW THE SEARCH NARROWS -- the mutation observer as a MAPPING, not a search (RELATIONS.md, Isaiah
2026-09-15/22): every tracked object carries its full reading vector, NULL at frame 0; the
frame's CHANGE is the cue. `light(changed)` reads index.by_reading_reads for each changed
reading and ranks entries by how much of the change they cover (weighted); `molecules_lit()`
walks ingredient_of to the molecules whose operands are all lit. ORDER, NEVER EXCLUDE: nothing
lit is dropped, only ranked.

THE ABDUCTIVE LOOKUP (v7, 2026-10-09) -- "what PRODUCES this", beside "what READS this". A residual
is an EFFECT: o2 changed colour. The forward lookup asks which entries READ colour_changed; the
entry that explains it may only PRODUCE it (MEDICAL|Contagion reads touching / contact / prev and
affects colour_changed, so a pure colour_changed residual never lit it). `produces(changed,
context)` reads index.by_reading_affects -- built since v2, never read at run time until v7 -- and
ranks by how many changed readings the entry produces, then by how much of its own `reads` the
description already holds (`context`: the readings present this frame, e.g. touching), then by
key. It returns atoms AND molecules (a molecule may produce an effect none of its operands does).
`light(changed, abduce=...)` is UNCHANGED with abduce False (the default, byte-identical to v6);
"after" appends the grounded produce-only entries behind the forward list (the forward list is a
prefix); "merged" ranks the union on forward score + produce score. Both modes return the SAME
set: ORDER, NEVER EXCLUDE. Which mode the agent uses is an arm for the seat to measure, not a
choice made here.

HOW THE AGENT ADDS TO IT: `invent_atom` (INVENTED: a new primitive the agent names, from a
pattern it observed and could not compose -- trigger: an abstention receipt, `owed_import`) and
`mint_recipe` (MINTED: a new arrangement of existing entries in its own grammar). Both land in
RUNTIME with the same schema as the seed, are indexed at once, and run through the same path.
`carry()` marks an entry IMPORTED into the next game (Isaiah 2026-10-07: import = across games).
"""

from __future__ import annotations

import json
import re as _re
from collections import defaultdict
from pathlib import Path

PRIOR, MINTED, IMPORTED, INVENTED = "prior", "minted", "imported", "invented"
BONDS = ("+", "∥", "≡", "→", "⇒", "−", "⋛")
UNKNOWN = "?"

# THE TEMPLATE FAMILY PER READING TYPE -- data. `{o}` is the entry's subject object, `{x}` a
# second object (a two-place frame: NSM's TOUCH(X, Y)), `{r}` the reading. Written in
# condition.py's grammar (expr OP expr; SLOT; NUMBER), so the existing compiler parses them.
TEMPLATES = {
    "DELTA": [
        ("moves", "{o}.{r} != 0"),
        ("up", "{o}.{r} > 0"),
        ("down", "{o}.{r} < 0"),
        ("with", "{o}.{r} == {x}.{r}"),
        ("unlike", "{o}.{r} != {x}.{r}"),
    ],
    "EXTENT": [
        ("more", "{o}.{r} > {x}.{r}"),
        ("less", "{o}.{r} < {x}.{r}"),
        ("same", "{o}.{r} == {x}.{r}"),
        ("present", "{o}.{r} > 0"),
    ],
    "POSITION": [
        ("before", "{o}.{r} < {x}.{r}"),
        ("after", "{o}.{r} > {x}.{r}"),
        ("level", "{o}.{r} == {x}.{r}"),
    ],
    "COLOUR": [("same", "{o}.{r} == {x}.{r}"), ("other", "{o}.{r} != {x}.{r}")],
    "SHAPE": [("same", "{o}.{r} == {x}.{r}"), ("other", "{o}.{r} != {x}.{r}")],  # nominal: no order
    "BOOL": [("holds", "{o}.{r} == 1"), ("fails", "{o}.{r} == 0"), ("both", "{o}.{r} == {x}.{r}")],
    "PRED": [("holds", "{r}({o}, {x}) == 1"), ("fails", "{r}({o}, {x}) == 0")],
    "OBJECT": [("occurs", "frame.{r} > 0")],
}
# Pair readings are written as INSTRUMENT calls, `contact(o1, o2)`, because condition.py's NAME
# token
# admits no '~' or '@'; the reader passed to condition.evaluate maps `contact(a, b)` to arc_world's
# slot `a~b.contact`, `board.completed` to `@goal.completed`, and `frame.came` to the frame's
# events.


# ONE ENTRY, SEVERAL VIEWS (Isaiah 2026-10-08: effect / affect -- the noun and the verb are one
# concept). The view is chosen by the slot the entry fills in a frame; grammar.json `roles`.
# Each view selects which templates the generator emits -- nothing is authored per entry.
DELTA_OF = {
    "row": "drow",
    "col": "dcol",
    "h": "dh",
    "w": "dw",
    "filled": "dcells",
    "colour": "colour_changed",
    "shape": "dperimeter",
    "completed": "dcompleted",
    "touching": "dcontact",
    "contact": "dcontact",
    "inside": "dinside",
    "bbox": "dbbox",
    "residual": "dresidual",
    "standing": "dstanding",
    "terms": "dterms",
    "stability": "colour_changed",
    "age": "came",
    "level": "dcompleted",
}
VALUE_TEMPLATES = {
    "same",
    "other",
    "more",
    "less",
    "present",
    "holds",
    "fails",
    "before",
    "after",
    "level",
}
CHANGE_TEMPLATES = {"moves", "up", "down", "occurs", "holds"}
VERDICT_TEMPLATES = {
    "same",
    "other",
    "holds",
    "fails",
    "present",
    "level",
    "with",
    "unlike",
    "both",
}
ORDER_TEMPLATES = {"more", "less", "before", "after"}
COMPARE_TEMPLATES = {
    "more",
    "less",
    "same",
    "before",
    "after",
    "level",
    "present",
    "with",
    "unlike",
    "both",
}
ROLES = (
    "STATE",
    "PROCESS",
    "RELATION",
    "MEASURE",
    "CAUSE",
    "RESULT",
    "INSTRUMENT",
    "TEST",
    "RULE",
    "AGENT",
)


_MEASURE_START = _re.compile(
    r"^(how (much|many|far|often|well|unpredictable)"
    r"|the (number|amount|size|count|least|ratio)|a (count|large value|level))",
    _re.I,
)
_DEFAULT_BY_AGENT = {
    "translate": "PROCESS",
    "recolour": "PROCESS",
    "rotate": "PROCESS",
    "reflect": "PROCESS",
    "count": "MEASURE",
    "distinct": "MEASURE",
    "sum_group": "MEASURE",
    "area": "MEASURE",
    "perimeter": "MEASURE",
    "holes": "MEASURE",
    "corners": "MEASURE",
    "rank_in": "MEASURE",
    "bbox_area": "MEASURE",
    "orbit_size": "MEASURE",
    "abs_delta": "MEASURE",
    "touching_n": "MEASURE",
}


def default_role(e: dict) -> str:
    """The role an entry takes when nothing in the sentence says otherwise -- derived, never
    authored. The same function for a preloaded entry (the build) and a new one (invent_atom /
    mint_recipe)."""
    if (e.get("role_of") or {}).get("role"):
        return e["role_of"]["role"]
    if e.get("kind") == "RELATION":
        return "RELATION"
    if e.get("kind") == "PRIMITIVE":
        return e.get("role_hint") or _DEFAULT_BY_AGENT.get(e.get("name"), "STATE")
    if _MEASURE_START.search((e.get("grid") or {}).get("meaning") or ""):
        return "MEASURE"
    return "PROCESS" if e.get("affects") else "STATE"


# WHAT MAY CROSS AN EPISODE (Isaiah 2026-10-08): colours change every load; private boards may be
# rearranged, rotated or shrunk. So a condition that names a RAW value -- a colour index, a row, a
# size
# -- is a recording of one occasion (Figure 4) and stays in its episode. Only relations cross, and
# an
# axis-bound relation crosses with its axis as a variable (F, the frame transform; T_A,
# abstraction).
_AXIS_SWAP = {
    "row": "col",
    "col": "row",
    "drow": "dcol",
    "dcol": "drow",
    "h": "w",
    "w": "h",
    "dh": "dw",
    "dw": "dh",
    "add_row": "add_col",
    "add_col": "add_row",
    "rem_row": "rem_col",
    "rem_col": "rem_row",
}
_LITERAL = _re.compile(
    r"([A-Za-z_][A-Za-z_0-9.]*(?:\([^)]*\))?)\s*(==|!=|<=|>=|<|>)\s*(-?\d+(?:\.\d+)?)"
)


def carry_check(condition: str, readings: dict) -> tuple[bool, str]:
    """(safe, reason). Safe when every literal is 0, or 1 against a BOOL/PRED reading -- the
    value-free forms the template family uses (moves, holds, present). Any other literal compares a
    raw value: a recording, not a method."""
    for lhs, _op, num in _LITERAL.findall(condition):
        name = lhs.split("(")[0].split(".")[-1]
        spec = readings.get(name, {})
        if float(num) == 0:
            continue
        if float(num) == 1 and spec.get("type") in ("BOOL", "PRED"):
            continue
        return (
            False,
            f"compares {name} with the literal {num}: a raw value, a recording of one occasion",
        )
    return True, "relations only"


def axis_forms(condition: str) -> list[str]:
    """The condition as it reads on a TURNED or MIRRORED board: axes swapped (a 90-degree turn) and
    orderings reversed (a reflection), alone and together. A carried rule is offered in all of them
    at the destination; the ground there decides which holds. Scale needs nothing: the templates
    compare
    objects with each other, never with a size."""
    names = sorted(_AXIS_SWAP, key=len, reverse=True)
    swap = lambda c: _re.sub(r"\b(" + "|".join(names) + r")\b", lambda m: _AXIS_SWAP[m.group(1)], c)  # noqa: E731

    def flip(c: str) -> str:
        return _re.sub(r"(?<![<>=!])([<>])(?!=)", lambda m: "<" if m.group(1) == ">" else ">", c)

    return list(dict.fromkeys([condition, swap(condition), flip(condition), flip(swap(condition))]))


class Library:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.seed: dict[str, dict] = {}
        self.runtime: dict[str, dict] = {}
        self.learnings: dict[str, dict] = {}
        self.readings: dict[str, dict] = {}
        self.by_reading: dict[str, list] = defaultdict(list)
        self.by_affects: dict[str, list] = defaultdict(list)  # v7: reading -> entries producing it
        self.ingredient_of: dict[str, list] = defaultdict(list)

    # ---------------------------------------------------------------- loading
    def load(self) -> Library:
        j = lambda n: json.loads((self.root / n).read_text(encoding="utf-8"))  # noqa: E731
        self.readings = j("readings.json")["readings"]
        for k, e in j("atoms.json")["atoms"].items():
            self.seed[k] = {**e, "origin": PRIOR}
        for k, e in j("molecules.json")["molecules"].items():
            self.seed[k] = {**e, "origin": PRIOR}
        for k, e in j("agent_atoms.json")["atoms"].items():
            self.seed[k] = {**e, "origin": PRIOR}
        for n, e in j("relations.json")["relations"].items():
            self.seed[f"RELATION|{n}"] = {**e, "name": n, "domain": "RELATION", "origin": PRIOR}
        idx = j("index.json")
        for r, rows in idx["by_reading_reads"].items():
            self.by_reading[r] = [tuple(x) for x in rows]
        for r, keys in idx["by_reading_affects"].items():
            self.by_affects[r] = list(keys)
        for k, rows in idx["ingredient_of"].items():
            self.ingredient_of[k] = list(rows)
        for layer, name in ((self.runtime, "runtime.json"), (self.learnings, "learnings.json")):
            p = self.root / name
            if p.exists():
                layer.update(json.loads(p.read_text(encoding="utf-8"))["entries"])
                for k, e in layer.items():
                    self._index(k, e)
        return self

    def get(self, key: str) -> dict | None:
        """learnings -> runtime -> seed, first hit wins (LIBRARY_RETRIEVAL 2.4)."""
        return self.learnings.get(key) or self.runtime.get(key) or self.seed.get(key)

    # ---------------------------------------------------------------- the mapping
    ABDUCE = (False, "after", "merged")

    def light(
        self,
        changed: dict[str, int],
        abduce: bool | str = False,
        context: frozenset | set = frozenset(),
    ) -> list[tuple[str, float]]:
        """`changed`: reading -> how many slots moved on it this frame. Returns entries ranked by
        the weighted share of the change they read. ORDER, NEVER EXCLUDE.

        abduce False (default): the forward lookup only, exactly as v6.
        abduce "after": the forward list, then the GROUNDED entries only `produces` reaches, in its
            order (molecules stay with molecules_lit / produces, as on the forward path).
        abduce "merged": the same set, ranked on forward score + produce score."""
        if abduce not in self.ABDUCE:
            raise ValueError(f"abduce must be one of {self.ABDUCE}, not {abduce!r}")
        score: dict[str, float] = defaultdict(float)
        for r, n in changed.items():
            for k, w in self.by_reading.get(r, ()):
                score[k] += w * (1 if n else 0)
        fwd = sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))
        if not abduce:
            return fwd
        prod = [(k, s) for k, s in self.produces(changed, context) if self._grounded(k)]
        if abduce == "after":
            seen = set(score)
            return fwd + [(k, s) for k, s in prod if k not in seen]
        for k, s in prod:
            score[k] += s
        return sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))

    def produces(
        self, changed: dict[str, int], context: frozenset | set = frozenset()
    ) -> list[tuple[str, float]]:
        """THE ABDUCTIVE LOOKUP: entries filed as PRODUCING a changed reading
        (index.by_reading_affects), atoms and molecules. Score = how many of the changed readings
        the entry produces; ties ranked by the weighted share of the entry's own `reads` that the
        description holds (`context` plus the changed readings), then by key. ORDER, NEVER
        EXCLUDE: every entry filed under a changed reading is returned."""
        hit: dict[str, float] = defaultdict(float)
        for r, n in changed.items():
            if not n:
                continue
            for k in self.by_affects.get(r, ()):
                hit[k] += 1.0
        held = set(context) | {r for r, n in changed.items() if n}

        def seen(k: str) -> float:
            e = self.get(k) or {}
            w = e.get("reads_weight") or {}
            return sum(w.get(r, 1.0) for r in e.get("reads", []) if r in held)

        return sorted(hit.items(), key=lambda kv: (-kv[1], -seen(kv[0]), kv[0]))

    def _grounded(self, key: str) -> bool:
        e = self.get(key)
        return e is not None and e.get("kind") != "COMPOSITE"

    def molecules_lit(self, lit: set[str]) -> list[dict]:
        """Walk ingredient_of upward: a molecule is offered when ALL its operands are lit (or are
        themselves offered molecules). Junction bonds stay as written ('?' = UNKNOWN)."""
        offered, frontier = set(), set(lit)
        out = []
        while frontier:
            nxt = set()
            for k in frontier:
                for m in self.ingredient_of.get(k, ()):
                    if m in offered:
                        continue
                    e = self.get(m)
                    ops = [o["ref"] for o in e["run"]["operands"]]
                    if all(o in lit or o in offered for o in ops):
                        offered.add(m)
                        nxt.add(m)
                        out.append({"key": m, "operands": ops, "junctions": e["run"]["junctions"]})
            frontier = nxt
        return out

    def view(self, key: str, role: str | None = None, o: str = "o1", x: str = "o2") -> list[dict]:
        """THE ROLE GENERATOR: the entry's candidates in one ROLE, from the same reads and the same
        template family. `role` defaults to the entry's own `role_of.role`, else STATE.

            STATE        its value this frame (every value template)
            TEST         the yes/no question only: does it hold -- verdict templates
                         (same/other/holds/fails/present), no ordering or threshold
            RULE         the STATE, quantified: it holds of EVERY object in scope, every frame
                         (carries "quantifier"; it compiles only through a group row)
            PROCESS      its change across frames (deltas, events) -- 'X of y'
            RELATION     against a second object: every comparison (nominal and ordered)
            MEASURE      a MAGNITUDE only: ordered comparisons on EXTENT / POSITION readings,
                         plus board- and self-level quantities -- 'how much'
            CAUSE        a state of o, then a change of x      (if STATE(o) ⇒ PROCESS(x))
            RESULT       a change of o, then the state it ends (if PROCESS(o) ⇒ STATE(o))
            AGENT        the agent's own action on o is followed by a change of o
                         (if action(agent, o) ⇒ PROCESS(o)) -- the actor is the agent
            INSTRUMENT   the change happens to o only while x takes part (touching)
        v6 (2026-10-08): the views were identical in two triples (STATE=TEST=RULE,
        CAUSE=RESULT=AGENT), found by the seat's compile census; each is now its own view and
        the self-test asserts they differ."""
        e = self.get(key)
        if e is None:
            return []
        role = role or (e.get("role_of") or {}).get("role") or "STATE"
        if role not in ROLES:
            raise ValueError(f"{role!r} is not a role ({ROLES})")
        base = self.candidates(key, o, x)
        if role in ("STATE", "TEST", "RULE"):
            out = [
                c
                for c in base
                if (
                    c["template"] in VALUE_TEMPLATES
                    and self.readings[c["reading"]]["type"] != "DELTA"
                )
                or self.readings[c["reading"]]["scope"] == "event"
            ]  # an event's state is that it happened
            inverse = {d: v for v, d in DELTA_OF.items()}
            for r in e.get("reads") or []:  # a change reading's STATE view is the value it changes
                v = inverse.get(r)
                if v and v in self.readings and not any(c["reading"] == v for c in out):
                    for label, tpl in TEMPLATES.get(self.readings[v]["type"], []):
                        if label in VALUE_TEMPLATES:
                            out.append(
                                {
                                    "entry": key,
                                    "reading": v,
                                    "template": label,
                                    "condition": tpl.format(o=o, x=x, r=v),
                                    "weight": 0.5,
                                    "status": self.readings[v].get("status"),
                                    "via": f"value under {r}",
                                }
                            )
            if role == "TEST":  # the yes/no question: verdicts only, no ordering
                out = [c for c in out if c["template"] in VERDICT_TEMPLATES]
            elif role == "RULE":  # holds of EVERY object in scope, on every frame
                out = [{**c, "quantifier": "ALL objects, every frame", "scope": o} for c in out]
        elif role == "PROCESS":
            out = [
                c
                for c in base
                if (
                    c["template"] in CHANGE_TEMPLATES
                    and self.readings[c["reading"]]["type"] in ("DELTA", "OBJECT", "BOOL")
                )
                or (
                    self.readings[c["reading"]]["scope"] == "context" and c["template"] == "present"
                )
            ]  # an action taken
            for r in e.get("affects") or []:  # what the entry CHANGES is its process, first
                if r in self.readings and self.readings[r]["type"] in ("DELTA", "BOOL", "OBJECT"):
                    for label, tpl in TEMPLATES.get(self.readings[r]["type"], []):
                        if label in CHANGE_TEMPLATES:
                            out.append(
                                {
                                    "entry": key,
                                    "reading": r,
                                    "template": label,
                                    "condition": tpl.format(o=o, x=x, r=r),
                                    "weight": 1.0,
                                    "status": self.readings[r].get("status"),
                                    "via": "affects",
                                }
                            )
            for r in e.get("reads") or []:  # a value reading's PROCESS view is its delta
                d = DELTA_OF.get(r)
                if d and d in self.readings:
                    t = self.readings[d]["type"]
                    for label, tpl in TEMPLATES.get(t, []):
                        if label in CHANGE_TEMPLATES or label in ("up", "down", "moves"):
                            out.append(
                                {
                                    "entry": key,
                                    "reading": d,
                                    "template": label,
                                    "condition": tpl.format(o=o, x=x, r=d),
                                    "weight": (e.get("reads_weight") or {}).get(r, 0.5),
                                    "status": self.readings[d].get("status"),
                                    "via": f"change of {r}",
                                }
                            )
            out.sort(key=lambda c: -c["weight"])  # the change of what it is ABOUT comes first
            seen: set = set()  # one row per condition: the highest-weighted source is kept
            out = [c for c in out if not (c["condition"] in seen or seen.add(c["condition"]))]
        elif role in ("RELATION", "MEASURE"):
            out = [
                c
                for c in base
                if c["template"] in COMPARE_TEMPLATES
                and (f"{x}" in c["condition"] or self.readings[c["reading"]]["scope"] == "pair")
            ]
            if role == "MEASURE":  # a magnitude: ordered comparisons, plus board/self quantities
                out = [
                    c
                    for c in out
                    if c["template"] in ORDER_TEMPLATES
                    and self.readings[c["reading"]]["type"] in ("EXTENT", "POSITION")
                ]
                out += [
                    c
                    for c in base
                    if self.readings[c["reading"]]["scope"] in ("board", "self") and c not in out
                ]
        else:  # CAUSE, RESULT, AGENT, INSTRUMENT: two-part, built from the STATE and PROCESS views
            if role == "RESULT":  # a change of o, then the state o ends in
                ch, st = self.view(key, "PROCESS", o, x), self.view(key, "STATE", o, x)
                return [
                    {
                        "entry": key,
                        "role": role,
                        "if": a["condition"],
                        "then": b["condition"],
                        "bond": "⇒",
                        "weight": min(a["weight"], b["weight"]),
                    }
                    for a in ch[:6]
                    for b in st[:6]
                ]
            if role == "AGENT":  # the agent acts on o, then o changes
                return [
                    {
                        "entry": key,
                        "role": role,
                        "if": f"action(agent, {o}) == 1",
                        "then": c["condition"],
                        "bond": "⇒",
                        "weight": c["weight"],
                    }
                    for c in self.view(key, "PROCESS", o, x)
                ]
            st = self.view(key, "STATE", o, x)  # CAUSE: a state of o, then a change of x
            pr = self.view(key, "PROCESS", x, o)
            if role == "INSTRUMENT":
                out = [
                    {
                        "entry": key,
                        "role": role,
                        "if": f"touching({o}, {x}) == 1",
                        "then": c["condition"],
                        "bond": "+",
                        "weight": c["weight"],
                    }
                    for c in self.view(key, "PROCESS", o, x)
                ]
            else:
                out = [
                    {
                        "entry": key,
                        "role": role,
                        "if": a["condition"],
                        "then": b["condition"],
                        "bond": "⇒",
                        "weight": min(a["weight"], b["weight"]),
                    }
                    for a in st[:6]
                    for b in pr[:6]
                ]
            return out
        return [{**c, "role": role} for c in out]

    def role_table(self, key: str) -> dict:
        """THE GENERIC STEP every entry goes through, preloaded or new: its default role, how many
        candidates it has in each role, and an example of the main ones. Needs only the entry's
        `reads` (and `affects`, if it changes anything) -- nothing is written per role."""
        e = self.get(key)
        d = default_role(e)
        table = {"default": d, "available": {}, "example": {}}
        if e.get("run", {}).get("route") in ("GROUNDED", "COMPOSED"):
            for r in ROLES:
                v = self.view(key, r)
                table["available"][r] = len(v)
                if v and r in ("STATE", "PROCESS", "RELATION", "MEASURE", "CAUSE"):
                    c = v[0]
                    table["example"][r] = c.get("condition") or f"{c['if']} {c['bond']} {c['then']}"
        else:
            table["available"] = {d: 1}
            table["example"] = {d: e.get("run", {}).get("impl")}
        return table

    def reads_of(self, condition: str) -> list[str]:
        """The readings a condition names -- so a new atom's `reads` come from the condition it was
        formed from, not from anyone's list. `o1.colour_changed`, `contact(o1, o2)`,
        `board.completed`."""
        names = _re.findall(r"[A-Za-z_][A-Za-z_0-9]*", condition)
        return [n for n in dict.fromkeys(names) if n in self.readings]

    def candidates(self, key: str, o: str = "{o}", x: str = "{x}") -> list[dict]:
        """THE GENERATOR: an entry's candidate conditions, from its reads and the type family.
        Weighted reads come first. A PRIMITIVE has none here -- its callable is arc_atoms'."""
        e = self.get(key)
        if e is None or e.get("run", {}).get("route") not in ("GROUNDED", "COMPOSED"):
            return []
        # a molecule's views come from what its operands read (inherited, weight 0.5); it still RUNS
        # as a composition -- these candidates describe it, the junctions decide it
        w = e.get("reads_weight") or dict.fromkeys(
            e.get("reads", []), 1.0 if e["run"]["route"] == "GROUNDED" else 0.5
        )
        out = []
        for r in sorted(w, key=lambda r: -w[r]):
            spec = self.readings.get(r)
            if not spec:
                continue
            scope, typ = spec.get("scope"), spec["type"]
            if (
                scope == "context"
            ):  # action / press: a GUARD (When(P, R)); its state is "taken or not"
                fam = [("present", "frame.{r} > 0"), ("fails", "frame.{r} == 0")]
            elif r == "predicted":  # the prediction is read through its miss
                fam = [("holds", "{o}.residual == 0"), ("fails", "{o}.residual > 0")]
            elif scope == "pair" and typ == "DELTA":
                fam = [
                    ("up", "{r}({o}, {x}) > 0"),
                    ("down", "{r}({o}, {x}) < 0"),
                    ("moves", "{r}({o}, {x}) != 0"),
                ]
            elif scope == "pair" and typ != "PRED":
                fam = [("present", "{r}({o}, {x}) > 0"), ("absent", "{r}({o}, {x}) == 0")]
            elif scope == "board" and typ == "DELTA":
                fam = [
                    ("up", "board.{r} > 0"),
                    ("down", "board.{r} < 0"),
                    ("moves", "board.{r} != 0"),
                ]
            elif scope == "board":
                fam = [("present", "board.{r} > 0")]
            elif (
                scope == "operand"
            ):  # `prev` is offered to the binder as an operand, not tested here
                continue
            else:
                fam = TEMPLATES.get(typ, [])
            for label, t in fam:
                text = t.format(o=o, x=x, r=r)
                out.append(
                    {
                        "entry": key,
                        "reading": r,
                        "template": label,
                        "condition": text,
                        "weight": w[r],
                        "status": spec.get("status"),
                    }
                )
        return out

    # ---------------------------------------------------------------- the agent adds
    def invent_atom(
        self,
        name: str,
        condition: str,
        reads: list[str] | None = None,
        *,
        game: str,
        cycle: int,
        receipt: dict | None = None,
        affects: list[str] | None = None,
    ) -> str:
        """INVENTED: a NEW primitive the agent names (the name is arbitrary; its identity is the
        observed pattern), formed when it observed something it could not compose (receipt =
        the abstention receipt that licensed it). Enters RUNTIME, indexed now, standing earned."""
        reads = list(reads) if reads else self.reads_of(condition)
        if not reads:
            raise ValueError(
                "the condition names no reading -- an invented atom grounds in the floor"
            )
        bad = [r for r in reads if r not in self.readings]
        if bad:
            raise ValueError(
                f"reads {bad} are not readings -- an invented atom grounds in the floor"
            )
        key = f"AGENT-INVENTED|{name}"
        if self.get(key):
            raise ValueError(f"{key} exists; record ≡ instead of re-inventing")
        e = {
            "name": name,
            "domain": "AGENT-INVENTED",
            "kind": "PERCEPT",
            "origin": INVENTED,
            "born": {"game": game, "cycle": cycle, "receipt": receipt},
            "grid": {"meaning": None, "status": "agent", "lineage": f"invented from: {condition}"},
            "reads": reads,
            "reads_weight": dict.fromkeys(reads, 1.0),
            "affects": list(affects or []),
            "run": {
                "route": "GROUNDED",
                "lit_by": reads,
                "condition_text": condition,
                "held_as": "the agent's own condition; settled by the ground",
            },
            "standing": None,
        }
        self.runtime[key] = e
        self._index(key, e)
        e["roles"] = self.role_table(
            key
        )  # the same generic step the preloaded entries went through
        return key

    def mint_recipe(
        self, name: str, operands: list[str], junctions: list[str], *, game: str, cycle: int
    ) -> str:
        """MINTED: a new arrangement of EXISTING entries in the agent's grammar. Operands must
        resolve; each junction is a bond or UNKNOWN; one fewer junction than operands."""
        if len(junctions) != len(operands) - 1:
            raise ValueError("a recipe of k operands has k-1 junctions")
        for b in junctions:
            if b not in BONDS and b != UNKNOWN:
                raise ValueError(f"{b!r} is not a bond (Operators table)")
        missing = [o for o in operands if self.get(o) is None]
        if missing:
            raise ValueError(f"operands {missing} are not in the library -- invent them first")
        key = f"AGENT-MINTED|{name}"
        reads = list(dict.fromkeys(r for o in operands for r in self.get(o).get("reads", [])))
        e = {
            "name": name,
            "domain": "AGENT-MINTED",
            "kind": "COMPOSITE",
            "origin": MINTED,
            "born": {"game": game, "cycle": cycle},
            "ingredients": [{"ref": o} for o in operands],
            "reads": reads,
            "affects": [],
            "run": {
                "route": "COMPOSED",
                "operands": [{"ref": o} for o in operands],
                "junctions": list(junctions),
                "junction_source": "agent",
            },
            "standing": None,
        }
        self.runtime[key] = e
        self._index(key, e)
        e["roles"] = self.role_table(key)
        return key

    def carry(self, key: str, to_game: str) -> dict:
        """IMPORTED (Isaiah 2026-10-07: import means carrying across games). BIRTH is fixed;
        binding is
        re-decided at the destination. A condition naming a raw colour, position or size does NOT
        cross (Isaiah 2026-10-08: colours change every load; boards may be rearranged, rotated,
        shrunk): it stays in its episode, refused with its reason. What crosses is offered along
        either axis."""
        e = self.get(key)
        cond = (e.get("run") or {}).get("condition_text") or ""
        safe, why = (
            carry_check(cond, self.readings)
            if cond
            else (True, "no condition (seed text or composition)")
        )
        rec = {"to": to_game, "carried": safe, "why": why}
        if safe and cond:
            rec["forms"] = axis_forms(cond)
        e.setdefault("carried", []).append(rec)
        return rec

    def save_runtime(self) -> None:
        (self.root / "runtime.json").write_text(
            json.dumps(
                {
                    "meta": {"what": "agent-made and carried entries, this agent runtime"},
                    "entries": self.runtime,
                },
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
            newline="\n",
        )

    def _index(self, key: str, e: dict) -> None:
        if e.get("kind") != "COMPOSITE":
            for r in e.get("reads", []):
                self.by_reading[r].append((key, e.get("reads_weight", {}).get(r, 1.0)))
        for r in e.get("affects", []) or []:
            self.by_affects[r].append(key)
        for i in e.get("ingredients", []) or []:
            self.ingredient_of[i["ref"]].append(key)


def _abductive_checks(lib: Library) -> list[tuple[bool, str]]:
    """v7: the abductive lookup, as (passed, what) pairs. Run on the real library by the self-test,
    and again with the affects path REMOVED, where the first check must fail (the must-fail)."""
    out = []
    eff = {"colour_changed": 1}
    fwd = lib.light(eff)
    fk = [k for k, _ in fwd]
    prod = [k for k, _ in lib.produces(eff)]
    out.append(
        (
            "MEDICAL|Contagion" not in fk and "MEDICAL|Contagion" in prod,
            "a colour_changed residual: forward never lights Contagion, the abductive lookup does",
        )
    )
    out.append((fwd == lib.light(eff, abduce=False), "abduce=False IS the forward lookup"))
    aft, mer = lib.light(eff, abduce="after"), lib.light(eff, abduce="merged")
    out.append((aft[: len(fwd)] == fwd, '"after" keeps the forward list as its prefix, unchanged'))
    grounded = {k for k in prod if lib._grounded(k)}
    out.append(
        (
            {k for k, _ in aft} == {k for k, _ in mer} == set(fk) | grounded,
            "both modes return the same set, forward + grounded producers: NEVER EXCLUDE",
        )
    )
    out.append(
        (
            set(prod) == set(lib.by_affects["colour_changed"]),
            "produces returns every entry filed under the reading, molecules included",
        )
    )

    def rank(ctx):
        ks = [k for k, _ in lib.produces(eff, ctx)]
        return ks.index("MEDICAL|Contagion") if "MEDICAL|Contagion" in ks else len(ks)

    out.append(
        (
            rank({"touching", "contact"}) < rank(set()),
            "the description orders it: with touching and contact held, Contagion ranks higher",
        )
    )
    return out


def _selftest(root: str) -> int:
    import shutil
    import tempfile  # noqa: E401

    tmp = Path(tempfile.mkdtemp())
    for n in (
        "atoms.json",
        "molecules.json",
        "agent_atoms.json",
        "relations.json",
        "readings.json",
        "index.json",
    ):
        shutil.copy(Path(root) / n, tmp / n)
    lib = Library(tmp).load()
    fails = 0

    def check(c, msg):
        nonlocal fails
        print(("ok   " if c else "FAIL ") + msg)
        fails += not c

    lit = lib.light({"touching": 3, "gone": 1})
    keys = [k for k, _ in lit]
    check("HUMAN|Solidity" in keys[:200], "a touching change lights Solidity near the top")
    check(len(lit) > 0 and all(s > 0 for _, s in lit), "every lit entry carries a positive score")
    cands = lib.candidates("HUMAN|Solidity", "o1", "o2")
    check(
        any(c["reading"] == "touching" for c in cands),
        "Solidity's candidates include a touching condition",
    )
    check(all("{" not in c["condition"] for c in cands), "every candidate is fully instantiated")
    mols = lib.molecules_lit({"KINETIC|Contact", "HUMAN|Consumed"})
    check(
        any(m["key"] == "HUMAN|Erase" for m in mols),
        "Contact + Consumed lit -> Erase offered (Erase = Contact ? Consumed)",
    )
    k = lib.invent_atom(
        "blinker",
        "o.colour_changed == 1",
        ["colour_changed", "prev"],
        game="g1",
        cycle=7,
        receipt={"verdict": "budget_spent"},
    )
    check(
        any(kk == k for kk, _ in lib.light({"colour_changed": 1})),
        "an invented atom is lit by its own reading at once",
    )
    m = lib.mint_recipe("blink-then-move", [k, "HUMAN|Movement"], ["→"], game="g1", cycle=9)
    check(
        any(x["key"] == m for x in lib.molecules_lit({k, "HUMAN|Movement"})),
        "a minted recipe is offered when its operands light",
    )
    try:
        lib.mint_recipe("bad", ["HUMAN|Movement", "NOPE|x"], ["+"], game="g1", cycle=9)
        check(False, "an unresolvable operand is refused")
    except ValueError:
        check(True, "an unresolvable operand is refused")
    try:
        lib.invent_atom("bad", "o.x == 1", ["not_a_reading"], game="g1", cycle=1)
        check(False, "an invented atom over a non-reading is refused")
    except ValueError:
        check(True, "an invented atom over a non-reading is refused")
    st = lib.view("MEDICAL|Contagion", "STATE")
    pr = lib.view("MEDICAL|Contagion", "PROCESS")
    check(
        bool(st)
        and bool(pr)
        and {c["condition"] for c in st}.isdisjoint({c["condition"] for c in pr}),
        "one atom, two views: STATE and PROCESS candidates differ (effect / affect)",
    )
    # v7: THE ABDUCTIVE LOOKUP, with its must-fail (the affects path removed must be caught)
    for ok, what in _abductive_checks(lib):
        check(ok, what)
    saved = lib.by_affects
    lib.by_affects = defaultdict(list)
    caught = not all(ok for ok, _ in _abductive_checks(lib))
    lib.by_affects = saved
    check(caught, "MUST-FAIL: with the affects path removed, the abductive checks fail")
    try:
        lib.light({"colour_changed": 1}, abduce="sideways")
        check(False, "an unknown abduce mode is refused")
    except ValueError:
        check(True, "an unknown abduce mode is refused")
    ca = lib.view("MEDICAL|Contagion", "CAUSE")
    check(
        bool(ca) and all(c["bond"] == "⇒" and "if" in c and "then" in c for c in ca),
        "the CAUSE view is a production: if <state of o> then <change of x>",
    )
    lp = lib.get("MEDICAL|Contagion spread")
    check(
        lp is None or (lp.get("role_of") or {}).get("role") == "PROCESS",
        "a held pair is re-expressed as base + role (Contagion spread = Contagion, PROCESS)",
    )
    try:
        lib.view("HUMAN|Solidity", "NOT_A_ROLE")
        check(False, "an unknown role is refused")
    except ValueError:
        check(True, "an unknown role is refused")
    k2 = lib.invent_atom(
        "spreader", "touching(o1, o2) == 1", game="g1", cycle=11, affects=["colour_changed"]
    )
    check(
        k2 in [kk for kk, _ in lib.produces({"colour_changed": 1})],
        "an invented atom is reached by what it produces at once (runtime indexed both ways)",
    )
    t = lib.get(k2)["roles"]
    check(
        lib.get(k2)["reads"] == ["touching"], "a new atom's reads are parsed from its own condition"
    )
    check(
        t["default"] == "PROCESS"
        and t["available"].get("STATE")
        and t["available"].get("PROCESS")
        and t["available"].get("CAUSE"),
        "a new atom gets the full role table automatically (state, process, cause ...)",
    )
    k3 = lib.invent_atom("red-thing", "o1.colour == 3", game="g1", cycle=12)
    r3 = lib.carry(k3, "g2")
    check(
        not r3["carried"],
        "a rule naming a raw colour does not cross games (colours change every load)",
    )
    k4 = lib.invent_atom("falls-onto", "o1.drow > 0", game="g1", cycle=13)
    r4 = lib.carry(k4, "g2")
    check(
        r4["carried"] and "o1.dcol > 0" in r4["forms"],
        "a relational rule crosses, offered along either axis (a rotated board)",
    )
    check(
        all(
            carry_check(c["condition"], lib.readings)[0]
            for k in ("HUMAN|Solidity", "MEDICAL|Contagion")
            for c in lib.candidates(k, "o1", "o2")
        ),
        "every generated candidate is value-free, so it can cross",
    )
    lib.save_runtime()
    lib2 = Library(tmp).load()
    check(
        lib2.get(k) is not None and lib2.get(m) is not None,
        "runtime survives save/load; seed untouched",
    )
    check(
        lib2.seed["HUMAN|Solidity"]["origin"] == PRIOR and lib2.get(k)["origin"] == INVENTED,
        "origins kept apart",
    )

    # v6: THE ROLES ARE DIFFERENT VIEWS (the seat's census found two identical triples)
    def sig(k, r):
        return sorted(
            str((c.get("condition"), c.get("if"), c.get("then"), c.get("quantifier")))
            for c in lib.view(k, r)
        )

    sample = [k for k in ("MEDICAL|Contagion", "HUMAN|Solidity", "KINETIC|Contact") if lib.get(k)]
    for a, b in (
        ("STATE", "TEST"),
        ("STATE", "RULE"),
        ("TEST", "RULE"),
        ("CAUSE", "RESULT"),
        ("CAUSE", "AGENT"),
        ("RESULT", "AGENT"),
        ("RELATION", "MEASURE"),
    ):
        check(any(sig(k, a) != sig(k, b) for k in sample), f"the {a} and {b} views differ")
    rv = lib.view("MEDICAL|Contagion", "RESULT")
    changes = {c["condition"] for c in lib.view("MEDICAL|Contagion", "PROCESS")}
    states = {c["condition"] for c in lib.view("MEDICAL|Contagion", "STATE")}
    check(
        bool(rv) and all(c["if"] in changes and c["then"] in states for c in rv),
        "RESULT reads a change first, then the state it ends in",
    )
    pv = [c["condition"] for c in lib.view("MEDICAL|Contagion", "PROCESS")]
    check(len(pv) == len(set(pv)), "a view lists each condition once")
    check(
        all(c["if"].startswith("action(agent,") for c in lib.view("MEDICAL|Contagion", "AGENT")),
        "AGENT's condition is the agent's own action",
    )
    # v5: THE AGENT'S OWN REACH (inherited.py reads agent_atoms.json + tag_index.json, nothing else)
    R = json.loads((Path(root) / "readings.json").read_text(encoding="utf-8"))["readings"]
    AG = json.loads((Path(root) / "agent_atoms.json").read_text(encoding="utf-8"))["atoms"]
    held = set(json.loads((Path(root) / "atoms.json").read_text(encoding="utf-8"))["atoms"]) | set(
        json.loads((Path(root) / "molecules.json").read_text(encoding="utf-8"))["molecules"]
    )
    TI = json.loads((Path(root) / "tag_index.json").read_text(encoding="utf-8"))
    named = (
        {k for d in TI["by_tag"].values() for v in d.values() for k in v}
        | {k for d in TI["by_pair"].values() for v in d.values() for k in v}
        | {k for v in TI["by_attribute"].values() for k in v}
    )
    check(
        not (named - held),
        f"tag_index.json names only entries the library holds ({len(named - held)} dangling)",
    )
    ext = {k: e for k, e in AG.items() if e.get("form") == "EXTRACT"}
    check(
        all(
            R.get(e.get("reading"), {}).get("code", {}).get("extract_atom") == k
            for k, e in ext.items()
        ),
        "every EXTRACT agent atom names a reading that points back to it",
    )
    check(
        all(f"AGENT|{r}" in ext for r, rd in R.items() if rd.get("code")),
        "every reading the code extracts is an atom in agent_atoms.json (the agent can reach it)",
    )
    check(
        all(e.get("reach_tier") == 0 and "primary" in (e.get("tags") or {}) for e in AG.values()),
        "every agent atom carries reach_tier 0 and its tags (inherited.py keys reach on them)",
    )
    shutil.rmtree(tmp)
    print(f"{fails} failure(s)")
    return fails


if __name__ == "__main__":
    import sys

    raise SystemExit(_selftest(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent)))
