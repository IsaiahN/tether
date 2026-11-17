"""AFFORDANCE BET (TETHER_AFFORDANCE, default ON; Isaiah 2026-11-16 "it's a ball (shaped like a
ball, acts like a ball) ... balls can roll, does this roll?"; write-up 40, "Affordances: shape ->
concept -> properties -> predictions"; lead 16:20 "circle -> ball, that 2d-3d or abstraction").

  PRIOR    an object of a kind new this run, whose perception reads a shape_name that resolves to
           a concept (word_map's shape_bridge shape_name -> form -> first object concept, else
           arc_percept.SHAPE_ATOMS shape_name -> atom names, else the shape_name itself), gets ONE
           affordance_prior row per (kind, property): the chain, the predicted reading and the
           prior's stamp (C6). It carries NO standing: a prior is a bet, never a credit.
  JUDGE    the first press that touches a member of that kind (C2's kind touch, felt in perceive)
           compares the prediction with the board:
             moves         the object's position readings changed on the step after the press
             keeps moving  they changed again on the next step with no new press landing on it
           matched -> affordance_settle ("it is a ball": earned only by acting like one);
           not     -> affordance_refuse with the CONDITION read (contact / the object's own
           contact context at press time): the prior is KEPT and its record gains "except when
           <condition>" (a list per kind and property); the concept drops back to the shape name
           for this kind. Nothing is deleted.
  RECORD   it never moves an action choice: rows and per-kind counts {held, settled, refused,
           exceptions} only.
  SOURCES  read lazily; absent -> inert, one affordance_inert row saying why.
  CN       (TETHER_RELATIONS_READ, default ON; write-up 42 handoff item 5) the prior lookup merges
           the concept's ConceptNet verbs (library/relations.json concept_actions_cn: CapableOf /
           ReceivesAction / UsedFor, with VerbNet classes) beside the word map's. Each merged prior
           keeps its own source and stamp and has standing none; a verb found in BOTH sources
           ranks first (found_in lists them). A ConceptNet verb predicts a reading only through
           the declared CN_READING table, and only for an OBJECT concept (library/
           vocabulary.json: a noun lexname in OBJECT_LEXNAMES). A concept absent from
           relations.json is unchanged. OFF: word-map-only, as before.
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

import armflag

_ON = armflag.arm("TETHER_AFFORDANCE", default=True)  # prior/settle/refuse rows; record only
WORD_MAP = Path(__file__).resolve().parent / "library" / "word_map.json"
# a verb's WordNet lexname -> the reading it predicts (a means: what to LOOK at, never the answer)
LEXNAME_READING = {"verb.motion": "moves"}
KEEPS = "keeps moving"
# B7 motion words (write-up 42 "the ball rolls to the right"); record only
_MOTION_UPPER = armflag.arm("TETHER_MOTION_WORDS", default=True)
_ROW, _COL = ("row", "r", "cy", "y"), ("col", "c", "cx", "x")
# write-up 42 handoff item 5: ConceptNet verbs beside the word map's in a concept's prior lookup
_RELATIONS_READ = armflag.arm("TETHER_RELATIONS_READ", default=True)  # merged priors; record only
RELATIONS = Path(__file__).resolve().parent / "library" / "relations.json"
VOCABULARY = Path(__file__).resolve().parent / "library" / "vocabulary.json"
# (ConceptNet relation, verb) -> the reading it predicts for an OBJECT concept. A declared table
# (Fig 10: a convention, visible and movable), a means of what to LOOK at, never an answer: what
# a thing can do by itself (CapableOf) or what is done to it that displaces it (ReceivesAction).
# UsedFor is not in it: what a thing is for says what an actor does with it, not that it moves.
CN_READING = {
    ("CapableOf", "roll"): "moves",
    ("CapableOf", "bounce"): "moves",
    ("CapableOf", "move"): "moves",
    ("CapableOf", "slide"): "moves",
    ("CapableOf", "fall"): "moves",
    ("ReceivesAction", "push"): "moves",
    ("ReceivesAction", "kick"): "moves",
    ("ReceivesAction", "throw"): "moves",
}
# the noun lexnames that make a concept an OBJECT: word_map.json header category_map -> "object"
# (tests/test_relations_read.py checks the two agree)
OBJECT_LEXNAMES = frozenset(("noun.animal", "noun.artifact", "noun.body", "noun.food",
                             "noun.object", "noun.person", "noun.plant", "noun.possession",
                             "noun.substance"))
CN_SOURCE = "conceptnet"
WM_SOURCE = "word_map"


def direction(before: dict, after: dict, obj: str) -> str | None:
    """The sign of the object's own (drow, dcol) at the press: right/left/up/down/up-right ...
    (grid rows grow downward). None when no position reading moved."""
    def d(names):
        for n in names:
            a, b = before.get(f"{obj}.{n}"), after.get(f"{obj}.{n}")
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return (b > a) - (b < a)
        return 0
    dr, dc = d(_ROW), d(_COL)
    v = {-1: "up", 1: "down"}.get(dr, "")
    h = {-1: "left", 1: "right"}.get(dc, "")
    return "-".join(x for x in (v, h) if x) or None


def manner(keeps: bool, verbs) -> str:
    """The concept's expectation confirmed by the object's own motion: it kept moving with no new
    press -> 'rolls' if the concept's actions include roll, else 'glides'; only on the press ->
    'is pushed'."""
    if not keeps:
        return "is pushed"
    return "rolls" if any(str(v or "").split()[:1] == ["roll"] for v in verbs) else "glides"


def _priors_of(wm: dict) -> list:
    """word_map's affordance priors: {concept, action_verb, verb_lexname, source, stamp, ...}."""
    for k in ("priors", "affordance priors", "affordance_priors"):
        v = wm.get(k)
        if isinstance(v, list):
            return [p for p in v if isinstance(p, dict) and p.get("concept")]
    return []


def _name(x) -> str | None:
    return x if isinstance(x, str) else (x or {}).get("name") if isinstance(x, dict) else None


@functools.cache
def _read(path: str) -> dict:
    """The word map, read once per process (it is large); {} when absent or unreadable."""
    try:
        p = Path(path)
        return (json.loads(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    except Exception:                   # noqa: BLE001
        return {}


@functools.cache
def cn_sources(rel_path: str | None = None, vocab_path: str | None = None) -> tuple:
    """(concept_actions_cn, noun lexnames by lemma, the ConceptNet stamp), read once per process
    and only the parts the lookup uses; ({}, {}, None) when absent or unreadable. Never raises."""
    def load(p):
        try:
            p = Path(p)
            return (json.loads(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
        except Exception:                   # noqa: BLE001
            return {}
    rel = load(rel_path or RELATIONS)
    acts = rel.get("concept_actions_cn") if isinstance(rel, dict) else None
    if not isinstance(acts, dict) or not acts:
        return {}, {}, None
    src = ((rel.get("header") or {}).get("sources") or {}).get("conceptnet") or {}
    stamp = {"corpus": "conceptnet-5.7", "sha": str(src.get("sha256") or "")[:16],
             "stage": "regularity"}
    voc = load(vocab_path or VOCABULARY)
    voc = voc.get("vocabulary") if isinstance(voc, dict) else None
    nouns = {w: e["n"] for w, e in (voc or {}).items() if isinstance(e, dict) and e.get("n")}
    return acts, nouns, stamp


def cn_key(concept) -> str:
    """A concept name as a ConceptNet/WordNet lemma: the text after the last '|' or ':' (the
    library's 'DOMAIN|Name', 'bridge:ball', 'imagenet:417:balloon'), lower case, '_' for space."""
    s = str(concept or "")
    for sep in ("|", ":"):
        s = s.rsplit(sep, 1)[-1]
    return s.strip().lower().replace(" ", "_")


def _vkey(p: dict) -> str:
    return str(p.get("action_verb") or "").strip().lower().replace(" ", "_")


def merge(concept, wm_priors, cn: tuple | None = None) -> list:
    """The concept's priors: the word map's beside ConceptNet's (TETHER_RELATIONS_READ). Each keeps
    its own source and stamp, standing none; found_in names the sources the verb was found in, and
    a verb in both ranks first (stable within a rank, the word map's first). A ConceptNet verb
    predicts a reading only through CN_READING, and only when the concept is an object. Arm OFF,
    or the concept absent from relations.json: the word map's list unchanged."""
    wm_priors = list(wm_priors or ())
    if not _RELATIONS_READ:
        return wm_priors
    acts, nouns, stamp = cn if cn is not None else cn_sources()
    key = cn_key(concept)
    got = (acts or {}).get(key)
    if not isinstance(got, dict) or not got:
        return wm_priors
    is_obj = bool(set((nouns or {}).get(key) or ()) & OBJECT_LEXNAMES)
    wm_verbs = {_vkey(p) for p in wm_priors}
    out = [dict(p, found_in=[WM_SOURCE, CN_SOURCE] if _vkey(p) in got else [WM_SOURCE])
           for p in wm_priors]
    for v in sorted(got):
        a = got[v] if isinstance(got[v], dict) else {}
        rels = list(a.get("relations") or ())
        row = {"concept": concept, "action_verb": v.replace("_", " "), "relations": rels,
               "verbnet": list(a.get("vn") or ()), "source": CN_SOURCE, "stamp": stamp,
               "standing": "none",
               "found_in": [WM_SOURCE, CN_SOURCE] if v in wm_verbs else [CN_SOURCE]}
        r = next((CN_READING[(rl, v)] for rl in rels if (rl, v) in CN_READING), None)
        if r and is_obj:
            row["reading"] = r
        out.append(row)
    out.sort(key=lambda p: -len(p["found_in"]))
    return out


def load_sources(word_map: Path | None = None) -> tuple:
    """(shape_atoms or None, bridge rows or None, priors list, why-inert or None). Never raises."""
    atoms = None
    try:
        import arc_percept
        atoms = getattr(arc_percept, "SHAPE_ATOMS", None)
    except Exception:                   # noqa: BLE001  absent perception table: inert part
        atoms = None
    p = word_map or WORD_MAP
    wm = _read(str(p))
    wm = wm if isinstance(wm, dict) else {}
    bridge = wm.get("shape_bridge") if isinstance(wm.get("shape_bridge"), list) else None
    priors = _priors_of(wm)
    why = None
    if not priors and not bridge:
        why = (f"no affordance priors and no shape_bridge: {p.name} absent or carries none "
               "(wip/word-map not landed)")
    return atoms, bridge, priors, why


def shape_name_of(v) -> str | None:
    """A shape_name reading as its name: a string as is; an int as the index into
    arc_percept.SHAPE_NAMES (wip/shape-names publishes the index); else None."""
    if isinstance(v, str):
        return v
    if isinstance(v, int) and not isinstance(v, bool):
        try:
            import arc_percept
            names = getattr(arc_percept, "SHAPE_NAMES", None)
        except Exception:               # noqa: BLE001
            names = None
        if names and 0 <= v < len(names):
            return str(names[v])
    return None


def _bridge_chain(shape_name: str, bridge: list | None) -> dict | None:
    """shape_2d -> form_3d -> the first object concept whose actions predict a reading."""
    for row in bridge or ():
        if not isinstance(row, dict) or shape_name not in {
                _name(x) for x in (row.get("shape_2d") or ())}:
            continue
        forms = [n for n in map(_name, row.get("form_3d") or ()) if n]
        for ob in row.get("objects") or ():
            c = _name(ob)
            acts = (ob.get("actions") if isinstance(ob, dict) else None) or ()
            ps = [{"concept": c, "action_verb": a.get("verb"),
                   "verb_lexname": a.get("verb_lexname"), "source": a.get("source"),
                   "stamp": row.get("stamp"),
                   **({"reading": a["reading"]} if a.get("reading") else {})}
                  for a in acts if isinstance(a, dict)]
            ps = merge(c, ps) if c else ps      # TETHER_RELATIONS_READ: ConceptNet beside
            if c and any(readings(p_) for p_ in ps):
                return {"shape_name": shape_name, "form": forms[0] if forms else None,
                        "concept": c, "via": "shape_bridge", "priors": ps}
    return None


def resolve(shape_name: str, atoms: dict | None, bridge: list | None, priors: list) -> dict | None:
    """The chain for a shape_name: {shape_name, form, concept, via, priors[...]}, or None. The
    bridge first (2D -> 3D -> object, lead 16:20), else SHAPE_ATOMS' atoms, else the shape name,
    each looked up in word_map's priors (and, TETHER_RELATIONS_READ, ConceptNet's verbs beside
    them: merge); a concept counts only if a prior predicts a reading."""
    got = _bridge_chain(shape_name, bridge)
    if got is not None:
        return got
    by_c: dict = {}
    for p in priors:
        by_c.setdefault(str(p["concept"]), []).append(p)
    cands = [("SHAPE_ATOMS", a) for a in ((atoms or {}).get(shape_name) or ())]
    cands.append(("shape_name", shape_name))
    for via, c in cands:
        ps = merge(c, by_c.get(c) or [])        # TETHER_RELATIONS_READ: ConceptNet beside
        if any(readings(p_) for p_ in ps):
            return {"shape_name": shape_name, "form": None, "concept": c, "via": via,
                    "priors": ps}
    return None


def readings(prior: dict) -> list:
    """The reading predictions a prior makes: its own 'reading'/'property' field, else by lexname;
    'keeps moving' implies 'moves'."""
    r = prior.get("reading") or prior.get("property") or LEXNAME_READING.get(
        str(prior.get("verb_lexname") or ""))
    if not r:
        return []
    return ["moves", KEEPS] if r == KEEPS else [str(r)]


def _stamp(p: dict) -> dict:
    """C6: where the prior came from and at what stage -- never a standing."""
    st = p.get("stamp")
    out = {"source": p.get("source"),
           "stage": st.get("stage") if isinstance(st, dict) else st}
    if isinstance(st, dict):
        out.update({k: st[k] for k in ("corpus", "sha") if k in st})
    return out


class Book:
    """Per-run record: priors per (kind, property), exceptions, counts. Decides nothing."""

    def __init__(self) -> None:
        self.seen: set = set()          # kinds offered (or found to carry no concept)
        self.prior: dict = {}           # (kind, property) -> the prior record
        self.counts: dict = {}          # kind -> {held, settled, refused, exceptions}
        self.judged: set = set()        # (kind, property) judged by its first press
        self.pending: dict = {}         # kind -> keeps-moving test waiting a step
        self.inert_said = False
        self.before: dict = {}          # B7: the state read before the press (direction)
        self.verbs: dict = {}           # B7: kind -> the concept's action verbs (manner)
        self.dirn: dict = {}            # B7: kind -> the direction read at its press

    def _c(self, kind: str) -> dict:
        return self.counts.setdefault(kind, {"held": 0, "settled": 0, "refused": 0,
                                             "exceptions": 0})

    def offer(self, kind: str, obj: str, chain: dict) -> list:
        """affordance_prior details (one per property) for a kind new this run."""
        if kind in self.seen:
            return []
        self.seen.add(kind)
        self.verbs[kind] = [p.get("action_verb") for p in chain["priors"]]
        out = []
        for p in chain["priors"]:
            for prop in readings(p):
                if (kind, prop) in self.prior:
                    continue
                rec = {"kind": kind, "object": obj, "shape_name": chain["shape_name"],
                       "form": chain["form"], "concept": chain["concept"], "via": chain["via"],
                       "property": prop, "action_verb": p.get("action_verb"),
                       "verb_lexname": p.get("verb_lexname"),
                       "stamp": _stamp(p),
                       **{k: list(p[k]) for k in ("found_in", "relations") if k in p},
                       "except_when": [], "name_now": chain["concept"]}
                self.prior[(kind, prop)] = rec
                self._c(kind)["held"] += 1
                out.append(dict(rec, except_when=[]))
        return out

    def judge(self, kind: str, obj: str, prop: str, happened: bool, condition: str,
              motion: dict | None = None) -> tuple:
        """(event, detail) for the first test of (kind, prop), or (None, None). motion (B7):
        {direction, manner} added to a settle row when TETHER_MOTION_WORDS is on."""
        rec = self.prior.get((kind, prop))
        if rec is None or (kind, prop) in self.judged:
            return None, None
        self.judged.add((kind, prop))
        c = self._c(kind)
        if happened:
            c["settled"] += 1
            rec["name_now"] = rec["concept"]
            mo = motion if _MOTION_UPPER and motion else {}
            return "affordance_settle", dict(rec, object=obj, happened=True,
                                             except_when=list(rec["except_when"]),
                                             counts=dict(c), **mo)
        rec["except_when"].append(condition)      # the split: the prior kept, an exception added
        c["refused"] += 1
        c["exceptions"] += 1
        rec["name_now"] = rec["shape_name"]       # a name that stops paying drops to the shape
        mo = motion if _MOTION_UPPER and motion else {}
        return "affordance_refuse", dict(rec, object=obj, happened=False, condition=condition,
                                         except_when=list(rec["except_when"]), counts=dict(c),
                                         **mo)
