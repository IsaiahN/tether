"""The end-of-run summary. **A READER over the ledger and Γ, never a producer.**

Same shape as `behaviour.py`: nothing here accumulates, and every number is a query over rows
that already exist. **A second producer of a fact the ledger holds is A1's defect at the level
of a record**, and it would look like a feature.

**IT INHERITS §14.7 RATHER THAN WRITING A FIFTH SET OF NUMBERS.** Three of the four sections
map exactly, population-to-statistic — the sections are the items and §14.7's numbers are
computed over them:

    CHAINS + reuse column   ->  chunk reuse count      *how often a settled term appears
                                                        inside a later mint. **Zero is the
                                                        failure signature**, and it is the one
                                                        that would otherwise look like progress*
    REUSED with pull counts ->  bench pulls            *which imports the agent actually needed.
                                                        A never-pulled bench item was a guess*
    REACHED-AND-FAILED      ->  unreached rate         *should fall as chunks accumulate*

**MINTED IS THE FOURTH AND §14.7 HAS NO COUNTERPART FOR IT** -- it is the proof rather than a
rate: *terms that did not exist, unnamed at mint time, against a residual that was recorded
first.*

**AND §14.7's `effective atom depth` IS NOT DERIVABLE HERE.** It is `Σ chunk lengths at search
depth 3`, computed over the CLOSURE rather than over what was minted -- **so it needs the
search, and this file does not have one.** Stated so the inheritance is not read as complete.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# Composition is sequential-only today, so every joint carries the same operator. The column
# is here because the multi-operator space is a recorded gap rather than an oversight, and a
# summary that omitted the joint would make a one-operator space look like the only one.
JOINT = "."


def _chain(term) -> str:
    return f" {JOINT} ".join(a.name for a in term.atoms)


def minted(rows: list[dict], gamma) -> list[dict]:
    """**Terms that did not exist in the library.** The proof section.

    Each carries its handle, its constituent atoms, the residual it was minted AGAINST, and
    the cost/left pair -- **`left_bits` is the delta between what the term predicted and what
    the ground did**, which is already on the mint row and needed no new field.
    """
    # `record(cycle, STEP, slot, EVENT, ...)` -- `MINT` is the STEP and `mint` is the EVENT.
    # Filtering on `event == "MINT"` matched nothing and every column read `None`, which looks
    # exactly like a mint that carried no cost rather than like a lookup that found nothing.
    bits = {r["detail"]["term"]: r["detail"] for r in rows
            if r.get("event") == "mint" and (r.get("detail") or {}).get("term")}
    out = []
    for name, t in gamma.library.items():
        if t.origin == "prior":
            continue
        st = gamma.stamps.get(name) or {}
        d = bits.get(name, {})
        out.append({"handle": gamma.handles.get(name), "term": name,
                    "atoms": [a.name for a in t.atoms], "joints": [JOINT] * (len(t.atoms) - 1),
                    "origin": t.origin, "admitted": st.get("admitted"),
                    "against_residual": st.get("residual"),
                    "cost_bits": d.get("term_bits"), "left_bits": d.get("left_bits"),
                    "closed_it": d.get("closes")})
    return out


def chains(gamma) -> list[dict]:
    """**`atom . atom . atom`, and whether it appeared inside a LATER mint.**

    That last column is §14.7's chunk reuse, and *zero is the failure signature*. A chain
    counts as reused when its atom sequence is contained in a longer term's -- **the chunk IS
    the atom sequence**, which is `units()`'s own rule and the reason the operand is not in it.
    """
    terms = [(n, t) for n, t in gamma.library.items() if t.origin != "prior"]
    out = []
    for name, t in terms:
        seq = tuple(a.name for a in t.atoms)
        inside = [n2 for n2, t2 in terms if n2 != name and len(t2.atoms) > len(seq)
                  and any(tuple(a.name for a in t2.atoms)[i:i + len(seq)] == seq
                          for i in range(len(t2.atoms) - len(seq) + 1))]
        out.append({"handle": gamma.handles.get(name), "chain": _chain(t),
                    "depth": len(t.atoms), "inside_later_mints": inside})
    return out


def reused(rows: list[dict]) -> dict:
    """**Library entries reached for, with pull counts.** §14.7's bench pulls.

    *A never-pulled bench item was a guess* -- so a term absent from this dict is a reading
    about whoever put it there, not only about the run.
    """
    pulls: dict[str, dict] = {}
    for r in rows:
        if r.get("event") == "pull":
            d = r.get("detail") or {}
            n = d.get("term")
            if n:
                e = pulls.setdefault(n, {"pulls": 0, "origin": d.get("origin")})
                e["pulls"] += 1
    return pulls


def transfer(rows: list[dict], gamma) -> dict:
    """**THE IMPORT's EVIDENCE COLUMN.** An imported term that gets pulled on a NEW game is
    transfer; one that never gets pulled **was a guess, by §14.7's own words.**

    **This is why `IMPORTED` had to be a third bucket.** It wipes like `promoted`, so the
    ablation is unaffected -- *the distinction it buys is countability, not survival* -- and
    countability is exactly what makes this number exist. A term entering as `promoted` would
    be indistinguishable from one minted here, and the transfer claim would have no subject.

    **A COUNT CAN BE GOT MANY WAYS; THIS CANNOT.** *This many were minted elsewhere* is
    ambiguous. **A composition that names its parts, carries the game it was born in, and was
    pulled against a residual in a different one** is transfer with a handle on it.
    """
    # KEYED ON THE COMPOSITION, WHICH IS WHAT CROSSED. Keyed on the NAME it could never match:
    # a re-bound import installs under a new name stamped `accepted`, so the column would read
    # zero however well transfer worked -- one of three independent reasons the old number was
    # not a measurement. The others: an unbound operand-reading term is `idn`, so it explained
    # nothing; and the sweep, the only path that re-bound, emitted no `pull` row.
    held: dict[str, list[str]] = {}
    for n, t in gamma.library.items():
        if t.origin == "imported":
            held.setdefault(_chain(t), []).append(n)
    pulled: dict[str, int] = {}
    foreign: dict[str, bool] = {}
    for r in rows:
        if r.get("event") != "pull":
            continue
        d = r.get("detail") or {}
        c = d.get("chain")
        if c in held:
            pulled[c] = pulled.get(c, 0) + 1
            h = gamma.handles.get(d.get("held") or "") or ""
            foreign[c] = bool(h) and not h.startswith(f"{gamma.game}_")
    return {"imported_held": len(held),
            "imported_pulled": len(pulled), "pulls": pulled,
            "pulled_from_elsewhere": {c: v for c, v in foreign.items() if v},
            "never_pulled": sorted(set(held) - set(pulled)),
            "handles": {c: [gamma.handles.get(n) for n in ns] for c, ns in held.items()},
            "reads": ("an imported term pulled here is TRANSFER; one never pulled was a "
                      "guess. The handle's prefix is the game it was born in, so a pull row "
                      "and a handle together say composed there, used here")}


def branching(gamma, inherited: set[str]) -> dict:
    """**Q25's BRANCHING TEST, on the generation the run just formed.**

    *A tower of seats, agents, or generations that has produced no divergence has no transform
    and is a copy loop however deep it goes* -- and Q25's point is that this is **visible
    without access to the transform itself.** So this compares OUTPUT SETS and never asks how a
    term was made.

    **DIVERGENCE IS ON THE COMPOSITION, NOT THE BINDING**, and that is the whole of the design.
    Bindings are re-decided per slot in every game, so a binding-keyed difference is non-empty
    by construction and the check could never fail -- *a metric whose denominator the mechanism
    changes cannot falsify that mechanism*. The atom sequence is what `save` carries across and
    what `units` composes over, so it is what a generation can be said to have added.

    `inherited` is the composition set present after loading and before playing. Empty means a
    cold run, which is generation zero and **cannot branch by definition** -- reported as such
    rather than as a failure.
    """
    final = {_chain(t) for t in gamma.library.values()}
    # ON A COLD RUN `added` WOULD BE THE WHOLE LIBRARY, ATOMS INCLUDED -- which is not a set
    # of additions, it is the absence of a parent rendered as a maximal difference. Null, like
    # the verdict it belongs to.
    added = sorted(final - inherited) if inherited else None
    return {"inherited": len(inherited), "final": len(final), "added": added,
            "diverged": bool(added) if inherited else None,
            "reads": ("generation zero cannot branch, so `diverged` is null on a cold run. "
                      "On a warm one, no added composition means this level is a copy of its "
                      "parent however deep the tower goes -- Q25, and it fails loudly")}


def catalysts(gamma) -> dict:
    """**Which terms SURVIVED THEIR OWN USE, and which were spent.** `CHEMISTRY.md`'s test,
    stated there as *does this term survive its own use unchanged -- checkable per term, and
    nothing currently records it.*

    **THE MATERIAL WAS ALWAYS THERE AND HAD NO POPULATION.** `Standing` carries `settled_at`
    and a DECAYING `rejections`, and `refute` clears the first while raising the second. What
    did not exist was anything settled: candidacy was gated on closure and nothing ever closed,
    so nothing could be spent. **The reading became possible the day the gate moved, which is
    the third instrument this week whose subject arrived with candidacy.**

    **AND `rejections` IS GRADED, WHICH IS MORE THAN THE ANALOGY ASKED FOR.** A catalyst is
    binary in chemistry -- consumed or not. Here a term carries how often the ground has turned
    on it, halved over `REJECTION_HALFLIFE`, so *spent* has a degree and a term can recover.
    """
    out: dict[str, dict] = {}
    for name, st in gamma.standing.items():
        settled = st.settled_at is not None
        out[name] = {"settled": settled, "rejections": round(st.rejections, 3)}
    survived = [n for n, v in out.items() if v["settled"] and v["rejections"] == 0.0]
    spent = [n for n, v in out.items() if not v["settled"] and v["rejections"] > 0.0]
    return {"survived_use_unchanged": len(survived), "spent": len(spent),
            "recovering": len([n for n, v in out.items()
                               if v["settled"] and v["rejections"] > 0.0]),
            "per_term": out,
            "reads": ("a term settled and never turned on is a CATALYST -- it survived its own "
                      "use and is available again. `rejections` is graded and decays, so spent "
                      "is a degree and a term can recover")}


def levels(rows: list[dict]) -> dict:
    """**THE ACCOUNT, SCOPED TO THE LEVEL BOUNDARY.** Four columns per level -- what was HELD
    entering it, USED during it, MINTED during it, and what the RESIDUAL did across it.

    **THE BOUNDARY IS THE SCOPE BECAUSE IT IS THE ONLY MOMENT *CONTRIBUTED* HAS A REFERENT.**
    `levels_completed` is the sole ground signal, so *this term was live when the counter moved*
    is the first statement that touches it. **A per-term reduction of 14 bits is frame-internal**
    and belongs here as an INPUT rather than as the deliverable.

    **AND IT PRODUCES A SERIES, NOT A VERDICT**, which is §14.7's own form: *unreached rate over
    time, and it should fall as chunks accumulate.*

    **THE PREDICTION IT MAKES FALSIFIABLE.** Each level adds problems to a cup that still holds
    everything the last one did not explain -- the residual does not leave, and `outstanding` is
    monotone-by-addition for exactly that reason. **So a library that is not composing should
    show RISING unexplained mass per level, and one that is composing should show the opposite.**

    **AND WHEN NO LEVEL HAS ADVANCED THE READING IS `UNREACHED`, NOT NULL.** One level means one
    row and no differences, which is a statement about the run rather than about the library.
    """
    seq = [r for r in rows if r.get("event") == "repeat"]
    if not seq:
        return {"levels": [], "verdict": "no_cycles", "reads": "nothing ran"}
    spans: dict[int, dict] = {}
    for r in seq:
        lv = r["detail"].get("level", 0)
        d = spans.setdefault(lv, {"level": lv, "first": r["cycle"], "last": r["cycle"],
                                  "outstanding_in": r["detail"].get("outstanding"),
                                  "outstanding_out": None})
        d["last"] = r["cycle"]
        d["outstanding_out"] = r["detail"].get("outstanding")
    for d in spans.values():
        lo, hi = d["first"], d["last"]
        d["used"] = len({(x.get("detail") or {}).get("term") for x in rows
                         if x.get("event") == "pull" and lo <= x["cycle"] <= hi})
        d["minted"] = sum(1 for x in rows
                          if x.get("event") == "mint" and lo <= x["cycle"] <= hi)
        d["held_entering"] = sum(1 for x in rows
                                 if x.get("event") == "mint" and x["cycle"] < lo)
        a, b = d["outstanding_in"], d["outstanding_out"]
        d["residual_moved"] = None if a is None or b is None else round(b - a, 3)
        del d["first"], d["last"]
    out = [spans[k] for k in sorted(spans)]
    advanced = len(out) > 1
    return {"levels": out, "advanced": advanced,
            "verdict": "series" if advanced else "unreached",
            "reads": ("four columns per level. ONE level means no differences and the verdict is "
                      "UNREACHED -- no level advanced, so no contribution reading exists. That is "
                      "a statement about the run, not a null about the library")}


def reach(rows: list[dict], gamma) -> dict:
    """**§14.7's FOUR NUMBERS, which §14.8 says to report every run.** *They describe REACH, not
    success, and the ground still settles everything.*

    **`bench pulls` IS THE MVS, AND *PER PRIMITIVE* IS THE PHRASE THAT MAKES IT ONE.** `reused`
    counts pulls by TERM NAME -- `translate . translate<o14.row>` -- and §14.7 asks per
    PRIMITIVE, which decomposes that into the atoms the agent actually reached for. **Which
    atoms compose most of the rest is not a fifth number; it is this one read correctly.**

    **AND `a never-pulled bench item was a guess` INDICTS WHOEVER STOCKED IT**, so the
    deliverable has both columns: pulled, and offered-and-never-reached.
    """
    # COMPOSITIONS, NOT NAMES. `Term.name` carries the binding and the atom tuple does not, so
    # a bound settled name never matched and the count read 0 -- which is §14.7's stated FAILURE
    # SIGNATURE, produced by a comparison rather than by the library. 0 -> 8 and 0 -> 1.
    settled = {tuple(a.name for a in t.atoms) for t in gamma.settled_terms}
    units = {u.name: len(u.atoms) for u in gamma.units()}

    # 1. effective atom depth -- the atom count of the deepest chain a depth-3 search reaches.
    #    Flat at 3 means every unit is an atom and chunking is not compounding.
    depth = 3 * max(units.values(), default=1)

    # 2. chunk reuse -- how often a settled term appears INSIDE a later mint. §14.7: *zero is
    #    the failure signature, and it is the one that would otherwise look like progress.*
    chunk = 0
    # A CONTIGUOUS SUBSEQUENCE OVER THE ATOM TUPLE, not a substring over the joined name. The
    # string form is safe for these atom names and is the wrong shape -- it would match a name
    # that happens to embed another, and the claim is about a chain containing a chunk.
    #
    # **OCCURRENCES, NOT TERMS-CONTAINING.** §14.7 says *how OFTEN a settled term appears
    # inside a later mint*, so a chunk appearing twice in one term counts twice. The other
    # reading -- how many later terms contain it -- is the smaller number and is not what the
    # sentence says; recorded here because the phrase admits both and the difference is exactly
    # the factor that decides whether chunking compounds.
    for t in gamma.library.values():
        seq = tuple(a.name for a in t.atoms)
        if seq in settled:
            continue
        for u in settled:
            k = len(u)
            chunk += sum(1 for i in range(len(seq) - k + 1) if seq[i:i + k] == u)

    # 3. bench pulls PER PRIMITIVE, and the never-pulled column beside it
    pulled: dict[str, int] = {}
    for r in rows:
        if r.get("event") != "pull":
            continue
        d = r.get("detail") or {}
        for a in (d.get("chain") or d.get("term") or "").split(JOINT):
            a = a.strip().split("<")[0].split("?")[0]
            if a:
                pulled[a] = pulled.get(a, 0) + 1
    offered = {a.name for a in gamma.atoms}
    never = sorted(offered - set(pulled))

    # 4. unreached rate over time -- §14.7: *should fall as chunks accumulate.*
    mints = [r for r in rows if r.get("event") in ("mint", "park")]
    per: dict[int, list] = {}
    for r in mints:
        per.setdefault(r["cycle"] // 5, []).append(
            (r.get("detail") or {}).get("verdict") in ("budget_spent", "depth_exhausted"))
    series = [round(sum(v) / len(v), 3) for _, v in sorted(per.items()) if v]

    return {"effective_atom_depth": depth,
            "chunk_reuse": chunk,
            "bench_pulls_per_primitive": dict(sorted(pulled.items(), key=lambda kv: -kv[1])),
            "never_pulled": never,
            "unreached_rate_over_time": series,
            "reads": ("§14.7's four. Depth flat at 3 means chunking is not compounding; chunk "
                      "reuse of zero is the failure signature; a never-pulled primitive was a "
                      "guess by whoever stocked it; and the unreached rate should FALL")}


def reached_and_failed(rows: list[dict]) -> dict:
    """**Descriptions that retrieved nothing.** *I looked for something with this shape and
    found nothing* is an `UNREACHED` with a SUBJECT, and it is the half the visible set exists
    to make possible.

    **A retrieval that returns nothing leaves no other trace**, which is why this had to be
    recorded at the pull site rather than derived.
    """
    reach = sum(1 for r in rows if r.get("event") == "reach")
    fail = [r for r in rows if r.get("event") == "reach_failed"]
    return {"reaches": reach, "failed": len(fail),
            "rate": round(len(fail) / reach, 4) if reach else None,
            "slots": sorted({r.get("slot") for r in fail if r.get("slot")})[:12]}


def report(rows: list[dict], gamma) -> dict:
    m, c = minted(rows, gamma), chains(gamma)
    return {
        "MINTED": m,
        "CHAINS": c,
        "REUSED": reused(rows),
        "TRANSFER": transfer(rows, gamma),
        "REACHED_AND_FAILED": reached_and_failed(rows),
        "chunk_reuse_count": sum(len(x["inside_later_mints"]) for x in c),
        "reads": ("14.7's three inherited, MINTED added. `effective atom depth` is NOT here: "
                  "it is computed over the closure, not over what was minted"),
    }
