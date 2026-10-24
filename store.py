"""THE ONE DOOR to the agent's knowledge (Isaiah 2026-10-24 08:30: "one service that fetches and
stores data based on the conditional efficiently"; the reviewer 08:49, 08:56, 08:58). Every read of
a library file and every load or save of the learned store goes through here.

STEP 1, A THIN FACADE: today's code does the work, unchanged, behind each function -- lineage.py,
lineage_store.py and gamma's save / load are the learned backends, folded in here at steps 4-5, when
the json|db conditional joins. Same arguments, same results; conform/door.py (M7) checks that no
other module opens a knowledge file.

At the repo root, not in library/: the library-ABSENT ablation (TETHER_LIBRARY_REQUIRED=0) still
loads and saves a learned store, and a door inside library/ would vanish with it."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

LIBRARY = Path(__file__).parent / "library"


def _lineage():
    """lineage, imported at first use: `import store` costs nothing, so the library readers
    (inherited, compile_term) import it without pulling in the learned backend."""
    import lineage
    return lineage


# ---------------------------------------------------------------- the library's files
def read_json(path: str | Path) -> Any:
    """A knowledge file's parsed JSON, or None when it is absent (the library ablation)."""
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def read_text(path: str | Path) -> str:
    """A knowledge file's text; raises as Path.read_text does."""
    return Path(path).read_text(encoding="utf-8")


def read_bytes(path: str | Path) -> bytes:
    """A knowledge file's bytes; raises as Path.read_bytes does."""
    return Path(path).read_bytes()


# ---------------------------------------------------------------- the learned store
def lineage_load(d: str | Path, ag: Any) -> dict:
    return _lineage().load(d, ag)


def lineage_write(d: str | Path, ag: Any, game: str, sleep: bool = True) -> dict:
    return _lineage().write(d, ag, game, sleep=sleep)


def lineage_boundary(d: str | Path | None, ag: Any, game: str, how: str) -> dict | None:
    return _lineage().boundary(d, ag, game, how)


def library_load(g: Any, path: str, **kw: Any) -> dict:
    """A library= save into Gamma g (gamma.Gamma.load)."""
    return g.load(path, **kw)


def library_save(g: Any, path: str, header: dict | None = None) -> dict:
    """Gamma g written to a library= save (gamma.Gamma.save)."""
    return g.save(path, header=header)


def replace(src: str | Path, dst: str | Path) -> None:
    """A checked save's temporary file moved over the save (os.replace)."""
    os.replace(src, dst)


# ---------------------------------------------------------------- reads during play
def resolve(ag: Any, lib: Any, key: str, role: str, sig: tuple) -> list | None:
    return _lineage().resolve(ag, lib, key, role, sig)


def resolve_memo(ag: Any, lib: Any, mkey: tuple, atoms: dict) -> tuple | None:
    return _lineage().resolve_memo(ag, lib, mkey, atoms)


def resolve_bs(ag: Any, lib: Any, skey: tuple, atoms: dict) -> tuple | None:
    return _lineage().resolve_bs(ag, lib, skey, atoms)


def recorded_whole(mkey: tuple) -> bool:
    return _lineage().recorded_whole(mkey)
