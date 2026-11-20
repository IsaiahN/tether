"""recognize -- B8: recognising pictures without a neural network (a front end at the edge).

Design: docs/05-RESEARCH/42-WATSON_2026-11-16_RECURSIVE_DIFFUSION_LEARNING_THE_DESIGN.md,
"B8 in detail". Key points + binary descriptors (AKAZE), a per-class memory compressed by
centroids (bitwise-majority centres, the Kokorin fix for class-size bias), a Hamming vote with
Lowe's ratio test, a geometric check (RANSAC homography) and an ABSTENTION rule: below a declared
minimum of geometrically consistent matches the front end says "I can't say this is like
something" and never invents a class. The second route, shape_from_contour, reads an outline as
one of the grid shape names for objects with no key points.

No learned weights anywhere: the memory is a record compressed by a stated rule and can be rebuilt
from the pictures at any time. Every centre is stamped {stage: 'regularity', source, sha} with
standing None (C3/C6): a recognition is a candidate, the board decides.

Nothing in the agent imports this module at module level, and this module imports cv2 LAZILY
(inside functions), so the agent runs without OpenCV installed.

THIRD-PARTY (akaze / opencv):
- OpenCV (https://opencv.org), Apache License 2.0 -- used as an installed package
  (opencv-python-headless), never vendored.
- AKAZE algorithm: Alcantarilla, Nuevo, Bartoli, "Fast Explicit Diffusion for Accelerated
  Features in Nonlinear Scale Spaces", BMVC 2013. Reference implementation akaze-eigen
  (https://github.com/sweeneychris/akaze-eigen), BSD 3-clause, Copyright (c) 2014 Chris Sweeney,
  Pablo Fernandez Alcantarilla, Jesus Nuevo -- NOT vendored; we call OpenCV's cv2.AKAZE_create.
- ImageNet (https://image-net.org) terms of access: non-commercial research and educational use
  only. Every ImageNet-derived memory stays LOCAL under the dir named by the plain env var
  RDL_RECOGNITION_DIR (default: the repo's shipped generated shapes) and is never committed.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# LOCAL ONLY: ImageNet-derived data never goes in the repository. The PLAIN env var
# RDL_RECOGNITION_DIR (NOT a TETHER_ arm -- the arms seat forbids raw TETHER_ reads) names the
# local dir; absent, the default is the repo's shipped generated shape memory, so Kaggle needs no
# absolute path in the code. Local ImageNet files stay out of the repo (never committed).
_SHIPPED_DIR = Path(__file__).resolve().parent / "library" / "shapes" / "memory"
DEFAULT_DIR = Path(os.environ.get("RDL_RECOGNITION_DIR") or str(_SHIPPED_DIR))

# The ImageNet PARQUET SOURCE is detected separately from the memory dir (both PLAIN env vars,
# never TETHER_ arms). The default is a repo-relative path that does NOT exist in the repo, so no
# absolute path is baked in and the data is never committed. A person with the data sets
# IMAGENET_PARQUET_DIR; the detector below only reports the state and writes nothing.
_PARQUET_DEFAULT = Path(__file__).resolve().parent / "library" / "imagenet" / "parquet-1k"

# ---- declared conventions (Fig 10: visible and movable, never claimed correct) ----
# Hamming radius (bits, of AKAZE's 486-bit MLDB descriptor) within which two descriptors join one
# centroid group. Declared convention, Fig 10: visible and movable, never claimed correct.
HAMMING_RADIUS = 60
# Lowe's ratio test: a match counts only if best distance < LOWE_RATIO * second-best distance.
# Declared convention, Fig 10.
LOWE_RATIO = 0.8
# Minimum geometrically consistent matches (RANSAC inliers) to name a class; below it, abstain (C8).
# Declared convention, Fig 10.
MIN_INLIERS = 10
# How many top-voted classes get the geometric check. Declared convention, Fig 10.
TOP_CLASSES = 3
# RANSAC reprojection threshold in pixels. Declared convention, Fig 10.
RANSAC_PX = 5.0
# The match radius of the Hamming index (bits): recognise() matches a key point only to centres
# within it, and the index finds every one of those exactly (HammingIndex). Set to HAMMING_RADIUS,
# the radius already declared as "the same key point" for centroids, so one radius means one thing;
# with exact-match buckets it makes 61 substrings, one per byte of AKAZE's 61-byte code. Declared
# convention, Fig 10: visible and movable, never claimed correct. Its cost, measured on the test's
# synthetic pictures (opencv 4.14.0): ratio-test matches whose nearest centre lies beyond 60 bits no
# longer vote (brute force had no radius at all).
INDEX_RADIUS = HAMMING_RADIUS
# Raw candidate pairs (before the union is deduplicated) the index materialises at once. A memory
# bound, not a result-affecting setting. Declared convention, Fig 10.
INDEX_PAIR_BUDGET = 1_000_000

# Contour route thresholds. Declared conventions, Fig 10.
DISC_ROUNDNESS = 0.85     # 4*pi*A/P^2 at or above -> disc (a square is pi/4 ~ 0.785)
LINE_ASPECT = 6.0         # long/short side of the min-area box at or above -> line
SQUARE_ASPECT = 1.15      # 4 corners and aspect at or below -> square, else rectangle
BOX_FILL = 0.85           # area / min-area-box area at or above for square/rectangle
HOLE_FRACTION = 0.05      # a child contour with area >= this share of the outer -> ring
APPROX_EPS = 0.03         # approxPolyDP epsilon as a share of the perimeter

# The names shape_from_contour may return. All but 'triangle' are arc_percept.SHAPE_NAMES; the
# grid alphabet has no triangle, so this name is the contour route's own and is flagged as such.
CONTOUR_SHAPES = ("disc", "square", "rectangle", "line", "ring", "triangle", "irregular")

_POP = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint16)


def _cv2():
    import cv2  # lazy: the agent never needs OpenCV

    return cv2


def describe(image_bgr):
    """AKAZE key points and binary MLDB descriptors ((n, 61) uint8, or None when there are none)."""
    cv2 = _cv2()
    img = image_bgr
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not hasattr(cv2, "AKAZE_create"):
        # OpenCV 5.0 wheels ship without AKAZE in the main modules; 4.x has it (pin <5).
        raise RuntimeError(f"cv2 {cv2.__version__} has no AKAZE_create; "
                           "install opencv-python-headless<5")
    kps, des = cv2.AKAZE_create().detectAndCompute(img, None)
    return kps, des


def hamming(a: np.ndarray, b: np.ndarray, chunk: int = 512) -> np.ndarray:
    """Pairwise Hamming distances, (len(a), len(b)) uint16, chunked over a."""
    out = np.empty((len(a), len(b)), dtype=np.uint16)
    for i in range(0, len(a), chunk):
        x = np.bitwise_xor(a[i:i + chunk, None, :], b[None, :, :])
        out[i:i + chunk] = _POP[x].sum(axis=2)
    return out


class HammingIndex:
    """Multi-index hash over binary codes, exact-match buckets only, pure numpy.

    The code's bits are split into m contiguous substrings of near-equal length, and each substring
    gets a bucket table (a sorted key array: a bucket is one run of equal keys). A query's
    candidates are the union of its m buckets; their exact Hamming distances are then computed and
    within `radius` are kept. Pigeonhole: if d(q, c) <= m - 1, then at least one of the m substrings
    of q and c is identical, so c is in that substring's bucket. The index is therefore EXACT --
    every centre within the radius is found, with its true distance -- whenever radius <= m - 1,
    and m defaults to radius + 1 (for AKAZE's 61-byte code and radius 60 that is one byte a
    substring). With m <= radius the guarantee is gone (`guaranteed` says so); the test uses that as
    its mutation.

    Method: Norouzi, Punjani, Fleet, "Fast Search in Hamming Space with Multi-Index Hashing", CVPR
    2012 -- here the special case of substring search radius 0 (exact buckets). No code taken."""

    def __init__(self, codes: np.ndarray, radius: int = None, m: int = None):
        radius = INDEX_RADIUS if radius is None else int(radius)
        self.src = codes                      # identity, so a memory can tell its index is current
        self.codes = np.ascontiguousarray(codes, dtype=np.uint8)
        nbits = self.codes.shape[1] * 8 if self.codes.ndim == 2 else 0
        self.m = int(m) if m is not None else radius + 1
        if not 1 <= self.m <= max(nbits, 1):
            raise ValueError(f"m={self.m} substrings for a {nbits}-bit code")
        self.radius = radius
        self.guaranteed = radius <= self.m - 1
        self.bounds = np.linspace(0, nbits, self.m + 1).round().astype(int)
        keys = self._keys(self.codes)
        self.order = np.argsort(keys, axis=0, kind="stable")          # (n, m)
        self.sorted = np.take_along_axis(keys, self.order, axis=0)    # (n, m), each column sorted

    def _keys(self, codes):
        """(n, m) int64: substring j's bits [bounds[j], bounds[j+1]) read big-endian from the bytes
        that span it (no unpacked copy of the whole code)."""
        out = np.empty((len(codes), self.m), np.int64)
        for j in range(self.m):
            lo, hi = int(self.bounds[j]), int(self.bounds[j + 1])
            b0, b1 = lo // 8, (hi - 1) // 8
            if (b1 - b0 + 1) * 8 > 62:
                raise ValueError(f"substring {j} spans {hi - lo} bits; use more substrings")
            v = np.zeros(len(codes), np.int64)
            for b in range(b0, b1 + 1):
                v = (v << 8) | codes[:, b].astype(np.int64)
            v >>= (b1 + 1) * 8 - hi
            out[:, j] = v & ((1 << (hi - lo)) - 1)
        return out

    def pairs(self, q: np.ndarray):
        """Yield (query row, centre, distance) arrays for every pair within the radius, in chunks
        bounded by INDEX_PAIR_BUDGET raw candidates (a row is never split)."""
        q = np.ascontiguousarray(q, dtype=np.uint8)
        n = len(self.codes)
        if len(q) == 0 or n == 0:
            return
        qk = self._keys(q)
        lo = np.empty(qk.shape, np.int64)
        cnt = np.empty(qk.shape, np.int64)
        for j in range(self.m):
            lo[:, j] = np.searchsorted(self.sorted[:, j], qk[:, j], "left")
            cnt[:, j] = np.searchsorted(self.sorted[:, j], qk[:, j], "right") - lo[:, j]
        cum = np.cumsum(cnt.sum(axis=1))
        start = 0
        while start < len(q):
            base = cum[start - 1] if start else 0
            stop = max(start + 1, int(np.searchsorted(cum, base + INDEX_PAIR_BUDGET, "right")))
            c = cnt[start:stop].ravel()
            tot = int(c.sum())
            if tot:
                rows = np.arange(start, stop)
                row_rep = np.repeat(np.repeat(rows, self.m), c)
                j_rep = np.repeat(np.tile(np.arange(self.m), len(rows)), c)
                offs = np.arange(tot) - np.repeat(np.cumsum(c) - c, c)
                cid = self.order[np.repeat(lo[start:stop].ravel(), c) + offs, j_rep]
                key = np.unique(row_rep * n + cid)        # the union of the m buckets, per row
                qi, ci = key // n, key % n
                d = _POP[np.bitwise_xor(q[qi], self.codes[ci])].sum(axis=1).astype(np.int32)
                w = d <= self.radius
                yield qi[w], ci[w], d[w]
            start = stop

    def search(self, q: np.ndarray):
        """Nearest and second-nearest within the radius, per query row: (index, best, second).
        A row with nothing within the radius gets index -1 and best = second = radius + 1; a row
        with one centre within it gets second = radius + 1. radius + 1 is a LOWER BOUND there
        ("beyond the radius"), never a measured distance."""
        nq = len(q)
        beyond = self.radius + 1
        idx = np.full(nq, -1, np.int64)
        best = np.full(nq, beyond, np.int32)
        second = np.full(nq, beyond, np.int32)
        for qi, ci, d in self.pairs(q):
            if not len(qi):
                continue
            o = np.lexsort((ci, d, qi))
            qi, ci, d = qi[o], ci[o], d[o]
            f = np.nonzero(np.r_[True, qi[1:] != qi[:-1]])[0]
            idx[qi[f]] = ci[f]
            best[qi[f]] = d[f]
            nxt = np.minimum(f + 1, len(qi) - 1)
            two = (f + 1 < len(qi)) & (qi[nxt] == qi[f])
            second[qi[f[two]]] = d[f[two] + 1]
        return idx, best, second


def _greedy_groups(des: np.ndarray, radius: int = HAMMING_RADIUS):
    """Leaders and members: each descriptor joins the nearest existing leader within `radius`
    (greedy, in input order), else leads a new group."""
    leaders: list[int] = []
    members: list[list[int]] = []
    lead_des = np.zeros((0, des.shape[1]), np.uint8)
    for i in range(len(des)):
        if len(leaders):
            d = hamming(des[i:i + 1], lead_des)[0]
            j = int(d.argmin())
            if d[j] <= radius:
                members[j].append(i)
                continue
        leaders.append(i)
        members.append([i])
        lead_des = np.vstack([lead_des, des[i:i + 1]])
    return leaders, members


def _majority(des: np.ndarray) -> np.ndarray:
    bits = np.unpackbits(des, axis=1)
    return np.packbits((bits.sum(axis=0) * 2 > len(des)).astype(np.uint8))


def centroids(des: np.ndarray, pts: np.ndarray, radius: int = HAMMING_RADIUS):
    """Group descriptors within `radius` of a group leader (greedy, in input order) and replace each
    group by its bitwise-majority centre. Returns (centres uint8, positions float32, sizes int)."""
    if des is None or len(des) == 0:
        return np.zeros((0, 61), np.uint8), np.zeros((0, 2), np.float32), np.zeros(0, int)
    leaders, members = _greedy_groups(des, radius)
    centres = np.empty((len(members), des.shape[1]), np.uint8)
    for g, idx in enumerate(members):
        centres[g] = _majority(des[idx])
    # A centre's position is its LEADER's key point in its own picture (declared convention, Fig 10:
    # across pictures of a category the geometry is weak; the check stays a check, not a claim).
    positions = pts[leaders].astype(np.float32)
    sizes = np.array([len(m) for m in members])
    return centres, positions, sizes


def _sha_images(images_by_class) -> str:
    h = hashlib.sha256()
    for name in sorted(images_by_class):
        h.update(str(name).encode())
        for img in images_by_class[name]:
            h.update(np.ascontiguousarray(img).tobytes())
    return h.hexdigest()


@dataclass
class Memory:
    """Per-class descriptor centres. A record, never weights; standing None (C3)."""

    classes: list
    centres: np.ndarray            # (n, 61) uint8
    labels: np.ndarray             # (n,) int index into classes
    positions: np.ndarray          # (n, 2) float32
    synsets: dict = field(default_factory=dict)   # class -> WordNet id, when known
    stamp: dict = field(default_factory=dict)
    raw_count: int = 0             # descriptors before centroids


def build_memory(images_by_class, max_per_class=None, centroid=True, synsets=None,
                 source="imagenet-1k") -> Memory:
    """Describe every picture of every class; compress each class by centroids (unless centroid is
    False, kept so the compression's effect stays measurable)."""
    classes = sorted(images_by_class)
    cs, ls, ps = [], [], []
    raw = 0
    for k, name in enumerate(classes):
        imgs = list(images_by_class[name])[:max_per_class] if max_per_class else list(
            images_by_class[name])
        des_l, pts_l = [], []
        for img in imgs:
            kps, des = describe(img)
            if des is None:
                continue
            des_l.append(des)
            pts_l.append(np.array([kp.pt for kp in kps], np.float32))
        if not des_l:
            continue
        des = np.vstack(des_l)
        pts = np.vstack(pts_l)
        raw += len(des)
        if centroid:
            c, p, _ = centroids(des, pts)
        else:
            c, p = des, pts
        cs.append(c)
        ps.append(p)
        ls.append(np.full(len(c), k, int))
    stamp = {"stage": "regularity", "source": source, "sha": _sha_images(images_by_class),
             "standing": None, "hamming_radius": HAMMING_RADIUS if centroid else None,
             "max_per_class": max_per_class}
    return Memory(classes=classes,
                  centres=np.vstack(cs) if cs else np.zeros((0, 61), np.uint8),
                  labels=np.concatenate(ls) if ls else np.zeros(0, int),
                  positions=np.vstack(ps) if ps else np.zeros((0, 2), np.float32),
                  synsets=dict(synsets or {}), stamp=stamp, raw_count=raw)


def save(memory: Memory, path=None) -> Path:
    """Write <path>.npz (arrays) and <path>.json (header). Default: DEFAULT_DIR/memory."""
    path = Path(path) if path else DEFAULT_DIR / "memory"
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path.with_suffix(".npz"), centres=memory.centres, labels=memory.labels,
                        positions=memory.positions)
    header = {"classes": memory.classes, "synsets": memory.synsets, "stamp": memory.stamp,
              "raw_count": memory.raw_count, "n_centres": int(len(memory.centres))}
    path.with_suffix(".json").write_text(json.dumps(header, indent=1), encoding="utf-8")
    return path


def load(path=None) -> Memory:
    path = Path(path) if path else DEFAULT_DIR / "memory"
    header = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    z = np.load(path.with_suffix(".npz"))
    return Memory(classes=header["classes"], centres=z["centres"], labels=z["labels"],
                  positions=z["positions"], synsets=header.get("synsets", {}),
                  stamp=header.get("stamp", {}), raw_count=header.get("raw_count", 0))


def class_memory_status(dir=None) -> dict:
    """The state of the OPTIONAL ImageNet class memory at `dir` (default: the configured
    RDL_RECOGNITION_DIR, resolved at import). NO side effects and NO large reads: the small header
    JSON is parsed and the npz is only OPENED (its array keys checked, never the arrays loaded).

    Returns a dict: dir, dir_exists, parquet_dir, parquet_source ('env' or 'default'),
    parquet_detected (the parquet dir is a directory holding at least one .parquet shard),
    present (memory.json + memory.npz both exist), loadable (header parses, npz opens with the
    three expected arrays), classes (count from the header, 0 if absent), active (present and
    loadable with at least one class), event ('class_memory_active' or 'recognised_inert') and
    one 'reason' string. The reason names the exact state: no data / parquet not found /
    not built / load failed, or the active class count. The memory being loadable is the
    activation condition; parquet detection explains WHY an absent memory cannot be used."""
    d = Path(dir) if dir is not None else DEFAULT_DIR
    raw_pq = os.environ.get("IMAGENET_PARQUET_DIR")
    pq = Path(raw_pq) if raw_pq else _PARQUET_DEFAULT
    pq_source = "env" if raw_pq else "default"
    # rglob, not glob: the real download puts shards under data/ (and train/validation
    # subfolders), not at the top level. A top-level glob reports "no data" for a
    # fully-populated directory -- measured 2026-11-20: 308 shards present, detector False.
    pq_detected = pq.is_dir() and any(pq.rglob("*.parquet"))

    present = (d / "memory.json").is_file() and (d / "memory.npz").is_file()
    classes = 0
    loadable = False
    err = None
    if present:
        try:
            header = json.loads((d / "memory.json").read_text(encoding="utf-8"))
            classes = len(header.get("classes") or ())
            z = np.load(d / "memory.npz")
            try:
                missing = {"centres", "labels", "positions"} - set(z.files)
                if missing:
                    raise KeyError(f"npz missing {sorted(missing)}")
            finally:
                z.close()
            loadable = True
            if classes == 0:
                err = "header carries 0 classes"
        except Exception as e:                   # noqa: BLE001  a present-but-broken memory is said
            err = f"{type(e).__name__}: {e}"

    active = present and loadable and classes > 0
    if active:
        event = "class_memory_active"
        reason = f"class memory active: {classes} classes loaded from {d}"
    elif present and not active:
        event = "recognised_inert"
        reason = f"class memory load failed at {d}: {err or 'unknown error'}"
    elif pq_source == "env" and not pq.is_dir():
        event = "recognised_inert"
        reason = (f"parquet not found at {pq}: class memory absent at {d}; point "
                  "IMAGENET_PARQUET_DIR at the ImageNet parquet dir")
    elif not pq_detected:
        event = "recognised_inert"
        reason = (f"no data: class memory absent at {d}; no ImageNet parquet at {pq} "
                  "(set IMAGENET_PARQUET_DIR); memory.json/memory.npz not built")
    else:
        event = "recognised_inert"
        reason = (f"class memory not built: ImageNet parquet detected at {pq} but "
                  f"memory.json/memory.npz absent at {d}; run python recognize.py "
                  "--build-class-memory")

    return {"dir": str(d), "dir_exists": d.is_dir(), "parquet_dir": str(pq),
            "parquet_source": pq_source, "parquet_detected": bool(pq_detected),
            "present": bool(present), "loadable": bool(loadable), "classes": int(classes),
            "active": bool(active), "event": event, "reason": reason}


def _abstain(reason, **kw):
    row = {"class": None, "synset": None, "votes": 0, "margin": 0, "inliers": 0,
           "abstained": True, "reason": reason}
    row.update(kw)
    return row


def recognise(image_bgr, memory: Memory, geometric: bool = True) -> dict:
    """Match, vote per class centre, check geometry, abstain when evidence is thin.

    geometric=False skips the RANSAC check and counts every ratio-test match as consistent; it
    exists only so the test can show the check is what abstains."""
    cv2 = _cv2()
    if len(memory.centres) < 2:
        return _abstain("memory holds fewer than two centres")
    kps, des = describe(image_bgr)
    if des is None or len(des) == 0:
        return _abstain("no key points")
    d = hamming(des, memory.centres).astype(np.int32)
    order = np.argsort(d, axis=1)[:, :2]
    best = d[np.arange(len(d)), order[:, 0]]
    second = d[np.arange(len(d)), order[:, 1]]
    ok = best < LOWE_RATIO * second
    if not ok.any():
        return _abstain("no match passes the ratio test")
    q_idx = np.nonzero(ok)[0]
    c_idx = order[ok, 0]
    cls = memory.labels[c_idx]
    votes = np.bincount(cls, minlength=len(memory.classes))
    ranked = [int(k) for k in np.argsort(-votes, kind="stable") if votes[k] > 0][:TOP_CLASSES]
    q_pts = np.array([kps[i].pt for i in q_idx], np.float32)
    inl = {}
    for k in ranked:
        sel = cls == k
        if not geometric:
            inl[k] = int(sel.sum())
            continue
        if sel.sum() < 4:
            inl[k] = 0
            continue
        src = memory.positions[c_idx[sel]].reshape(-1, 1, 2)
        dst = q_pts[sel].reshape(-1, 1, 2)
        _h, mask = cv2.findHomography(src, dst, cv2.RANSAC, RANSAC_PX)
        inl[k] = int(mask.sum()) if mask is not None else 0
    top = max(ranked, key=lambda k: (inl[k], votes[k]))
    sv = sorted(votes.tolist(), reverse=True)
    margin = int(sv[0] - (sv[1] if len(sv) > 1 else 0))
    name = memory.classes[top]
    abstained = inl[top] < MIN_INLIERS
    reason = (f"inliers {inl[top]} < MIN_INLIERS {MIN_INLIERS}" if abstained else
              f"inliers {inl[top]} >= MIN_INLIERS {MIN_INLIERS}"
              + ("" if geometric else " (geometric check disabled)"))
    return {"class": None if abstained else name,
            "synset": None if abstained else memory.synsets.get(name),
            "candidate": name, "votes": int(votes[top]), "margin": margin,
            "inliers": inl[top], "abstained": abstained, "reason": reason,
            "geometric": geometric, "stamp": memory.stamp}


def shape_from_contour(image_bgr):
    """The second route: the largest outline as a grid shape name. Returns (name, measures)."""
    cv2 = _cv2()
    g = image_bgr if image_bgr.ndim == 2 else cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    _t, bw = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    border = np.concatenate([bw[0], bw[-1], bw[:, 0], bw[:, -1]])
    if border.mean() > 127:          # background is the bright side: the object is dark
        bw = 255 - bw
    contours, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    outer = [i for i in range(len(contours)) if hier[0][i][3] < 0]
    if not outer:
        return "irregular", {"reason": "no contour"}
    i = max(outer, key=lambda j: cv2.contourArea(contours[j]))
    c = contours[i]
    area = float(cv2.contourArea(c))
    perim = float(cv2.arcLength(c, True))
    roundness = 4 * math.pi * area / (perim * perim) if perim > 0 else 0.0
    (_cx, _cy), (bw_, bh_), _ang = cv2.minAreaRect(c)
    long_, short = max(bw_, bh_), max(min(bw_, bh_), 1e-6)
    aspect = long_ / short
    fill = area / (long_ * short) if long_ * short > 0 else 0.0
    corners = len(cv2.approxPolyDP(c, APPROX_EPS * perim, True))
    holes = [j for j in range(len(contours)) if hier[0][j][3] == i
             and cv2.contourArea(contours[j]) >= HOLE_FRACTION * area]
    m = {"area": area, "perimeter": perim, "roundness": round(roundness, 4),
         "aspect": round(aspect, 4), "fill": round(fill, 4), "corners": corners,
         "holes": len(holes)}
    if holes:
        name = "ring"
    elif aspect >= LINE_ASPECT:
        name = "line"
    elif roundness >= DISC_ROUNDNESS and corners > 4:
        name = "disc"
    elif corners == 3:
        name = "triangle"
    elif corners == 4 and fill >= BOX_FILL:
        name = "square" if aspect <= SQUARE_ASPECT else "rectangle"
    else:
        name = "irregular"
    return name, m


def _lexicon_wnids(path=None) -> dict:
    path = Path(path) if path else (Path(__file__).parent / "library"
                                    / "lexicon_imagenet_wordnet.json")
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {int(c["index"]): c["wnid"] for c in data["classes"]}


def build_from_parquet(parquet_paths, out_dir=None, per_class=50, lexicon=None, labels=None):
    """Read ImageNet-1k parquet shards (columns image{bytes}, label), decode, build and save the
    memory with labels mapped to WordNet ids. Returns the saved path, or None (with a message) when
    neither pyarrow nor pandas is installed. Writes only under out_dir (default DEFAULT_DIR).

    `labels`, when given, restricts the build to those integer ImageNet labels: a small opt-in
    proof build over a handful of classes, rather than the whole shard. Never used on the agent
    path; the caller supplies it for an offline demonstration."""
    cv2 = _cv2()
    wanted = set(int(x) for x in labels) if labels is not None else None
    rows = None
    try:
        import pyarrow.parquet as pq

        def rows():  # noqa: F811
            # CHOOSE ROWS BY LABEL FIRST, THEN DECODE ONLY THE SELECTED IMAGES.
            # The old form did read_table(["image","label"]).to_pylist(), which
            # materialized every image in the shard as a Python object BEFORE the
            # per_class filter in the caller. Measured 2026-11-20: one 458 MB
            # validation shard reached 2.96 GB RAM and 8+ min at per_class=3,
            # while reading the label column alone took 0.1 s. The image bytes stay
            # in the Arrow column until a selected row is converted, one at a time.
            for p in parquet_paths:
                t = pq.read_table(p, columns=["image", "label"])
                labels = t.column("label").to_pylist()
                img_col = t.column("image")
                counts: dict = {}
                for i, lab in enumerate(labels):
                    k = int(lab)
                    if wanted is not None and k not in wanted:
                        continue
                    if per_class and counts.get(k, 0) >= per_class:
                        continue
                    counts[k] = counts.get(k, 0) + 1
                    yield {"label": lab, "image": img_col[i].as_py()}
    except ImportError:
        try:
            import pandas as pd

            def rows():  # noqa: F811
                for p in parquet_paths:
                    yield from pd.read_parquet(p, columns=["image", "label"]).to_dict("records")
        except ImportError:
            print("SKIP build_from_parquet: neither pyarrow nor pandas is installed")
            return None
    wnids = _lexicon_wnids(lexicon)
    by_class: dict = {}
    for r in rows():
        k = int(r["label"])
        if per_class and len(by_class.get(k, ())) >= per_class:
            continue
        img = r["image"]
        raw = img.get("bytes") if isinstance(img, dict) else img
        if raw is None:
            continue
        pic = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if pic is not None:
            by_class.setdefault(k, []).append(pic)
    named = {wnids.get(k, str(k)): v for k, v in by_class.items()}
    mem = build_memory(named, max_per_class=per_class,
                       synsets={w: w for w in named if w.startswith("n")})
    out = Path(out_dir) if out_dir else DEFAULT_DIR
    return save(mem, out / "memory")


# ---- the preloaded shape memory (library/shapes, generated by library/build_shapes.py) ----
SHAPES_DIR = Path(__file__).resolve().parent / "library" / "shapes"
# Abstain when the nearest class's feature distance exceeds this. Declared convention, Fig 10.
SHAPE_MAX_DISTANCE = 3.5
# Per-feature weights of the L1 distance: Hu 1-4, Hu 5-7 (off: near-zero for symmetric shapes, so
# their logs are noise), hole share, solidity, shading std, log2 of the distinct interior grey
# levels (capped, see SHADE_LEVELS_CAP). The last reads shading TEXTURE, which the std alone misses
# on gently-lit solids; it is 0 for a flat outline, ~1.6 for a three-face solid and ~3.6 for a
# gently shaded one, so weight 1 puts it on the same scale as a Hu dimension. Declared convention,
# Fig 10.
SHAPE_W = np.array([1, 1, 1, 1, 0, 0, 0, 1, 1, 0.05, 1.0], np.float32)
# Distinct interior grey levels at or above this read as "smoothly shaded"; finer counts do not
# change the geometry (faceted solids carry 2-14 levels, smooth ones 55-100, measured over all 13
# generated 3D classes). Capping the tail keeps a frame-filling noise mask -- which carries ~245
# levels -- from looking unlike every smooth template once the share guard is removed. Declared
# convention, Fig 10: visible and movable, never claimed correct.
SHADE_LEVELS_CAP = 16
# Abstain when the second class is within this of the first. Declared convention, Fig 10.
SHAPE_MIN_MARGIN = 0.02
# Interior grey standard deviation above which the picture is read as SHADED (a 3D solid), so the
# contour route compares it only with 3D classes, else only with 2D ones. Declared convention,
# Fig 10.
SHADED_STD = 8.0
# A discrete object sits on a background: the largest outer contour of a real shape never fills the
# frame. Measured over all 176 held-out renders (2026-11-19) the max blob_share is 0.4803 (sphere);
# uniform noise renders at ~0.98 (its foreground mask swallows the frame). Declared convention,
# Fig 10, set between the two measured values; visible and movable, never claimed correct.
SHAPE_MAX_SHARE = 0.75
# approxPolyDP epsilon for the corner feature, as a share of the outer contour's perimeter. Declared
# convention, Fig 10: at 0.01 every drawn polygon reads its own vertex count on the held-outs.
SHAPE_CORNER_EPS = 0.01
# Added to a 2D class's distance when its expected corner count (memory.json "corners"; curved
# classes 0, exempt) differs from the picture's. Declared convention, Fig 10.
SHAPE_CORNER_PENALTY = 10.0
# FIG 10 CONVENTION: a "dot" is a TINY blob. Hu moments are scale-invariant, so a dot and a
# circle have the same signature and the tie-break alone would name a large disc a dot; the
# largest contour's share of the picture separates them (2% of the frames; visible, movable).
DOT_MAX_SHARE = 0.02
# FIG 10 CONVENTION: an abs-log10 Hu moment at or above this has collapsed to zero (the clamp),
# so it says nothing about the shape. A dim saturated on EITHER side is left out of the distance
# and the distance is rescaled to its usual units, so an ideal circle is not charged for the
# higher moments its own symmetry zeroes.
HU_SATURATED = 11.5
_SHAPE_CACHE: dict = {}


def _foreground(image_bgr):
    """Mask of pixels that differ from the background (the median border colour) by > 40 on any
    channel. Declared convention, Fig 10."""
    img = image_bgr if image_bgr.ndim == 3 else np.repeat(image_bgr[:, :, None], 3, axis=2)
    border = np.concatenate([img[0], img[-1], img[:, 0], img[:, -1]]).astype(int)
    bg = np.median(border, axis=0)
    return (np.abs(img.astype(int) - bg).max(axis=2) > 40).astype(np.uint8) * 255


def shape_features(image_bgr):
    """abs log10 Hu moments (7) of the largest outer contour, then hole share, solidity, interior
    shading (grey std) and log2 of the distinct interior grey levels. None when no foreground."""
    cv2 = _cv2()
    bw = _foreground(image_bgr)
    contours, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    outer = [i for i in range(len(contours)) if hier[0][i][3] < 0]
    if not outer:
        return None
    i = max(outer, key=lambda j: cv2.contourArea(contours[j]))
    c = contours[i]
    area = float(cv2.contourArea(c))
    hu = np.zeros(7) if area < 4 else cv2.HuMoments(cv2.moments(c)).ravel()
    lhu = np.abs(np.log10(np.maximum(np.abs(hu), 1e-12)))
    holes = sum(cv2.contourArea(contours[j]) for j in range(len(contours)) if hier[0][j][3] == i)
    hull = float(cv2.contourArea(cv2.convexHull(c)))
    solidity = area / hull if hull > 0 else 0.0
    inside = np.zeros_like(bw)
    cv2.drawContours(inside, [c], -1, 255, -1)
    inside = cv2.erode(inside, np.ones((5, 5), np.uint8)) & bw
    g = image_bgr if image_bgr.ndim == 2 else cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    std = float(g[inside > 0].std()) if (inside > 0).sum() > 10 else 0.0
    levels = min(interior_grey_levels(image_bgr), SHADE_LEVELS_CAP)
    extra = [10 * holes / max(area, 1.0), 10 * solidity, std, math.log2(max(levels, 1))]
    return np.concatenate([lhu, extra]).astype(np.float32)


def interior_grey_levels(image_bgr):
    """Distinct grey levels in the eroded interior of the largest foreground contour (0 when the
    outline is too thin to leave an interior). A flat filled outline has exactly one; a shaded
    solid has more, including when its shading is too gentle to raise the grey std above SHADED_STD.
    Read by shape_features as the shading-texture feature and by recognise_shape for the 2D/3D
    gate."""
    cv2 = _cv2()
    bw = _foreground(image_bgr)
    contours, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    outer = [k for k in range(len(contours)) if hier[0][k][3] < 0]
    if not outer:
        return 0
    c = contours[max(outer, key=lambda m: cv2.contourArea(contours[m]))]
    inside = np.zeros_like(bw)
    cv2.drawContours(inside, [c], -1, 255, -1)
    inside = cv2.erode(inside, np.ones((5, 5), np.uint8)) & bw
    g = image_bgr if image_bgr.ndim == 2 else cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    vals = g[inside > 0]
    return int(np.unique(vals).size) if len(vals) > 10 else 0


def roundness(image_bgr):
    """4*pi*A/P^2 of the largest outer contour (1.0 a circle, pi/4 ~ 0.785 a square). Read by
    recognise_shape as a rule against polygons; never a feature, so the memory stays valid."""
    cv2 = _cv2()
    bw = _foreground(image_bgr)
    contours, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    outer = [k for k in range(len(contours)) if hier[0][k][3] < 0]
    if not outer:
        return 0.0
    c = contours[max(outer, key=lambda m: cv2.contourArea(contours[m]))]
    area, per = float(cv2.contourArea(c)), float(cv2.arcLength(c, True))
    return float(4.0 * np.pi * area / (per * per)) if per > 0 else 0.0


def blob_share(image_bgr):
    """The largest outer contour's area as a share of the picture (0.0 when there is none).
    Read by recognise_shape for the dot rule; never part of shape_features, so the committed
    memory stays valid."""
    cv2 = _cv2()
    bw = _foreground(image_bgr)
    contours, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    outer = [k for k in range(len(contours)) if hier[0][k][3] < 0]
    if not outer:
        return 0.0
    k = max(outer, key=lambda m: cv2.contourArea(contours[m]))
    frame = float(image_bgr.shape[0] * image_bgr.shape[1])
    return float(cv2.contourArea(contours[k])) / frame if frame else 0.0


def corner_count(image_bgr):
    """Corners of approxPolyDP (SHAPE_CORNER_EPS x perimeter) on the largest outer contour."""
    cv2 = _cv2()
    contours, _ = cv2.findContours(_foreground(image_bgr), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)
    if not contours:
        return None
    c = max(contours, key=cv2.contourArea)
    return len(cv2.approxPolyDP(c, SHAPE_CORNER_EPS * cv2.arcLength(c, True), True))


def load_shapes(path=None) -> dict:
    """The preloaded shape memory: Hu features per variant + an AKAZE Memory over the variants."""
    path = Path(path) if path else SHAPES_DIR / "memory"
    key = str(path)
    if key not in _SHAPE_CACHE:
        header = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        z = np.load(path.with_suffix(".npz"))
        mem = Memory(classes=header["akaze_classes"], centres=z["centres"], labels=z["labels"],
                     positions=z["positions"], stamp=header.get("stamp", {}))
        index = json.loads((path.parent / "index.json").read_text(encoding="utf-8"))
        _SHAPE_CACHE[key] = {"classes": header["classes"], "dims": header["dims"],
                             "corners": header.get("corners", {}), "hu": z["hu"],
                             "hu_labels": z["hu_labels"], "akaze": mem,
                             "meta": {e["name"]: e for e in index["classes"]}}
    return _SHAPE_CACHE[key]


def recognise_shape(image_bgr, memory=None, hu_route: bool = True) -> dict:
    """Name a picture as one of the core shapes, or abstain.

    (1) contour route: nearest class by L1 distance over shape_features (2D classes for flat
    pictures, 3D classes for shaded ones), with the margin to the next class; a 2D class whose
    expected corner count differs from the picture's (corner_count) is penalised by
    SHAPE_CORNER_PENALTY, so among matching classes the Hu distance decides; a class named "dot"
    is penalised the same way when its blob fills more than DOT_MAX_SHARE of the picture, and a
    polygon class is penalised when the picture's outline is at least DISC_ROUNDNESS round;
    (2) AKAZE vote over the
    shape memory. The contour winner stands unless AKAZE has >= MIN_INLIERS for a different class.
    Abstains when the foreground fills more than SHAPE_MAX_SHARE of the frame (no closed outline),
    the distance exceeds SHAPE_MAX_DISTANCE, or the margin is below SHAPE_MIN_MARGIN.
    A Hu dim saturated on either side (HU_SATURATED) is left out of the distance.
    hu_route=False exists only for the test's mutation check (AKAZE alone)."""
    m = memory or load_shapes()
    names = m["classes"]
    out = {"class": None, "dim": None, "grid_shape_name": None, "bridge": None, "route": None,
           "distance": None, "margin": None, "abstained": True, "reason": ""}
    winner, route = None, None
    f = shape_features(image_bgr) if hu_route else None
    if f is not None:
        # A gently-lit solid can have interior grey std below SHADED_STD (measured: cone views at
        # 6.06/6.21). Its interior still holds more than one grey level, while a flat filled outline
        # holds exactly one (measured over all 31 generated 2D classes). Either reading
        # says "solid".
        shaded = f[-1] > SHADED_STD or interior_grey_levels(image_bgr) > 1
        want = 3 if shaded else 2
        feats = m["hu"].copy()
        # a dim saturated on either side is uninformative (HU_SATURATED): mask it, rescale
        diff = np.abs(feats - f)
        inform = (np.minimum(feats, f) < HU_SATURATED).astype(np.float32)
        w = inform * SHAPE_W
        denom = w.sum(axis=1)
        full = float(SHAPE_W.sum())
        with np.errstate(invalid="ignore", divide="ignore"):
            d = np.where(denom > 0, (diff * w).sum(axis=1) / denom * full, np.inf)
        best: dict = {}
        for k, lab in enumerate(m["hu_labels"]):
            n = names[int(lab)]
            if m["dims"][n] != want:
                continue
            best[n] = min(best.get(n, np.inf), float(d[k]))
        seen = corner_count(image_bgr) if want == 2 else None
        out["corners"] = seen
        share = blob_share(image_bgr)
        out["share"] = round(share, 4)
        rnd = roundness(image_bgr)
        out["roundness"] = round(rnd, 4)
        if share > SHAPE_MAX_SHARE:
            # The foreground fills the frame: no closed outline encloses a bounded object, so no
            # class can be named (the false-positive failure mode on uniform noise).
            out["reason"] = (
                f"blob fills {share:.3f} of frame > SHAPE_MAX_SHARE {SHAPE_MAX_SHARE}"
            )
            winner = None
        else:
            for n in best:
                exp = m["corners"].get(n)
                if seen is not None and exp and exp != seen:
                    best[n] += SHAPE_CORNER_PENALTY
                if n == "dot" and share > DOT_MAX_SHARE:
                    best[n] += SHAPE_CORNER_PENALTY   # a large blob is not a dot (DOT_MAX_SHARE)
                if rnd >= DISC_ROUNDNESS and (m["corners"].get(n) or 0) >= 3:
                    # a round outline is not a polygon: Hu moments clamp on symmetric shapes, so an
                    # ideal circle can sit nearer a square template than its own (DISC_ROUNDNESS)
                    best[n] += SHAPE_CORNER_PENALTY
            ranked = sorted(best.items(), key=lambda kv: kv[1])
            if ranked:
                winner, dist = ranked[0]
                margin = ranked[1][1] - dist if len(ranked) > 1 else float("inf")
                out.update(distance=round(dist, 4), margin=round(margin, 4))
                route = "contour"
                if dist > SHAPE_MAX_DISTANCE:
                    out["reason"] = f"distance {dist:.3f} > SHAPE_MAX_DISTANCE {SHAPE_MAX_DISTANCE}"
                    winner = None
                elif margin < SHAPE_MIN_MARGIN:
                    out["reason"] = f"margin {margin:.3f} < SHAPE_MIN_MARGIN {SHAPE_MIN_MARGIN}"
                    winner = None
    ak = recognise(image_bgr, m["akaze"])
    out["akaze"] = {"candidate": ak.get("candidate"), "inliers": ak.get("inliers", 0)}
    if not ak["abstained"] and ak["class"] != winner and (winner is not None or not hu_route
                                                          or f is None):
        winner, route = ak["class"], "akaze"
        out["reason"] = ak["reason"]
    if winner is None:
        out["reason"] = out["reason"] or "no route names a class"
        return out
    meta = m["meta"].get(winner, {})
    out.update({"class": winner, "dim": m["dims"][winner],
                "grid_shape_name": meta.get("grid_shape_name"), "bridge": meta.get("bridge"),
                "route": route, "abstained": False})
    return out


# ---- OFFLINE class-memory builder: CLI only, NEVER on the agent path (Isaiah 2026-11-20) ----
def build_class_memory_from_parquet(parquet_dir, out_dir, per_class=50, lexicon=None):
    """OFFLINE builder for the OPTIONAL ImageNet class memory. Discovers *.parquet shards under
    `parquet_dir` (data the person supplies locally -- never committed) and delegates to
    build_from_parquet, so the SAME lexicon/WordNet mapping and build_memory shape are reused.
    Writes only under `out_dir`. Returns the saved path, or None when there are no shards or no
    parquet reader. The agent never calls this; only the CLI below and the tests do."""
    d = Path(parquet_dir)
    if not d.is_dir():
        print(f"SKIP build_class_memory_from_parquet: {d} is not a directory")
        return None
    paths = sorted(d.rglob("*.parquet"))   # shards live under data/, not at the top level
    if not paths:
        print(f"SKIP build_class_memory_from_parquet: no .parquet shards under {d}")
        return None
    return build_from_parquet(paths, out_dir=Path(out_dir), per_class=per_class,
                              lexicon=lexicon)


def _main(argv=None) -> int:
    """CLI: `python recognize.py --build-class-memory --parquet-dir DIR --out-dir DIR`.
    The offline build is the ONLY thing this entry point does; importing recognize (the agent
    path) never builds anything."""
    import argparse

    p = argparse.ArgumentParser(description="recognize: the optional image class memory")
    p.add_argument("--build-class-memory", action="store_true",
                   help="OFFLINE: build a class memory from local ImageNet parquet shards")
    p.add_argument("--parquet-dir", default=None,
                   help="dir holding *.parquet shards (default: $IMAGENET_PARQUET_DIR)")
    p.add_argument("--out-dir", default=None,
                   help="dir to write memory.json / memory.npz (default: $RDL_RECOGNITION_DIR)")
    p.add_argument("--per-class", type=int, default=50)
    p.add_argument("--lexicon", default=None, help="optional lexicon JSON override")
    a = p.parse_args(argv)
    if not a.build_class_memory:
        p.print_help()
        return 0
    pq = Path(a.parquet_dir) if a.parquet_dir else Path(
        os.environ.get("IMAGENET_PARQUET_DIR") or str(_PARQUET_DEFAULT))
    out = Path(a.out_dir) if a.out_dir else DEFAULT_DIR
    saved = build_class_memory_from_parquet(pq, out, per_class=a.per_class,
                                             lexicon=a.lexicon)
    print(f"built class memory at {saved}" if saved else "no class memory built")
    return 0 if saved else 1


if __name__ == "__main__":
    raise SystemExit(_main())
