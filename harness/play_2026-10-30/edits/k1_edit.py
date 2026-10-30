p = "test_k1.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


rep('''    gen = [json.load(open(os.path.join(d, f), encoding="utf-8")) for f in os.listdir(d)
           if f.endswith(".json") and "kinds_landed_dk" in open(os.path.join(d, f),
                                                                 encoding="utf-8").read()]
''', '''    from test_k1 import carried
    gen = carried(d)
''')
rep('''HERE = os.path.dirname(os.path.abspath(__file__))
''', '''HERE = os.path.dirname(os.path.abspath(__file__))


def carried(d: str) -> list:
    """The generation files in `d` that carry kinds_landed_dk, read through lineage's own reader
    (lineage_store.file_bytes): since d5c1b12 a save is a zlib stream, and reading it as text
    failed on every run (the reviewer 2026-10-20 21:58)."""
    from pathlib import Path

    import lineage_store as ls
    out = []
    for f in sorted(Path(d).iterdir()):
        if f.suffix == ".json":
            raw = ls.file_bytes(f)
            if b"kinds_landed_dk" in raw:
                out.append(json.loads(raw))
    return out
''')
rep('''def main() -> int:
    in_process()
    d = tempfile.mkdtemp()
''', '''def main() -> int:
    import zlib
    from pathlib import Path
    # the reader can still fail (the reviewer 21:58): a planted compressed save WITHOUT
    # kinds_landed_dk carries nothing, so the pre-check below would be red; one with it is read
    plant = tempfile.mkdtemp()
    Path(plant, "gen_planted.json").write_bytes(zlib.compress(json.dumps({"episodes": []}).encode()))
    assert carried(plant) == [], carried(plant)
    Path(plant, "gen_with.json").write_bytes(
        zlib.compress(json.dumps({"kinds_landed_dk": [[["x"], "e", "k"]]}).encode()))
    assert [len(g["kinds_landed_dk"]) for g in carried(plant)] == [1], carried(plant)
    print("MF-READ a compressed save without kinds_landed_dk carries 0; with it, 1")
    in_process()
    d = tempfile.mkdtemp()
''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
