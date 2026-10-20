"""M, THE STREAMED ak_ READ (the reviewer 2026-10-19 19:21 item 4, G4). Each case runs the real
merge_save on a small memory folder holding one save's ak_ file.

  S1   a non-ASCII entry straddling the read boundaries (reads of 1..13 bytes, a 3-character
       margin, so the decoder's retry runs) gives the SAME store (asked_tally and ak_whole) as the
       whole parse, for a form-2 file and an old-form file
  S2   a file not opening with {"entries":[ is parsed whole, and the merge says so (ak_whole_parse)
  S3   pass 1: a file whose bytes do not hash to its name is refused before any write
  S4   the file altered between pass 1 and pass 2 (same length): refused inside the transaction
       and rolled back -- no row of the save lands, last_merged unchanged
  MFb  MUST-FAIL: a reader that ignores the body's tail (never learns form 2) changes the tally
  MFc  MUST-FAIL: a reader that decodes each read on its own breaks on the straddling character

    python test_store_stream.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
import lineage_store as ls  # noqa: E402

H = "a" * 16
ENTRIES = [{"key": "kÉy-日本", "role": "CAUSE", "o": "o1", "x": "x1", "slot": None, "n": 3},
           {"key": "kÉy-日本", "role": "EFFECT", "o": "o2", "x": "x2", "slot": "o3.ñame", "n": 2},
           {"key": "plain", "role": "CAUSE", "o": "o4", "x": "x4", "slot": "o4.col", "n": 5},
           {"key": "plain", "role": "CAUSE", "o": "o4", "x": "x4", "slot": "o9.col", "n": 1},
           {"key": "ζ", "role": "EFFECT", "o": "o5", "x": "x5", "slot": None, "n": 7}]
G = {"parent": None, "terms": [], "status": [], "invented": {}, "book": {}, "evidence": [],
     "vindication_tail": []}


def folder(form2: bool, lead: str = "") -> tuple[Path, Path]:
    """A memory folder with one ak_ file, named by its own hash; lead="" writes the form the code
    writes ({"entries":[ first)."""
    ents = ENTRIES if form2 else [{k: v for k, v in e.items() if k != "n"} for e in ENTRIES]
    body = {"entries": ents, "gen": H, "refused": [], "sig_arm": "a", "sig_atoms": [],
            **({"form": 2} if form2 else {})}
    raw = (lead + json.dumps(body, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False)).encode("utf-8")
    d = Path(tempfile.mkdtemp(prefix="akst_"))
    f = d / f"ak_{H}_{hashlib.sha256(raw).hexdigest()[:16]}.json"
    f.write_bytes(raw)
    return d, f


def merged(d: Path):
    """merge_save on a fresh store in d; returns (its report, the store's rows) or the exception."""
    con = ls.open_store(d)
    try:
        try:
            rep = ls.merge_save(con, d, H, dict(G))
        except (ls.Refused, UnicodeDecodeError, KeyError, ValueError) as e:
            rep = e
        sym = dict(con.execute("SELECT id, s FROM sym"))
        rows = (sorted((sym[a], sym[b], sym[c], *rest) for a, b, c, *rest
                       in con.execute("SELECT * FROM asked_tally")),
                sorted(con.execute("SELECT * FROM ak_whole")),
                con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone())
    finally:
        con.close()
    return rep, rows


class patched:
    def __init__(self, **kw):
        self.kw = kw

    def __enter__(self):
        self.old = {k: getattr(ls, k) for k in self.kw}
        for k, v in self.kw.items():
            setattr(ls, k, v)

    def __exit__(self, *exc):
        for k, v in self.old.items():
            setattr(ls, k, v)


def main() -> int:
    for form2 in (True, False):
        want_rep, want = merged(folder(form2, lead=" ")[0])           # the whole parse
        assert want_rep["ak_whole_parse"] and want[0] and want[2] == (H,), (want_rep, want)
        for chunk in range(1, 14):
            with patched(AK_READ=chunk, AK_MARGIN=3):
                rep, got = merged(folder(form2)[0])
            assert isinstance(rep, dict) and "ak_whole_parse" not in rep, rep
            assert got == want, (form2, chunk, got, want)
        print(f"S1 form {'2' if form2 else 'old'}: streamed (reads 1..13 bytes, margin 3) = whole "
              f"parse; {len(want[0])} tally rows, {len(want[1])} ak_whole rows")
    print("S2 a file not opening with the entries is parsed whole and reported (ak_whole_parse)")

    d, f = folder(True)
    f.write_bytes(f.read_bytes().replace(b'"n":3', b'"n":4'))
    rep, got = merged(d)
    assert isinstance(rep, ls.Refused) and "hash to its name" in str(rep), rep
    assert got == ([], [], None), got
    print(f"S3 pass 1 refuses a file not matching its name, before any write: {rep}")

    d, f = folder(True)
    real = ls.AkFile.verify

    def verify_then_alter(self):
        real(self)
        self.f.write_bytes(self.f.read_bytes().replace(b'"n":3', b'"n":4'))
    ls.AkFile.verify = verify_then_alter
    try:
        rep, got = merged(d)
    finally:
        ls.AkFile.verify = real
    assert isinstance(rep, ls.Refused) and "changed between" in str(rep), rep
    assert got == ([], [], None), got
    print(f"S4 altered between the passes: {rep}; rolled back, no row, last_merged None")

    class NoTail(ls.AkFile):
        def entries(self):
            yield from super().entries()
            self.tail = {}
    _, want = merged(folder(True)[0])
    with patched(AkFile=NoTail):
        _, got = merged(folder(True)[0])
    assert got[0] != want[0], "MFb: a tail-ignoring reader gave the same tally"
    print("MFb a reader that ignores the tail changes the tally (form 2 read as the old form)")

    class Naive:
        def __init__(self, *_a, **_k):
            pass

        def decode(self, b, **_k):
            return b.decode("utf-8")

    class FakeCodecs:
        @staticmethod
        def getincrementaldecoder(_name):
            return Naive
    broke = []
    for chunk in range(2, 14):       # some of these sizes split a character; each is recorded
        with patched(AK_READ=chunk, AK_MARGIN=3, codecs=FakeCodecs):
            rep, got = merged(folder(True)[0])
        if isinstance(rep, UnicodeDecodeError) or got != want:
            broke.append(chunk)
    assert broke, "MFc: decoding each read on its own never broke"
    print(f"MFc decoding each read on its own breaks on a split character at read sizes {broke}")
    print("store_stream: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
