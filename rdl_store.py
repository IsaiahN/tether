"""RECURSIVE DIFFUSION LEARNING, PIECE 1: THE STORE (C1, C2, C3, C6).

Spec: docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md, Piece 1. Design: docs/05-RESEARCH/
40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md, constraints C1-C6 and the tier ladder.

A Preload is a HEAD START, never a verdict: a kind-level term in the agent's grammar with its
bonds, its refusal forms, the library entries it attaches to (by cluster) and the lower-tier
preloads it abstracts. It carries its stamp (C6: stage, tier, source with corpus, corpus sha,
parser, parser version). No field here means standing, and nothing in this module settles
anything (C3): "preloaded material has no standing until the board pays".

  head_start(p)  C1, form: False with the reason for a RECORDING -- a move list or action
                 sequence, an object name (o12), a coordinate, a solution. Fig 4 :22-24, the
                 membrane lets only methods cross.
  usable(p)      C2, usability: at least one bond AND at least one attach; anything else is
                 recorded, never offered (Fig 5 :70-72; Fig 12 :111, :140).
  load / dump    deterministic JSON (sorted keys, stable order, pid re-checked at load), a
                 header with the sources (file, bytes, sha256), the licences carried from the
                 inputs, the standing note and the readers.

No import of tether (spec). Python only, no network, no weights.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

STAGES = ("instance", "regularity", "abstraction", "core_rule")   # tier = index + 1
STANDING = "none (C3): preloaded material has no standing until the board pays"
KIND_RE = re.compile(r"^(wn|wn-group|card):\S")

# C1's recording shapes. Each is a FORM, never a vocabulary list of games: an object name is
# the observer's per-board id (o + digits); a coordinate is a number pair; a move list is two or
# more directions or ACTIONn steps in a row; a solution is a solution or answer key handed over.
_RECORDING = (
    ("object name", re.compile(r"(?<![A-Za-z0-9_])o\d+(?![A-Za-z0-9_])")),
    ("coordinate", re.compile(r"[(\[]\s*-?\d+\s*,\s*-?\d+\s*[)\]]")),
    ("coordinate", re.compile(r"\b(?:x|y|row|col)\s*[=:]\s*-?\d+", re.I)),
    ("action sequence", re.compile(r"\bACTION\d+\b(?:\s*[,;>→]+\s*\bACTION\d+\b)+")),
    ("action sequence", re.compile(r"\bACTION\d+\b")),
    ("move list", re.compile(
        r"\b(?:up|down|left|right)\b(?:\s*[,;>→]+\s*\b(?:up|down|left|right)\b)+", re.I)),
    ("move list", re.compile(r"\b(?:click|press)\s*\(\s*-?\d+", re.I)),
    ("solution", re.compile(r"\b(?:solution|answer key|solved board)\s*[:=]", re.I)),
)


def _plain(v: Any) -> Any:
    """Tuples to lists, recursively: the canonical JSON form of a field."""
    if isinstance(v, (tuple, list)):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    return v


def canonical(obj: Any) -> str:
    return json.dumps(_plain(obj), sort_keys=True, ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True)
class Preload:
    pid: str
    tier: int
    stage: str
    source: dict
    kind: str
    text: str
    bonds: tuple = ()
    refusal: tuple = ()
    attaches: tuple = ()
    parents: tuple = ()

    def body(self) -> dict:
        """Every field but pid: what the pid hashes."""
        d = asdict(self)
        d.pop("pid")
        return d


def pid_of(body: dict) -> str:
    """sha256[:16] of the canonical JSON of every field other than pid."""
    return hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()[:16]


def make(tier: int, source: dict, kind: str, text: str, bonds=(), refusal=(), attaches=(),
         parents=()) -> Preload:
    """The one constructor that computes the pid; the stage follows the tier (STAGES)."""
    body = {"tier": tier, "stage": STAGES[tier - 1], "source": dict(source), "kind": kind,
            "text": text, "bonds": tuple(tuple(b) for b in bonds), "refusal": tuple(refusal),
            "attaches": tuple(attaches), "parents": tuple(parents)}
    return Preload(pid=pid_of(body), **body)


def _strings(p: Preload) -> list[tuple[str, str]]:
    out = [("kind", p.kind), ("text", p.text)]
    out += [("bond", str(x)) for b in p.bonds for x in b[1:]]
    out += [("refusal", r) for r in p.refusal]
    return out


def head_start(p: Preload) -> tuple[bool, str]:
    """C1: (True, "") for a head start; (False, reason) for a recording or a malformed stamp."""
    if p.tier not in range(1, len(STAGES) + 1) or p.stage != STAGES[p.tier - 1]:
        return False, f"stage {p.stage!r} does not match tier {p.tier}"
    if not KIND_RE.match(p.kind):
        return False, f"kind {p.kind!r} is not kind-level (wn:, wn-group:, card:)"
    for where, s in _strings(p):
        for what, rx in _RECORDING:
            m = rx.search(s)
            if m:
                return False, f"recording ({what}) in {where}: {m.group(0)!r}"
    return True, ""


def usable(p: Preload) -> bool:
    """C2: offered only with at least one bond AND at least one attach; else recorded."""
    return bool(p.bonds) and bool(p.attaches)


def file_source(path: str | Path, name: str | None = None) -> dict:
    """A header source row: file, bytes, sha256."""
    raw = Path(path).read_bytes()
    return {"file": name or Path(path).name, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def dumps(preloads, header: dict) -> str:
    """The deterministic text: sorted keys, preloads ordered by (tier, kind, pid), one per line."""
    head = dict(header)
    head["standing"] = STANDING
    head.setdefault("readers", [])
    order = sorted(preloads, key=lambda p: (p.tier, p.kind, p.pid))
    rows = ",\n".join(canonical(asdict(p)) for p in order)
    return ('{"header":' + json.dumps(_plain(head), sort_keys=True, ensure_ascii=False, indent=1)
            + ',\n"preloads":[\n' + rows + "\n]}\n")


def dump(preloads, path: str | Path, header: dict) -> None:
    Path(path).write_bytes(dumps(preloads, header).encode("utf-8"))


def from_dict(d: dict) -> Preload:
    names = {f.name for f in fields(Preload)}
    kw = {k: d[k] for k in names}
    for k in ("bonds", "refusal", "attaches", "parents"):
        kw[k] = tuple(tuple(x) if isinstance(x, list) else x for x in kw[k])
    p = Preload(**kw)
    if pid_of(p.body()) != p.pid:
        raise ValueError(f"pid {p.pid} does not match its fields (kind {p.kind})")
    return p


def load(path: str | Path) -> list[Preload]:
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    return [from_dict(d) for d in doc["preloads"]]


def load_header(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)["header"]
