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

RECOGNISED (TETHER_RECOGNISED, default ON; write-up 42 handoff item 4, "Recognition into the
agent"): when an observation carries a PICTURE -- an env attribute or an observation field named in
PICTURE_NAMES holding an image array, board-wide ('picture') or per object ('o1.picture') -- the
picture is recognised once per (holder, picture): recognize.recognise_shape over the preloaded shape
memory, and recognize.recognise when a class memory is present under CLASS_MEMORY_DIR. Each route
writes one `recognised` row {class, synset, dim, grid_shape_name, bridge, route, votes/distance,
margin, abstained, stamp}; a class that did not abstain is then read by the PRIOR step exactly as a
shape_name is (class -> concept through the word map's shape_bridge; else the class's grid shape
name; else its own bridge's 2D names). Grid boards carry no picture: one recognised_inert row per
run. recognize (and with it cv2) is imported lazily, inside the call, never at module level.
"""
from __future__ import annotations

import functools
import hashlib
import json
from pathlib import Path

import armflag

_ON = armflag.arm("TETHER_AFFORDANCE", default=True)  # prior/settle/refuse rows; record only
# write-up 42 item 4: a picture's recognised class read like a shape_name; inert on grid boards
_RECOGNISED = armflag.arm("TETHER_RECOGNISED", default=True)
# the field / attribute names a picture is read from. Declared convention, Fig 10: visible, movable
PICTURE_NAMES = ("picture", "image")
# a picture is a uint8 array at least this many pixels on each side. Declared convention, Fig 10
PICTURE_MIN_SIDE = 16
# the local class memory (ImageNet terms: never in the repository); absent -> shape route only
CLASS_MEMORY_DIR = Path(r"C:\TETHER_RUNS\DATA_2026-11-16\recognition")
_CLASS_MEMORY: dict = {}
WORD_MAP = Path(__file__).resolve().parent / "library" / "word_map.json"
# a verb's WordNet lexname -> the reading it predicts (a means: what to LOOK at, never the answer)
LEXNAME_READING = {"verb.motion": "moves"}
KEEPS = "keeps moving"
# B7 motion words (write-up 42 "the ball rolls to the right"); record only
_MOTION_UPPER = armflag.arm("TETHER_MOTION_WORDS", default=True)
_ROW, _COL = ("row", "r", "cy", "y"), ("col", "c", "cx", "x")


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
            if c and any(readings(p_) for p_ in ps):
                return {"shape_name": shape_name, "form": forms[0] if forms else None,
                        "concept": c, "via": "shape_bridge", "priors": ps}
    return None


def resolve(shape_name: str, atoms: dict | None, bridge: list | None, priors: list) -> dict | None:
    """The chain for a shape_name: {shape_name, form, concept, via, priors[...]}, or None. The
    bridge first (2D -> 3D -> object, lead 16:20), else SHAPE_ATOMS' atoms, else the shape name,
    each looked up in word_map's priors; a concept counts only if a prior predicts a reading."""
    got = _bridge_chain(shape_name, bridge)
    if got is not None:
        return got
    by_c: dict = {}
    for p in priors:
        by_c.setdefault(str(p["concept"]), []).append(p)
    cands = [("SHAPE_ATOMS", a) for a in ((atoms or {}).get(shape_name) or ())]
    cands.append(("shape_name", shape_name))
    for via, c in cands:
        ps = by_c.get(c) or []
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
    """(rows, why_inert). One `recognised` detail per route: the preloaded shape memory always,
    the class memory when present. why_inert names the failure when no route could run (cv2 or
    the shape memory absent); a route's own abstention is a row, never an inert."""
    try:
        import recognize  # lazy: never at module level (cv2 stays unimported)
        pic = _bgr(img)
        mem = recognize.load_shapes()
        r = recognize.recognise_shape(pic, mem)
    except Exception as e:              # noqa: BLE001  cv2 or the shape memory absent: inert
        return [], f"recognition unavailable: {type(e).__name__}: {e}"
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
    try:
        cm = _class_memory(Path(class_dir) if class_dir else CLASS_MEMORY_DIR)
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
    except Exception as e:              # noqa: BLE001  the class memory unreadable: said, not hidden
        rows.append({"class": None, "route": "class_memory", "abstained": True,
                     "reason": f"class memory unreadable: {type(e).__name__}: {e}",
                     "memory": "class_memory", "stamp": None, "standing": None})
    return rows, None


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
