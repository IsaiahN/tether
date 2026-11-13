"""8e: Isaiah's ATTRIBUTE_INDEX moved to library/ (the reviewer r1855, r1861): both readers load it
from the new path, byte-for-byte (its sha256 holds), and nothing is left at docs/corpus/.

  AI1   inherited.CORPUS_INDEX is library/ATTRIBUTE_INDEX.json; by_cluster() loads it with no error
        and 17 clusters; build_library.CORPUS_INDEX names the same file.
  MF-AI1 inherited.CORPUS_INDEX pointed back at docs/corpus/ (the plant): by_cluster() reads
        "absent" and no clusters -> RED.

    python tests/test_attribute_index_path.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.pop("ATTRIBUTE_INDEX", None)       # build_library reads this override first

import inherited  # noqa: E402

ROOT = Path(_repo.ROOT)
sys.path.insert(0, str(ROOT / "library"))
import build_library  # noqa: E402


def load(path: Path) -> tuple[dict, str | None]:
    real = inherited.CORPUS_INDEX
    inherited.CORPUS_INDEX = path
    inherited.by_cluster.cache_clear()
    try:
        return inherited.by_cluster()
    finally:
        inherited.CORPUS_INDEX = real
        inherited.by_cluster.cache_clear()


def main() -> int:
    new = ROOT / "library" / "ATTRIBUTE_INDEX.json"
    got, why = load(inherited.CORPUS_INDEX)
    same = Path(build_library.CORPUS_INDEX).resolve() == new.resolve()
    print(f"   inherited: {inherited.CORPUS_INDEX} -> {len(got)} clusters, error {why}; "
          f"build_library: {build_library.CORPUS_INDEX}; docs/corpus present: "
          f"{(ROOT / 'docs' / 'corpus').exists()}")
    ok = (Path(inherited.CORPUS_INDEX).resolve() == new.resolve() and why is None
          and len(got) == 17 and same and not (ROOT / "docs" / "corpus").exists())
    print("AI1 both readers load the index from library/: " + ("GREEN" if ok else "RED"))
    assert ok
    bad, why_bad = load(ROOT / "docs" / "corpus" / "ATTRIBUTE_INDEX.json")
    print(f"   the plant (the old path): {len(bad)} clusters, error {why_bad}")
    print("MF-AI1 the old path finds nothing: "
          + ("RED" if not bad else "GREEN (the plant went unseen)"))
    assert not bad
    print("attribute_index_path: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
