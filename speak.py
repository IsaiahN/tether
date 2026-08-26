"""The builder: decision state -> language.

Reads the LEDGER only. The gate reads the world; neither reaches the other's sources.

Fixed tokens are the record; this is a rendering OF the record. Every sentence carries the
sequence numbers it was read from, so a claim can be checked line by line -- and a sentence
that traces to nothing is a defect, not a flourish. Compositional fluency in the library is
the target here; sounding human is not, and would be the failure signature.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True


def _zero(names: list[str]) -> str:
    return f"The guard at zero was {', '.join(names)}. " if names else ""


def _n(x: object, places: int = 1) -> str:
    try:
        return f"{float(x):.{places}f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return str(x)


def sentences(rows: list[dict]) -> list[tuple[list[int], str]]:
    """(source sequence numbers, sentence). Nothing is emitted that cites no row."""
    out: list[tuple[list[int], str]] = []
    for r in rows:
        seq, d, slot = r.get("seq"), r.get("detail", {}), r.get("slot")
        ev = r.get("event")

        if ev == "route" and d.get("bin") != "held":
            out.append(([seq], f"On {slot} I was wrong, and I read it as "
                               f"{d.get('bin')} -- {d.get('why_not')}."))
        elif ev == "mint":
            closes = d.get("closes")
            out.append(([seq], f"I offered `{d.get('term')}` for {slot}. It costs "
                               f"{_n(d.get('term_bits'))} bits and leaves "
                               f"{_n(d.get('left_bits'))} of the "
                               f"{_n(d.get('base_bits'))} that were unexplained, so the "
                               f"bargain pays." + ("" if closes else
                               " It pays and it does not close the gap, so the slot still "
                               "owes.")))
        elif ev == "park":
            g = d.get("guards", {})
            zero = [k for k, v in g.items() if not v]
            out.append(([seq], f"On {slot} I could not close it. I searched "
                               f"{d.get('candidates_seen')} compositions to depth "
                               f"{d.get('depth')} and none of them pays. "
                               f"{_zero(zero)}"
                               f"That is unreached at this budget, which is not a proof "
                               f"that it is unreachable. I need either a sharper instrument "
                               f"on what I can already see, or a primitive I do not have."))
        elif ev == "accept":
            out.append(([seq], f"`{d.get('term')}` is in the library for {slot}, stamped "
                               f"{d.get('origin')} at entry {d.get('seq')}. It is a "
                               f"candidate: nothing has settled it, so I will hold it and "
                               f"not cite it."))
        elif ev == "rebind":
            out.append(([seq], f"On {slot} the library already held `{d.get('term')}`. "
                               f"I re-fitted rather than minting; the library did not "
                               f"change."))
        elif ev == "settle":
            out.append(([seq], f"The ground settled `{d.get('term')}` on {slot}: it held "
                               f"on a transition it was never fitted to. It is accepted "
                               f"now, and may be cited."))
        elif ev == "probe":
            # WHAT THE PROBE DOES, not what it used to. It cited `probe_err`, a field
            # deleted with the EMA, and rendered "my own error is None"; and it described
            # perturbing, when the draw was always the default and the change is that the
            # model no longer gets to choose. Twice diverged from the mechanism.
            out.append(([seq], f"On {slot} nothing is live. Over {d.get('probe_n')} "
                               f"observations no slot carried mass, so my model explains "
                               f"everything I can currently see -- and an action I picked "
                               f"from that model could only confirm it. So I am not "
                               f"picking this one: the draw is uninformed, and what comes "
                               f"back is an ordinary observation."))
        elif ev == "unreached":
            # THE HARDEST THING THE AGENT CAN SAY, and it could not say it before: not
            # `I cannot explain this` but `there may be nothing here I can see`. The two
            # readings are indistinguishable from inside, and pretending otherwise would
            # be the confident half of exactly the failure this reports.
            out.append(([seq], f"I have drawn every action I was offered "
                               f"({', '.join(d.get('tried') or [])}) over "
                               f"{d.get('observations')} observations, and nothing in "
                               f"{', '.join(d.get('slots') or [])} has ever moved. Either "
                               f"this world is still, or what moves is not something I am "
                               f"built to see -- from here those are the same reading. The "
                               f"second is answered by a different set of slots, and I do "
                               f"not have a way to change mine."))
        elif ev == "refused":
            out.append(([seq], f"I did not act. The utterance did not compose: "
                               f"{d.get('reason')}."))
    return out


def account(rows: list[dict], limit: int | None = None) -> str:
    lines = [f"[{','.join(map(str, s))}] {t}" for s, t in sentences(rows)]
    if limit is not None:
        lines = lines[:limit]
    return "\n".join(lines)


def verify(rows: list[dict], said: list[tuple[list[int], str]]) -> dict:
    """Every sentence traces to a row that exists. A sentence citing nothing is a defect."""
    known = {r.get("seq") for r in rows}
    orphans = [t for s, t in said if not s or any(x not in known for x in s)]
    return {"sentences": len(said), "orphans": len(orphans),
            "traceable": not orphans, "examples": orphans[:2]}
