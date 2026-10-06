"""Lit atoms -> candidate molecules via the RECIPES (F162: the recipes, not the domain adjacency
graph, are the atom->molecule composition). Parses ATOMS.md's recipe tables into {molecule ->
ingredients} and, given the atoms a mutation lit (detectors.py), returns the molecules whose recipe
those atoms COVER -- the composition the lit cues map to. Nothing invented: every molecule and its
recipe is the closure's own; this only reads them.

The layer above detectors: detectors light the ARC-level atoms (Translate, Rotate...), each itself a
recipe in ATOMS.md; the composer finds the molecules those compose into (Orbit = Rotate+Translate).
An ingredient the board never lights (Lev, Su...) simply keeps its molecule off the candidate list,
so the closure filters itself to what the game supports -- no ARC judgement here.

CUE_BOUNDARY IS RETIRED AND THIS MODULE MAY NOW REACH THE BETTING PATH -- reviewer, 2026-09-22.
This paragraph used to read *a CUE module, never imported by the betting path*. The rule's only
stated premise was §12.3's *reaching is the only evidence the composition system works*, and Isaiah
superseded that clause on 2026-09-19: the evidence moved to OOD composition, so an instrument on the
training side cannot consume the measurement. Re-scoped by INPUT PROVENANCE instead of module name
-- this module reads `ATOMS.md` and nothing else, no board and no answer key. `mapping` stays
blocked (it imports `reverse_engineer`), and KEY_BOUNDARY is untouched.

**AND `F165`'s *0 molecules on all 25* WAS MEASURED THROUGH THAT WALL, so it reads UNTESTED rather
than negative.** See also `candidates`: the exact-cover test is a second, independent reason that
zero was the only available answer.

ISAIAH, 2026-09-22 -- THIS IS THE COMPOSER THE AGENT KEEPS. `gamma.enumerate_closure` (the
type-walk) is to be ported from and then deleted, once the route chart holds.
"""

from __future__ import annotations

import functools
import os
import re
import sys
from dataclasses import dataclass

sys.dont_write_bytecode = True

# THE SEED IS READ FROM BESIDE THIS FILE, NOT FROM WHEREVER THE PROCESS STARTED -- 2026-10-06.
# Kaggle runs main.py from another directory; a cwd-relative open fails there. The
# recorded provenance keeps the repo-relative path.
_HERE = os.path.dirname(os.path.abspath(__file__))

_ATOMS_MD = "docs/library-closure/ATOMS.md"


UNKNOWN = "?"          # a junction whose bond the GROUND has not settled yet

# THE SEVEN BONDS PLUS NEGATION (OPERATORS.md). Isaiah, 2026-09-22: **`+` IN THE RECIPE LIST IS A
# PLACEHOLDER** -- any of these may be the real one, and the ground settles which. So a recipe is a
# FAMILY of candidates, one per bond reading, not a single composition.
BONDS = ("+", "→", "⇒", "∥", "−", "≡", "⋛")


@dataclass(frozen=True)
class Bonded:
    """5.9.3. `Node = Term | Bonded`. A junction, with its own standing.

    **`Term` IS KEPT AS THE CHAIN CASE AND WRAPPED, NOT REPLACED.** `Term` already is the `->`
    chain and ~24% of recipes need nothing more, so replacing it would be a rewrite in exchange
    for nothing -- and every existing `Term` consumer stays untouched.

    **EACH JUNCTION CARRIES ITS OWN `standing` AND SETTLES INDEPENDENTLY.** One standing for a
    whole tree would let a confirmed junction be demoted by a sibling's refutation.

    `standing` is left UNTYPED and defaults to `None` DELIBERATELY: the real one is
    `gamma.Standing`, and importing `gamma` here would put a domain module inside the composer.
    The caller supplies it.
    """
    bond: str
    left: object
    right: object
    standing: object = None
    origin: str = UNKNOWN


def bind(bond: str, left: object, right: object, standing: object = None,
         origin: str = UNKNOWN) -> Bonded:
    """5.9.2. **ONE constructor with the BOND AS A PARAMETER** -- Isaiah's item 6.

    Not eight functions. A recipe is a FAMILY of candidates, one per bond reading, and the
    ground settles which -- so the bond has to be a value that can vary, never a choice baked
    into which function was called.
    """
    if bond not in BONDS and bond != UNKNOWN:
        raise ValueError(f"{bond!r} is not one of {BONDS} nor UNKNOWN")
    return Bonded(bond, left, right, standing, origin)



def render_node(node: object) -> str:
    """ONE LINE FOR A LIT TREE. §12.2: the thing it holds is the sentence it says.

    **AN UNKNOWN JUNCTION PRINTS AS `?` AND THAT IS THE POINT, NOT A PLACEHOLDER IN THE OUTPUT.**
    A recipe's junction is a HYPOTHESIS the ground settles -- Isaiah: *`+` in the recipe list is
    a PLACEHOLDER* -- so a renderer that picked a bond to show would be supplying the meaning the
    whole design refuses to supply. `rotate ? translate` says exactly what is known: these two,
    bonded somehow.

    A settled junction prints its own bond (`rotate → translate`) with no change here, because
    the bond is a FIELD rather than a choice baked into the renderer.

    Leaves are rendered by their own `name` where they have one, so a `Term` prints as the chain
    it is. **No import of `gamma`** -- that would put a domain module inside the composer.
    """
    if isinstance(node, Bonded):
        return f"({render_node(node.left)} {node.bond} {render_node(node.right)})"
    return getattr(node, "name", str(node))


def junctions(node: object) -> tuple:
    """Every junction in the tree as `(bond, rendered)`. UNKNOWN ones are the open hypotheses,
    and counting them is how *what does this molecule still owe* gets answered without guessing
    at any of them."""
    if not isinstance(node, Bonded):
        return ()
    return ((node.bond, render_node(node)),) + junctions(node.left) + junctions(node.right)


def node_length(node: object) -> int:
    """A molecule costs what its parts cost, plus one per junction.

    The junction is charged because it is a CLAIM -- *these two are bonded* -- and the bargain
    prices claims. `Term` carries its own length and is asked for it rather than re-counted.
    """
    if isinstance(node, Bonded):
        return 1 + node_length(node.left) + node_length(node.right)
    n = getattr(node, "atoms", None)
    return len(n) if n is not None else 1


def _split_top(recipe: str) -> tuple[list[str], list[str]]:
    """Ingredients IN WRITTEN ORDER and the junction bonds between them.

    SPLITS ONLY OUTSIDE PARENTHESES, because `A(x)` is OPERATORS.md's qualifier form and the
    argument can itself contain a separator -- `Freq (high, >20kHz) + Refl` is TWO ingredients,
    and a naive `split("+")` on 713 parenthesised rows would shred them.
    """
    parts: list[str] = []
    bonds: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in recipe:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(depth - 1, 0)
        if depth == 0 and ch in BONDS:
            parts.append("".join(buf))
            bonds.append(ch)
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return [p.strip().strip("*").strip() for p in parts], bonds


@functools.lru_cache(maxsize=2)
def recipe_rows(path: str = _ATOMS_MD) -> dict:
    """{molecule -> {"ingredients": tuple IN ORDER, "junctions": tuple, "as_written": str}}.

    **ORDER IS KEPT AND THE BOND IS NOT INVENTED** -- the two halves of Isaiah's 2026-09-22 ruling.

    WHAT THE PREVIOUS PARSE LOST, AND IT WAS THE ONLY THING THERE WAS TO LOSE. It built a
    `frozenset`, which discards the written order of the ingredients. **Measured over ATOMS.md's
    3,495 table rows: the recipe column contains `+` 4,294 times, `>` 5 times, `=` once, and the
    seven unicode bonds effectively never.** So there is no ORDERED bond in the file to preserve --
    `+` is not merely the commonest, it is the only thing ever written. The order of the
    INGREDIENTS is therefore the whole of the recoverable signal, and the frozenset threw it away.

    **EVERY JUNCTION IS THEREFORE `UNKNOWN`, INCLUDING THE ONES WRITTEN `+`.** A `+` in the file is
    the corpus declining to say, not the corpus saying "conjunction" -- reading it as a claim is
    what made `Translate` a single composition instead of a family. The ground settles each
    junction, independently, via `Standing`; `n` ingredients have `n-1` of them.
    """
    out: dict = {}
    with open(path if os.path.isabs(path) else os.path.join(_HERE, path),
              encoding="utf-8") as fh:
        for lineno, ln in enumerate(fh, 1):
            m = re.match(r"\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$", ln)
            if not m:
                continue
            name = m.group(1).strip().strip("*").strip()
            recipe = m.group(2).strip().strip("*").strip()
            if not any(b in recipe for b in BONDS):
                continue
            ings, _written = _split_top(recipe)
            if name and all(ings) and len(ings) > 1:
                out[name] = {"ingredients": tuple(ings),
                             "junctions": (UNKNOWN,) * (len(ings) - 1),
                             "as_written": recipe,
                             # 5.9.4 names it and the row did not carry it. Provenance is what
                             # keeps the ablation partition reconstructible -- what was SEEDED
                             # apart from what the ground settled -- and it cannot be rebuilt
                             # afterwards from a row that never recorded where it came from.
                             "provenance": f"seed:{path}:{lineno}"}
    return out


def light(row: dict, standing=None) -> object:
    """5.9.4, the AFTER-LIGHTING shape: a recipe row -> a `Node` tree, **junctions still
    UNKNOWN**, each junction with its own fresh standing.

    **THE JUNCTIONS STAY UNKNOWN AND THAT IS THE WHOLE POINT.** `recipe_rows` already refuses to
    read the `+` in the file as a bond -- Isaiah, 2026-09-22: *`+` in the recipe list is a
    PLACEHOLDER* -- so lighting must not quietly supply one either. A recipe becomes a FAMILY of
    candidates and the GROUND settles each junction, which is `settle` and is the next item.

    Left-nested, matching `as_written` order: `a ? b ? c` lights as `((a ? b) ? c)`. Ordering is
    the recipe's own and is not a claim about associativity -- when a junction settles to a bond
    that associates differently, the tree is rebuilt rather than re-read.

    `standing` is a FACTORY (called per junction) rather than one object, because 5.9.3 requires
    each junction to settle independently and a shared instance would couple them.
    """
    ings = row["ingredients"]
    if len(ings) < 2:
        raise ValueError(f"a recipe needs two ingredients to have a junction: {ings}")
    node: object = ings[0]
    for right in ings[1:]:
        node = bind(UNKNOWN, node, right,
                    standing() if standing else None, row.get("provenance", UNKNOWN))
    return node


# WHAT A DELTA MUST CARRY FOR EACH TEST (5.4's table). A test whose quantity is absent returns
# None AND NAMES THE QUANTITY -- reviewer's pre-registration: *that is a finding about perception,
# not a licence to infer.* `None` IS NOT A SOFT FALSE: a bond not yet decidable on this delta must
# never be counted as refuted, or a quiet frame eliminates a reading.
NEEDS = {
    "+":  "order -- the SEQUENCE of changes within and across a frame",
    "→": "order -- the SEQUENCE of changes within and across a frame",
    "∥": "history -- a frame where one ingredient failed and the result still occurred",
    # PUBLISHED 2026-09-23 by `tether.Agent._delta`. The text read "computed in `_present` and
    # UNPUBLISHED" and that was the gap this table existed to name -- it is closed, and leaving
    # the old wording would have made a REASON STRING lie every time a junction went undecided.
    "−": "gone -- a value->null transition, published by `Agent._delta`",
    "⇒": "came -- a null->value transition, published by `Agent._delta`",
    "⋛": "magnitudes -- two changed slots' values, which the delta DOES carry",
}


def settle(bond: str, left: object, right: object, delta: dict) -> tuple:
    """5.9.2 / item 4. `(verdict, why)` where verdict is True | False | **None**.

    **`None` IS THE THIRD ANSWER AND IT IS NOT A SOFT FALSE.** A junction that this delta cannot
    decide stays UNKNOWN. Counting it as refuted would let a quiet frame eliminate a reading --
    the same error as reading a dead window as a zero.

    **`≡` IS NOT HERE, DELIBERATELY** (reviewer, ruling 4): it is a statement about the
    LIBRARY -- *two names, one referent* -- not about the board, and asking the board a question
    it cannot answer is how a reading gets invented.
    """
    if bond not in NEEDS:
        return (None, f"{bond!r} has no test: not one of the six")
    if bond == "⋛":
        # I WROTE `a > b or a < b` HERE AND IT IS A TEST THAT FAKES A PASS. It is True whenever
        # two values DIFFER, so it would mark nearly every junction a magnitude comparison --
        # and *two values differing is not evidence the junction IS about which is larger*.
        # Isaiah: never stub anything that would fake a pass. An over-accepting test is worse
        # than a missing one, because it produces confirmations nobody asked whether to trust.
        vals = delta.get("values") or {}
        a, b = vals.get(left), vals.get(right)
        if a is None or b is None:
            return (None, "magnitudes -- the delta carries no value for one operand")
        return (None, f"magnitudes {a} vs {b} are READABLE, and no DISCRIMINATING test is "
                      f"written: a difference does not establish the bond is a comparison")
    have = delta.get(bond_field(bond))
    if not have:
        return (None, NEEDS[bond])
    return (None, f"{NEEDS[bond]} -- present but no test is written yet")


def bond_field(bond: str) -> str:
    """the delta key each bond's test reads. Named apart so a missing FIELD and a missing TEST
    are distinguishable in the report -- they have different repairs."""
    return {"+": "order", "→": "order", "∥": "history",
            "−": "gone", "⇒": "came", "⋛": "values"}.get(bond, "")


def settle_tree(node: object, delta: dict) -> dict:
    """Walk a lit tree and try every junction. **NO JUNCTION IS FIXED WITHOUT GROUND EVIDENCE**
    (reviewer, pre-registration 3): UNKNOWN stays UNKNOWN until a delta decides it, and a decided
    bond is written to the RUNTIME layer with provenance DERIVED-BY-GROUND -- never to the seed.

    Returns the tally rather than a mutated tree: `Bonded` is frozen, and the isomer case --
    **two readings of the same junction both supported** -- is a COUNT, not a choice to make here.
    """
    decided, undecided, why = 0, 0, []
    stack = [node]
    while stack:
        n = stack.pop()
        if not isinstance(n, Bonded):
            continue
        supported = [b for b in BONDS if b != "≡"
                     and settle(b, n.left, n.right, delta)[0] is True]
        if supported:
            decided += 1
            if len(supported) > 1:
                why.append(f"ISOMER: {n.left}/{n.right} supports {supported}")
        else:
            undecided += 1
            # **THE REASON MUST NAME THE BOND WHOSE QUANTITY WE ACTUALLY HAVE.** This reported
            # `BONDS[0]`'s reason unconditionally -- always `+`, always *order -- the SEQUENCE
            # of changes*. So once `came`/`gone` were published the tally still said the delta
            # lacked ORDER, when the truth had become *the quantity is carried and no test is
            # written*. `bond_field` is named apart precisely so a missing FIELD and a missing
            # TEST stay distinguishable, and this line was collapsing them again one level up.
            have = [b for b in BONDS if b != "≡" and delta.get(bond_field(b))]
            why.append(settle(have[0] if have else BONDS[0], n.left, n.right, delta)[1])
        stack += [n.left, n.right]
    return {"decided": decided, "undecided": undecided, "why": why}


def candidates(lit: set, path: str = _ATOMS_MD, partial: bool = False) -> list[dict]:
    """Molecules whose recipe the lit atoms cover. Ranked by recipe size: a longer covered recipe
    is a more specific match.

    **`covered` AND `size` ARE ALWAYS REPORTED, WHICH THEY WERE NOT, BECAUSE THE EXACT-COVER TEST
    IS THE LIKELIEST REASON `F165` READ ZERO.** The default is unchanged -- `ingredients <= lit`,
    every ingredient lit -- and that is an ALL-OR-NOTHING test against **2,669 distinct ingredient
    names**, while today's perception lights **11**. A 3-ingredient recipe then needs the lit set
    to contain exactly its triple, so a zero is what this returns almost regardless of whether the
    pipeline works. **F165's *0 molecules on all 25* cannot separate "the recipe layer is inert"
    from "nothing could ever have been covered", and the coverage fraction is the quantity that
    separates them.** Published, not acted on.

    `partial=True` admits a recipe the lit atoms cover in PART, which is what the bargain's
    `cost(phi) + left(R, phi) < cost(R)` already licenses -- a term that explains some of the
    residual is priced, not refused. OFF by default: whether partial cover is the right admission
    rule is a ruling, not a parse detail.
    """
    # **THE JOIN IS NORMALISED, AND A CASE-SENSITIVE ONE WAS RETURNING ZERO BY CONSTRUCTION.**
    # The corpus capitalises ingredients (`Contact`, `Reflect`, `Stability`) and the registry
    # lower-cases atoms (`contact`, `reflect`, `stability`), so `i in lit` matched NOTHING --
    # measured 0 of 61 agent atoms against 2,669 ingredient names, on both exact and partial
    # cover. Normalised it is 13, covering up to 10 recipes each.
    #
    # **AND THE CORPUS IS INCONSISTENT WITH ITSELF, WHICH IS WHAT MAKES THIS A JOIN DEFECT
    # RATHER THAN A CONVENTION MISMATCH: `Sign` and `SIGN` are both present.** No single casing
    # rule on either side would have joined them; only normalising does.
    #
    # `ATOMS.md` IS READ-ONLY SEED, so the repair belongs here and could not have gone there.
    def _norm(x: str) -> str:
        return re.sub(r"[^a-z0-9]", "", x.lower())

    lit = {_norm(x) for x in lit}
    hits = []
    for n, r in recipe_rows(path).items():
        ing = r["ingredients"]
        hit = sum(1 for i in ing if _norm(i) in lit)
        if hit == len(ing) or (partial and hit):
            # LIT, as 5.9.4's after-lighting shape. Added as a KEY rather than by changing
            # the return shape: `mapping.py` and the `__main__` demo both read `molecule` off
            # these rows, and a candidate is exactly what "lit" means -- its ingredients are
            # covered by this frame. Junctions stay UNKNOWN; the ground settles them.
            hits.append({"molecule": n, "recipe": list(ing), "size": len(ing),
                         "junctions": r["junctions"], "covered": hit,
                         "coverage": round(hit / len(ing), 3),
                         "node": light(r), "provenance": r.get("provenance", UNKNOWN)})
    return sorted(hits, key=lambda d: (-d["coverage"], -d["size"], d["molecule"]))


def bond_report(lit: set, delta: dict, path: str = _ATOMS_MD) -> str:
    """The reviewer's pre-registered item-4 report: junctions decided / undecided BY BOND, how
    many decisions this delta supports, and **how often two readings of the same junction are
    both supported** -- the isomer case, which is the interesting failure.

    It is the consumer `settle_tree` needs, and it is also the deliverable: a report that reads
    all-undecided is a statement about what PERCEPTION does not carry, with the missing quantity
    named per junction rather than summarised as a rate.
    """
    cands = candidates(lit, path)
    dec = und = iso = 0
    missing: dict[str, int] = {}
    for c in cands:
        t = settle_tree(c["node"], delta)
        dec += t["decided"]
        und += t["undecided"]
        for w in t["why"]:
            if w.startswith("ISOMER"):
                iso += 1
            else:
                missing[w.split(" -- ")[0]] = missing.get(w.split(" -- ")[0], 0) + 1
    out = [f"  BOND REPORT over {len(cands)} lit recipes",
           f"    junctions decided    {dec}",
           f"    junctions undecided  {und}",
           f"    isomers (two readings both supported)  {iso}"]
    for q, n in sorted(missing.items(), key=lambda kv: -kv[1]):
        out.append(f"      undecided for want of {q:10s} {n}")
    return "\n".join(out)


if __name__ == "__main__":
    import json
    for lit in ({"Rotate", "Translate"}, {"Rotate", "Translate", "Scale"}, {"Recolour"}):
        print(sorted(lit), "->", json.dumps([c["molecule"] for c in candidates(lit)]))
    # ITEM 4's report. An EMPTY delta is the honest default here: the point of the report is
    # WHICH QUANTITY each junction wants, and a hand-made delta would only show that a delta I
    # invented decides the junctions I aimed it at.
    print(bond_report({"Ct", "Co", "Contact", "Bind", "So", "Lev", "Collide"}, {}))
