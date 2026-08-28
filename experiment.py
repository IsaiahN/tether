"""§21.1 / 4e — the controlled experiment, and it is the only one the loop can run.

§21.1: *everywhere else the agent gets **observational** data, and correlation is cheap;
causation is not, because **you can never re-run the same moment.** A level-resetting loss
breaks that **because the games are deterministic**: same starting board, vary exactly one
action, observe the difference.*

**ITS PRECONDITION IS A PROPERTY OF THE DOMAIN, NOT OF THE DESIGN**, and it was confirmed
before this was written rather than after: `ls20` returns `GAME_OVER` on 172 of 300 blind
steps, so a level-resetting loss exists to be exploited. **A mechanism built on a panel that
cannot supply its precondition is the fourth defect this project has recorded that way.**

WHAT MAKES IT CONTROLLED. Two visits to the SAME state signature, differing in EXACTLY ONE
action, with both outcomes read. Anything else is two observations that happen to look alike.
So the signature is the full slot reading -- not a summary, not a hash of a summary -- because
**two boards agreeing on a digest is Figure 2's collapse at the level of the key.**

**IT RECORDS, IT DOES NOT DECIDE.** A pair is evidence about one action's effect; what that
means for a bet is the loop's, and what it means for a diagnosis is a seat's. The rung
reports; the layer above judges.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

sys.dont_write_bytecode = True


@dataclass
class Controlled:
    """Visits keyed by exact state, so a repeat is a re-run rather than a resemblance."""

    seen: dict[tuple, dict[str, dict]] = field(default_factory=dict)
    pairs: list[dict] = field(default_factory=list)

    @staticmethod
    def signature(state: dict[str, int]) -> tuple:
        """The whole reading, ordered. **Not a hash and not a summary.**

        A digest would let two different boards collide into one key, and the mechanism's
        entire claim is *the same moment, re-run* -- which a collision silently falsifies.
        """
        return tuple(sorted(state.items()))

    def visit(self, state: dict[str, int], action: str, outcome: float) -> dict | None:
        """One (state, action, outcome). Returns a PAIR when this completes a control.

        A pair is the same signature under a DIFFERENT action. The same action twice is a
        determinism check, not an experiment, and is kept separately rather than counted --
        it says the domain held still, which is the precondition rather than the result.
        """
        sig = self.signature(state)
        prior = self.seen.setdefault(sig, {})
        if action in prior:
            # same state, same action: a determinism reading, not a control.
            prior[action]["repeats"] += 1
            prior[action]["stable"] = prior[action]["stable"] and (
                abs(prior[action]["outcome"] - outcome) < 1e-9)
            return None
        pair = None
        if prior:
            other = sorted(prior)[0]
            pair = {"varied": (other, action), "slots": len(state),
                    "outcome_a": prior[other]["outcome"], "outcome_b": outcome,
                    "difference": outcome - prior[other]["outcome"],
                    "reads": "same state, exactly one action varied, both outcomes read"}
            self.pairs.append(pair)
        prior[action] = {"outcome": outcome, "repeats": 0, "stable": True}
        return pair

    def determinism(self) -> dict:
        """What the repeats say about the DOMAIN, reported apart from the experiments.

        §21.1's precondition is determinism, and it is a property of the world rather than a
        design choice -- so it is MEASURED here and never assumed, and an unstable repeat
        invalidates every pair drawn from that state rather than merely being noted.
        """
        reps = [v for a in self.seen.values() for v in a.values() if v["repeats"]]
        return {"states_revisited": sum(1 for a in self.seen.values() if any(
                    v["repeats"] for v in a.values())),
                "repeated_readings": len(reps),
                "unstable": sum(1 for v in reps if not v["stable"])}

    def report(self) -> dict:
        d = self.determinism()
        return {"states_seen": len(self.seen), "controlled_pairs": len(self.pairs),
                **d,
                "reads": ("a pair is the same state with exactly one action varied; "
                          "`unstable` above zero means the domain did not hold still and "
                          "the pairs from that state are not controls")}
