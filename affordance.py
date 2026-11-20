"""AFFORDANCE BET (TETHER_AFFORDANCE, default ON; Isaiah 2026-11-16 "it's a ball (shaped like a
ball, acts like a ball) ... balls can roll, does this roll?"; write-up 40, "Affordances: shape ->
concept -> properties -> predictions"; lead 16:20 "circle -> ball, that 2d-3d or abstraction").

  PRIOR    an object of a kind new this run, whose perception reads a shape_name that resolves to
           a concept (word_map's shape_bridge shape_name -> form -> first object concept, else
           arc_percept.SHAPE_ATOMS shape_name -> atom names, else the shape_name itself), gets ONE
           affordance_prior row per (kind, property): the chain, the predicted reading and the
           prior's stamp (C6). It carries NO standing: a prior is a bet, never a credit.
           A prior predicts 'moves' when its verb is verb.motion, or (TETHER_CONTACT_MOVES)
           when word_map marks it moves_object: its sense's WordNet '@' chain reaches
           verb.motion (throw -> propel -> move), the chain carried as moves_via.
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

 RECOGNISED (TETHER_RECOGNISED, default ON; write-up 42 handoff item 4, "Recognition into the
agent"): when an observation carries a PICTURE -- an env attribute or an observation field named in
PICTURE_NAMES holding an image array, board-wide ('picture') or per object ('o1.picture') -- the
picture is recognised once per (holder, picture): recognize.recognise_shape over the repo-relative
shape memory, and recognize.recognise when a class memory is LOADED under the dir named by the
plain env var RDL_RECOGNITION_DIR (default: the shipped generated shapes; no absolute path). The
ImageNet class memory is OPTIONAL (Isaiah 2026-11-20): it activates only when a memory has been
built and loads, with parquet data detected via the plain env var IMAGENET_PARQUET_DIR. ONE state
row is legible from the ledger alone -- class_memory_active (with the class count) when loaded,
else recognised_inert naming the exact reason (no data / parquet not found / not built / load
failed) -- so the route is never silently dropped on Kaggle and never requires committed data.
Each live route writes one `recognised` row {class, synset, dim,
grid_shape_name, bridge, route, votes/distance, margin, abstained, stamp}; a class that did not
abstain is then read by the PRIOR step exactly as a shape_name is (class -> concept through the
word map's shape_bridge; else the class's grid shape name; else its own bridge's 2D names). Grid
boards carry no picture: one recognised_inert row per run. recognize (and with it cv2) is imported
lazily, inside the call, never at module level.
"""
from __future__ import annotations

import functools
import hashlib
import json
import os
from pathlib import Path

import armflag

_ON = armflag.arm("TETHER_AFFORDANCE", default=True)  # prior/settle/refuse rows; record only
# write-up 42 item 4: a picture's recognised class read like a shape_name; inert on grid boards
_RECOGNISED = armflag.arm("TETHER_RECOGNISED", default=True)
# the field / attribute names a picture is read from. Declared convention, Fig 10: visible, movable
PICTURE_NAMES = ("picture", "image")
# a picture is a uint8 array at least this many pixels on each side. Declared convention, Fig 10
PICTURE_MIN_SIDE = 16
# The class memory (local ImageNet terms: never in the repository). The PLAIN env var
# RDL_RECOGNITION_DIR (NOT a TETHER_ arm -- the arms seat forbids raw TETHER_ reads) names the
# local dir; absent, the default is the repo's shipped generated shape memory, so recognition
# still runs on Kaggle with no absolute path in the code. Absent dir -> shape route only, and
# the class-memory route says WHY it is inert rather than dropping silently (AKAZE 2026-11-16).
_SHIPPED_CLASS_MEMORY = Path(__file__).resolve().parent / "library" / "shapes" / "memory"
CLASS_MEMORY_DIR = Path(os.environ.get("RDL_RECOGNITION_DIR") or str(_SHIPPED_CLASS_MEMORY))
_CLASS_MEMORY: dict = {}
WORD_MAP = Path(__file__).resolve().parent / "library" / "word_map.json"
# a verb's WordNet lexname -> the reading it predicts (a means: what to LOOK at, never the answer)
LEXNAME_READING = {"verb.motion": "moves"}
# a contact verb on an object predicts it moves when WordNet's own '@' chain makes the sense a
# cause-to-move verb (throw -> propel -> move): word_map's prior.moves_object, record only
_CONTACT_MOVES = armflag.arm("TETHER_CONTACT_MOVES", default=True)
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
                   **({"moves_object": a["moves_object"], "moves_via": a.get("moves_via")}
                      if "moves_object" in a else {}),
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
    """The reading predictions a prior makes: its own 'reading'/'property' field, else by lexname,
    else 'moves' when the prior's moves_object is True (TETHER_CONTACT_MOVES: its verb sense's
    WordNet hypernym chain reaches verb.motion); 'keeps moving' implies 'moves'."""
    r = prior.get("reading") or prior.get("property") or LEXNAME_READING.get(
        str(prior.get("verb_lexname") or ""))
    if not r and _CONTACT_MOVES and prior.get("moves_object") is True:
        r = "moves"
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
                       **({"moves_via": p["moves_via"]} if prop == "moves" and p.get("moves_via")
                          and p.get("moves_object") is True and not LEXNAME_READING.get(
                              str(p.get("verb_lexname") or "")) else {}),
                       "stamp": _stamp(p),
                       **{k: list(p[k]) for k in ("found_in", "relations") if k in p},
                       "except_when": [], "name_now": chain["concept"]}
                if chain.get("recognised"):           # TETHER_RECOGNISED: the picture's class
                    rec["recognised"] = chain["recognised"]
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


# ---- TETHER_RECOGNISED (write-up 42 handoff item 4): a picture's class, read like a shape_name
def is_picture(v) -> bool:
    """An image array: uint8, 2D (grey) or 3D with 1, 3 or 4 channels, each side no smaller
    than PICTURE_MIN_SIDE.
    Read by attributes only, so numpy is not imported here."""
    nd, sh, dt = getattr(v, "ndim", None), getattr(v, "shape", None), getattr(v, "dtype", None)
    if nd not in (2, 3) or sh is None or str(dt) != "uint8":
        return False
    if nd == 3 and sh[2] not in (1, 3, 4):
        return False
    return min(sh[0], sh[1]) >= PICTURE_MIN_SIDE


def pictures(env, obs: dict) -> dict:
    """{holder: image}: '@picture' for a board-wide field or env attribute named in PICTURE_NAMES,
    the object's id for an '<object>.<name>' field. {} on a board that carries no picture."""
    out: dict = {}
    for n in PICTURE_NAMES:
        v = obs.get(n) if isinstance(obs, dict) else None
        if v is None:
            v = getattr(env, n, None)
        if is_picture(v):
            out.setdefault("@picture", v)
    for k, v in (obs.items() if isinstance(obs, dict) else ()):
        if "." in k and k.split(".", 1)[1] in PICTURE_NAMES and is_picture(v):
            out.setdefault(k.split(".", 1)[0], v)
    return out


def picture_sha(img) -> str:
    return hashlib.sha256(img.tobytes()).hexdigest()[:16]


def _bgr(img):
    """The recognisers read BGR: grey and one-channel pictures are widened, alpha dropped."""
    import numpy as np  # lazy: only when a picture is present
    a = np.ascontiguousarray(img)
    if a.ndim == 2:
        return np.repeat(a[:, :, None], 3, axis=2)
    if a.shape[2] == 1:
        return np.repeat(a, 3, axis=2)
    return np.ascontiguousarray(a[:, :, :3])


def _num(x):
    """JSON-safe: an infinite margin (one candidate class) is written as None."""
    try:
        return None if x is None or x != x or abs(x) == float("inf") else x
    except TypeError:
        return x


def class_memory_dir() -> Path:
    """The configured class-memory dir, resolved at call time so a Kaggle env var is honoured
    even though this module was imported before the environment was finalised."""
    raw = os.environ.get("RDL_RECOGNITION_DIR")
    return Path(raw) if raw else CLASS_MEMORY_DIR


def class_memory_status(cm_dir: Path | None = None) -> dict:
    """The detector's status for the configured class-memory dir. Lazy import (cv2 stays out of
    the module), no side effects, no large reads -- see recognize.class_memory_status."""
    import recognize  # lazy: recognize imports cv2 only inside its calls

    return recognize.class_memory_status(Path(cm_dir) if cm_dir is not None else class_memory_dir())


def _class_memory_why(path: Path) -> str | None:
    """Why the class-memory route is inert at `path`, or None when a memory is loaded there.
    Derived from the detector so the inert row and the detector cannot disagree: a missing dir
    used to drop the route with no row at all; name the exact reason so the zero is visible."""
    st = class_memory_status(path)
    return None if st["active"] else st["reason"]


def _class_memory(path: Path):
    """The local class memory, loaded once per process; None when absent."""
    key = str(path)
    if key not in _CLASS_MEMORY:
        mem = None
        if (path / "memory.json").exists() and (path / "memory.npz").exists():
            import recognize  # lazy: recognize imports cv2 only inside its calls
            mem = recognize.load(path / "memory")
        _CLASS_MEMORY[key] = mem
    return _CLASS_MEMORY[key]


def recognise_rows(img, class_dir: Path | None = None) -> tuple:
    """(rows, why_inert, class_memory_why, class_memory_status). One `recognised` detail per route:
    the preloaded shape memory always, the class memory when it is LOADED (detector says active).
    why_inert names the failure when no route could run (cv2 or the shape memory absent);
    class_memory_why is None when active, else the detector's exact reason; class_memory_status is
    the full detector dict so the caller can write ONE legible state row -- class_memory_active
    (with the class count) or recognised_inert (the precise reason). A route's own abstention is a
    row, never an inert."""
    try:
        import recognize  # lazy: never at module level (cv2 stays unimported)
        pic = _bgr(img)
        mem = recognize.load_shapes()
        r = recognize.recognise_shape(pic, mem)
    except Exception as e:              # noqa: BLE001  cv2 or the shape memory absent: inert
        return [], f"recognition unavailable: {type(e).__name__}: {e}", None, None
    cls = r.get("class")
    meta = (mem.get("meta") or {}).get(cls) or {}
    st = dict(mem["akaze"].stamp or {})
    stamp = {"stage": (meta.get("stamp") or {}).get("stage") or st.get("stage"),
             "source": st.get("source"), "memory": "library/shapes/memory",
             **{k: st[k] for k in ("akaze_sha", "hu_sha") if k in st}}
    rows = [{"class": cls, "synset": meta.get("wordnet_synset"), "dim": r.get("dim"),
             "grid_shape_name": r.get("grid_shape_name"), "bridge": r.get("bridge"),
             "route": r.get("route") or "shape", "distance": _num(r.get("distance")),
             "votes": None, "inliers": (r.get("akaze") or {}).get("inliers"),
             "margin": _num(r.get("margin")), "abstained": bool(r.get("abstained")),
             "candidate": (r.get("akaze") or {}).get("candidate"), "corners": r.get("corners"),
             "reason": r.get("reason"), "memory": "shapes", "stamp": stamp, "standing": None}]
    cm_dir = Path(class_dir) if class_dir else class_memory_dir()
    st = class_memory_status(cm_dir)
    cm_why = None if st["active"] else st["reason"]
    if st["active"]:
        try:
            cm = _class_memory(cm_dir)
            if cm is not None:
                c = recognize.recognise(pic, cm)
                cst = dict(c.get("stamp") or {})
                rows.append({"class": c.get("class"), "synset": c.get("synset"), "dim": None,
                             "grid_shape_name": None, "bridge": None, "route": "class_memory",
                             "distance": None, "votes": c.get("votes"), "inliers": c.get("inliers"),
                             "margin": _num(c.get("margin")), "abstained": bool(c.get("abstained")),
                             "candidate": c.get("candidate"), "reason": c.get("reason"),
                             "memory": "class_memory",
                             "stamp": {k: cst.get(k) for k in ("stage", "source", "sha")},
                             "standing": None})
        except Exception as e:          # noqa: BLE001  present but unreadable: said, not hidden
            rows.append({"class": None, "route": "class_memory", "abstained": True,
                         "reason": f"class memory unreadable: {type(e).__name__}: {e}",
                         "memory": "class_memory", "stamp": None, "standing": None})
            cm_why = f"class memory load failed at {cm_dir}: {type(e).__name__}: {e}"
            st = dict(st, active=False, event="recognised_inert", reason=cm_why)
    return rows, None, cm_why, st


def resolve_recognised(row: dict, atoms: dict | None, bridge: list | None,
                       priors: list) -> dict | None:
    """A recognised class read exactly as a shape_name: the class itself, then its grid shape
    name, then its own bridge's 2D names (a sphere is read through circle); the first that
    resolves to a concept. The chain carries the class as 'recognised'."""
    if not row or row.get("abstained") or not row.get("class"):
        return None
    names = [row["class"], row.get("grid_shape_name")]
    names += [_name(x) for x in ((row.get("bridge") or {}).get("shape_2d") or ())]
    seen: list = []
    for n in names:
        if not n or n in seen:
            continue
        seen.append(n)
        chain = resolve(n, atoms, bridge, priors)
        if chain is not None:
            return dict(chain, recognised=row["class"])
    return None
