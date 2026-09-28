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

        # THE ACT SPACE, WHICH THE NARRATION COULD NOT SAY. `speak` is the agent's account
        # of itself and it cited 0 of 2 `PLAN` rows -- so every routine minted, run, exhausted
        # or refused was invisible to the one instrument whose whole job is saying why.
        # *A change that makes the agent better and its reasoning unreadable has destroyed the
        # instrument*, and a new SPACE with no sentences is that at the largest scale available.
        # THE INTENT, AND IT IS THE CLEAREST THING THE AGENT CAN SAY ABOUT ITSELF NOW.
        # `docs/ACTION_INTERFACE_PLAN.md`: the agent reasons in what it WANTS and the interface
        # translates. **So the narration says the want and the translation separately** -- which
        # is the seam made legible rather than merely built. A sentence naming only the button
        # would be the old account of a new mechanism.
        if ev == "intent":
            want, why = (list(d.get("reads") or ("", "")) + ["", ""])[:2]
            out.append(([seq], f"On {slot} I wanted: {want}. I did not choose an action for "
                               f"that -- the interface did, and its reason was: {why}."))
        elif ev == "routine":
            out.append(([seq], f"On {slot} I committed to a plan: `{d.get('routine')}`. It "
                               f"costs {_n(d.get('cost'))} bits and leaves {_n(d.get('left'))} "
                               f"of the {_n(d.get('base'))} the goal residual owed, so the "
                               f"bargain pays. I chose it from {d.get('considered')} shapes, "
                               f"and its route is what I have observed my own actions do."))
        elif ev == "routine_end":
            why = {"done": "the guard I set held, so the plan finished",
                   "exhausted": "I spent the whole budget and the guard never held, which "
                                "refutes the plan rather than the goal",
                   "blocked": "I could not read the guard, which is not the same as the "
                              "guard being false",
                   "unadvertised": "it named an action this level does not offer, so it "
                                   "failed its guard rather than crashing"}
            tail = ("" if d.get("status") != "refuted" else
                    f" I filed that against the plan at strength {_n(d.get('rejections'))}, "
                    f"and it reopens if the goal residual rises above "
                    f"{_n(d.get('reopens_above'))}.")
            out.append(([seq], f"On {slot} the plan `{d.get('routine')}` ended: "
                               f"{why.get(d.get('outcome'), d.get('outcome'))}." + tail))
        elif ev == "routine_cut":
            out.append(([seq], f"On {slot} I considered `{d.get('routine')}` and refused it: "
                               f"{_n(d.get('cost'))} bits of plan plus {_n(d.get('left'))} left "
                               f"unreached is not worth the {_n(d.get('base'))} it owed. It "
                               f"reaches {d.get('reach')} of {d.get('unsat')}."))
        elif ev == "routine_refused":
            out.append(([seq], f"On {slot} I formed no plan: {d.get('reason')}."))
        elif ev == "committed_on_accumulation":
            # THE AGENT ACTING WITHOUT HAVING PAID. This is the sentence that must exist or
            # the narration cannot tell a LEAN from a purchase -- and a lean that goes wrong
            # has to be a finding, which means the account has to say it leaned and why.
            _v = d.get("vector") or {}
            _why = ", ".join(f"{k} {v:+g}" for k, v in _v.items() if v)
            out.append(([seq], f"On {slot} the bargain refused `{d.get('routine')}` and I "
                               f"took it anyway: the weight behind it reached "
                               f"{d.get('total')} against a bar of {d.get('threshold')}, "
                               f"lowered by {d.get('idle')} cycles without committing to "
                               f"anything. What carried it: {_why or 'nothing nameable'}."))
        elif ev == "reach_tested":
            # THE AGENT MARKING ITS OWN ESTIMATE AGAINST WHAT HAPPENED. Without a sentence the
            # upgrade from ASSUMED to TESTED would be invisible in the account, and it is the
            # only place the record says whether a plan's claimed reach was ever borne out.
            out.append(([seq], f"On {slot} the plan `{d.get('routine')}` ended "
                               f"{d.get('ending')} having emitted {d.get('emitted')} "
                               f"action(s), so its reach is now {d.get('verdict')} rather "
                               f"than assumed."))
        elif ev == "routine_inert":
            # THE AGENT REFUSING ITS OWN PLAN FOR A REASON THAT IS NOT PRICE. Without a
            # sentence the narration would show a cycle where candidates were composed and
            # none survived, with no account of why -- and the reason here is the most
            # interesting one it can give: *I would have finished before I started.*
            out.append(([seq], f"On {slot} I dropped {d.get('dropped')} of "
                               f"{d.get('considered')} plans before pricing them: each would "
                               f"have ended before acting, because the condition it stops at "
                               f"is already true."))
        elif ev == "split_refused":
            # **THE EVENT THAT COULD NOT FIRE UNTIL TODAY, AND THE NARRATION WENT QUIET THE
            # MOMENT IT COULD -- 2026-09-25.** `split_refused` exists so the several exits
            # of `_goal_split` stop being reported as one message, and `_mint_routine` was
            # printing *coverage incomplete, or every action ties* for all of them. The row is
            # the finer record and it had no sentence, so the one place a reader looks said
            # nothing at all about why no action was chosen.
            #
            # It is the M2 seat's own case: an ACT-space event with no sentence is invisible
            # to `orphans`, which counts sentences tracing to no record and cannot see a
            # record with no sentence. **The seat fired the first cycle the row was reached.**
            #
            # **THE EXITS CHANGED UNDER THIS AND THE SENTENCES FOLLOWED -- 2026-09-28.** The
            # `coverage` branch described a ballot that no longer exists. These two are what
            # the goal exit can now refuse on, and BOTH ARE ABOUT THE AGENT, never about a
            # button: one says its objective has no direction to ask for, the other says it
            # asked and got no answer.
            why_ = d.get("why")
            if why_ == "no_realisation":
                out.append(([seq], f"On {slot} I said which way I wanted it to go and no "
                                   f"action was found for that. I did not pick one anyway."))
            elif why_ == "nothing_separates":
                out.append(([seq], f"On {slot} I asked for something that would tell my "
                                   f"alternatives apart, and nothing I can do here does. "
                                   f"That is a reading about the board, not a failure to act."))
            elif why_ == "unordered_no_value_table":
                out.append(([seq], f"On {slot} I asked for the value {d.get('target')} rather "
                                   f"than a direction -- the slot has no order. Nothing I have "
                                   f"done is known to leave it there reliably."))
            else:
                out.append(([seq], f"On {slot} I chose no action: {why_ or 'nothing scored'}."))
        elif ev == "routine_recovered":
            # A FALLBACK IS THE ONE EVENT THAT LOOKS LIKE NOTHING HAPPENED. The plan carries
            # on and the step emits an action, so without a sentence the narration would
            # describe a smooth run over a body that FAILED. It has to say what failed and
            # that the failure is not a refutation, because `exhausted` IS one everywhere else.
            out.append(([seq], f"On {slot} part of `{d.get('routine')}` ended "
                               f"{d.get('outcome')} and I took the fallback instead. The "
                               f"body's ending is not a refutation of the plan -- I never "
                               f"finished putting it to the test."))
        elif ev == "books":
            # **THE AGENT'S ACCOUNT OF ITSELF, WHICH THIS FILE IS ALSO FOR, AND THE TWO NEVER
            # MET.** The books are what let the agent set a term instead of guessing one, and
            # `speak` could not say a single one of them -- so the narration described what the
            # agent DID and never what it KNOWS ABOUT ITSELF.
            #
            # AGAINST THE SCORE, BECAUSE THAT IS THE BOOKS' OWN RULE. Every quantity here is
            # reported beside `levels`, since the score is the one thing outside the agent and
            # without the link these are bookkeeping it could optimise.
            #
            # **`None` IS SAID AS UNDEFINED, NOT AS ZERO.** `per_arrival` and `per_level` are
            # `None` until something arrives or a level moves, and *nothing was bought at any
            # price* is a different sentence from *it was cheap*.
            _pa, _pl = d.get("per_arrival"), d.get("per_level")
            cost = (f"{_pa} action(s) per term that stuck" if _pa is not None
                    else "no cost per term yet, because nothing has arrived")
            lvl = (f"{_pl} per level" if _pl is not None
                   else "no cost per level yet, because the score has not moved")
            half = (d.get("halflife") if d.get("halflife_earned")
                    else "still the seeded one -- I have not earned it")
            out.append(([seq], f"So far I have spent {d.get('actions_spent')} action(s) for "
                               f"{d.get('score_levels')} of {d.get('score_target')} level(s). "
                               f"{d.get('settled')} term(s) settled and {d.get('demoted')} "
                               f"were demoted, {d.get('watching')} still being watched. "
                               f"That is {cost}, and {lvl}. "
                               f"My refutation halflife is {half}."))
        elif ev == "guard_unreadable":
            # THE ROW `F207` WAS DIAGNOSED FROM, AND THE NARRATION COULD NOT SAY IT. `blocked`
            # means only *I could not read the guard*, and WHICH of `goal_residual`'s exits
            # fired is a different fact each time -- supply, type, perception or scope.
            why = {"never_bound": "nothing is bound there, so there is no objective to read",
                   "subject_departed": "the slot my plan was about left the board",
                   "out_type-not-OBJ": "what is bound there is not an objective",
                   "empty-group": "the slot has no peers, so the scope is empty",
                   "slot-absent-from-state": "the slot is not in this frame"}
            ex = d.get("exit")
            out.append(([seq], f"On {slot} I could not read my own guard: "
                               f"{why.get(ex, ex)}. That is not the guard being false, and I "
                               f"am not counting it against the plan."))
        elif ev == "routine_abandoned":
            # METACOGNITION'S SENTENCE. It has to say the CLAIM, the MISS and the SAVING, because
            # those are the three things that distinguish abandoning from the other four endings
            # -- `done`, `blocked`, `exhausted` and `unadvertised` all describe the ROUTINE, and
            # only this one describes the agent noticing it was wrong while there was still
            # budget left to waste.
            out.append(([seq], f"On {slot} I dropped my plan `{d.get('routine')}` at step "
                               f"{d.get('step_index')}: I expected {slot} to change and it "
                               f"stayed {_n(d.get('unchanged_at'))}. That saved "
                               f"{d.get('actions_saved')} step(s) I would have spent on it."))
        elif ev == "reuse_install":
            out.append(([seq], f"On {slot} the sweep put `{d.get('term')}` into my library "
                               f"without asking the bargain. It would have said "
                               f"{'yes' if d.get('would_pay') else 'no'}."))
        elif ev == "route" and d.get("bin") != "held":
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
            tr = d.get('trials') or {}
            drawn = ', '.join(f'{a} from {n}' for a, n in sorted(tr.items()))
            out.append(([seq], f"I have drawn each action I was offered from at least "
                               f"two distinct states ({drawn}) over "
                               f"{d.get('observations')} observations, and no single one "
                               f"of them changed {', '.join(d.get('slots') or [])}. "
                               f"That is a claim about single actions and not about "
                               f"everything I could do -- a SEQUENCE I have not tried "
                               f"may still move something, and I have no way to tell "
                               f"from here. Of what it does cover: either this world is "
                               f"still, or what moves is not something I am built to "
                               f"see. Those are the same reading from in here, and the "
                               f"second is answered by a different set of slots, which "
                               f"I have no way to change."))
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
