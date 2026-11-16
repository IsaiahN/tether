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
  only. Every ImageNet-derived memory stays LOCAL under DEFAULT_DIR and never enters the repository.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# LOCAL ONLY: ImageNet-derived data never goes in the repository.
DEFAULT_DIR = Path(r"C:\TETHER_RUNS\DATA_2026-11-16\recognition")

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


def centroids(des: np.ndarray, pts: np.ndarray, radius: int = HAMMING_RADIUS):
    """Group descriptors within `radius` of a group leader (greedy, in input order) and replace each
    group by its bitwise-majority centre. Returns (centres uint8, positions float32, sizes int)."""
    if des is None or len(des) == 0:
        return np.zeros((0, 61), np.uint8), np.zeros((0, 2), np.float32), np.zeros(0, int)
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
    centres = np.empty((len(members), des.shape[1]), np.uint8)
    for g, idx in enumerate(members):
        bits = np.unpackbits(des[idx], axis=1)
        centres[g] = np.packbits((bits.sum(axis=0) * 2 > len(idx)).astype(np.uint8))
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


def build_from_parquet(parquet_paths, out_dir=None, per_class=50, lexicon=None):
    """Read ImageNet-1k parquet shards (columns image{bytes}, label), decode, build and save the
    memory with labels mapped to WordNet ids. Returns the saved path, or None (with a message) when
    neither pyarrow nor pandas is installed. Writes only under out_dir (default DEFAULT_DIR)."""
    cv2 = _cv2()
    rows = None
    try:
        import pyarrow.parquet as pq

        def rows():  # noqa: F811
            for p in parquet_paths:
                t = pq.read_table(p, columns=["image", "label"]).to_pylist()
                yield from t
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
