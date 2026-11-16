"""B8 recognition front end: synthetic pictures drawn with cv2, seconds. SKIPs without cv2."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import cv2
except ImportError:  # the agent runs without OpenCV; so must this suite
    cv2 = None

import recognize as rz


def _blocks(seed, n=60, size=320):
    r = np.random.default_rng(seed)
    img = np.full((size, size, 3), 128, np.uint8)
    for _ in range(n):
        x, y = r.integers(0, size - 30, 2)
        w, h = r.integers(10, 50, 2)
        col = [int(v) for v in r.integers(0, 256, 3)]
        cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), col, -1)
    return img


def _dots(seed, n=90, size=320):
    r = np.random.default_rng(seed)
    img = np.full((size, size, 3), 128, np.uint8)
    for _ in range(n):
        x, y = r.integers(10, size - 10, 2)
        rad = int(r.integers(3, 14))
        col = [int(v) for v in r.integers(0, 256, 3)]
        cv2.circle(img, (int(x), int(y)), rad, col, -1)
    return img


def _warp(img, angle, scale):
    h, w = img.shape[:2]
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    return cv2.warpAffine(img, m, (w, h), borderValue=(128, 128, 128))


def _scramble(img, tiles=8, seed=0):
    """Tiles shuffled and turned: local texture survives, one geometry does not."""
    r = np.random.default_rng(seed)
    h = img.shape[0] // tiles
    parts = [np.rot90(img[i * h:(i + 1) * h, j * h:(j + 1) * h], int(r.integers(0, 4)))
             for i in range(tiles) for j in range(tiles)]
    order = r.permutation(len(parts))
    rows = [np.hstack([parts[order[i * tiles + j]] for j in range(tiles)]) for i in range(tiles)]
    return np.ascontiguousarray(np.vstack(rows))


def _memory(centroid=True):
    return rz.build_memory({"blocks": [_blocks(1)], "dots": [_dots(2)]}, centroid=centroid,
                           synsets={"blocks": "n00000001", "dots": "n00000002"},
                           source="synthetic")


QUERIES = [(15, 1.0), (-30, 0.85), (45, 1.1)]


def test_r1_transformed_copies():
    if cv2 is None:
        print("SKIP R1: cv2 not installed")
        return
    mem = _memory(centroid=False)
    for cls, img in (("blocks", _blocks(1)), ("dots", _dots(2))):
        for a, s in QUERIES:
            row = rz.recognise(_warp(img, a, s), mem)
            assert not row["abstained"] and row["class"] == cls, (cls, a, s, row)
            assert row["synset"] == mem.synsets[cls]
            print("R1", cls, a, s, {k: row[k] for k in ("class", "votes", "margin", "inliers")})


def test_r2_blank_abstains():
    if cv2 is None:
        print("SKIP R2: cv2 not installed")
        return
    row = rz.recognise(np.full((320, 320, 3), 128, np.uint8), _memory())
    assert row["abstained"] and row["class"] is None, row
    print("R2", row["reason"])


def test_r3_centroids_compress_and_still_recognise():
    if cv2 is None:
        print("SKIP R3: cv2 not installed")
        return
    # Two pictures per class (the second a transformed copy) so groups have members to merge.
    pics = {"blocks": [_blocks(1), _warp(_blocks(1), 10, 0.95)],
            "dots": [_dots(2), _warp(_dots(2), -10, 1.05)]}
    raw = rz.build_memory(pics, centroid=False)
    cen = rz.build_memory(pics)
    assert len(cen.centres) < len(raw.centres), (len(cen.centres), len(raw.centres))
    assert cen.stamp["stage"] == "regularity" and cen.stamp["standing"] is None
    for cls, img in (("blocks", _blocks(1)), ("dots", _dots(2))):
        for a, s in QUERIES:
            row = rz.recognise(_warp(img, a, s), cen)
            assert not row["abstained"] and row["class"] == cls, (cls, a, s, row)
    print("R3 centres", len(cen.centres), "from", len(raw.centres))


def test_r3b_save_load_roundtrip(tmp_path=None):
    if cv2 is None:
        print("SKIP R3b: cv2 not installed")
        return
    import tempfile

    d = Path(tmp_path) if tmp_path else Path(tempfile.mkdtemp())
    mem = _memory()
    p = rz.save(mem, d / "mem")
    back = rz.load(p)
    assert np.array_equal(back.centres, mem.centres) and back.classes == mem.classes
    assert back.stamp == mem.stamp and back.synsets == mem.synsets


def _canvas():
    return np.zeros((300, 300, 3), np.uint8)


def test_r4_shape_from_contour():
    if cv2 is None:
        print("SKIP R4: cv2 not installed")
        return
    w = (255, 255, 255)
    disc = cv2.circle(_canvas(), (150, 150), 80, w, -1)
    rect = cv2.rectangle(_canvas(), (40, 90), (260, 200), w, -1)
    sq = cv2.rectangle(_canvas(), (70, 70), (230, 230), w, -1)
    line = cv2.line(_canvas(), (30, 150), (270, 160), w, 4)
    tri = cv2.fillPoly(_canvas(), [np.array([[150, 30], [270, 250], [30, 250]], np.int32)], w)
    ring = cv2.circle(_canvas(), (150, 150), 90, w, 25)
    for want, img in (("disc", disc), ("rectangle", rect), ("square", sq), ("line", line),
                      ("triangle", tri), ("ring", ring)):
        got, m = rz.shape_from_contour(img)
        assert got == want, (want, got, m)
        print("R4", want, m)


def test_mf_geometric_check_is_what_abstains():
    """RED as required: the scrambled picture matches locally but fits no one geometry. With the
    check it abstains; with the check disabled the same evidence names a class."""
    if cv2 is None:
        print("SKIP MF: cv2 not installed")
        return
    mem = _memory(centroid=False)
    # 4x4 tiles, seed 1: 24 ratio-test votes, 8 RANSAC inliers (opencv 4.14.0) -- local matches
    # without one geometry, which is exactly what the check exists to refuse.
    q = _scramble(_blocks(1), tiles=4, seed=1)
    on = rz.recognise(q, mem)
    off = rz.recognise(q, mem, geometric=False)
    print("MF on ", {k: on[k] for k in ("candidate", "votes", "inliers", "abstained")})
    print("MF off", {k: off[k] for k in ("candidate", "votes", "inliers", "abstained")})
    assert on["abstained"], on
    assert not off["abstained"], off


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
