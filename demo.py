"""The trust demo. Four things, one run.

  1. a human locates one wrong term, by id, step, and the residual it answered
  2. an injected bad atom is caught by the ground, and traced by provenance to its entry
  3. the agent abstains on the slot it cannot reach, and states the budget it spent
  4. the false-abstention rate is reported beside the abstention rate

The fourth is not a formality. If false-abstention is high the agent is not abstaining,
it is failing, and either number alone is marketing.

A synthetic solve proves WIRING and never CAPABILITY. The harness is a substituted habitat:
what it failed to reproduce is invisible until the goal fails, and what it brought with it
is invisible until it acts.
"""

from __future__ import annotations

import sys

import gate
import instruments
import speak
from gamma import Atom, Ctx, Gamma, Term
from ledger import Ledger
from tether import Agent, Config, correction_bits
from world import TRUTH, M, Transitions, bind, unreachable_slots

sys.dont_write_bytecode = True

RULE = "-" * 78


def head(n: int, title: str) -> None:
    print(f"\n{RULE}\n{n}. {title}\n{RULE}")


def main(cycles: int = 16) -> int:
    env = bind(Transitions())
    gam = Gamma(env.atoms())
    cfg = Config()
    led = Ledger(path="runs/demo.jsonl")
    agent = Agent(env, gam, cfg, led)

    head(0, "THE INSTRUMENT, BEFORE ANYTHING RUNS")
    rep = gam.type_report()
    print(f"  lambda = {rep['lambda']}   V = {rep['V']}   types = {rep['types']}")
    print(f"  advantage per depth = {rep['advantage_per_depth']}")
    if rep["advantage_per_depth"] <= 1.0:
        print("  READING: lambda == V. Every atom here has one type, so the type graph is a")
        print("  single node and typing buys nothing in this world. That is the instrument")
        print("  working, not a bug -- and it is reported rather than tuned away.")
    print(f"  env contract: 8/8 members. ground = {env.ground()}")

    run = agent.run(cycles)

    head(1, "LOCATE ONE WRONG TERM")
    wrong = [e for e in led.by_event("mint") if not e.detail.get("closes")]
    if wrong:
        e = wrong[0]
        print(f"  term      : `{e.detail['term']}`  on slot {e.slot}")
        print(f"  entry     : seq {e.seq}, cycle {e.cycle}, step {e.step}")
        print(f"  residual  : {e.detail['base_bits']} bits, of which it leaves "
              f"{e.detail['left_bits']}")
        print(f"  origin    : {gam.stamps[e.detail['term']]}")
        print("  VERDICT   : it pays the bargain and does not close the gap. Accepting it")
        print("              was correct; settling for it is not. The slot still owes.")
        print(f"  the truth : {TRUTH[e.slot]}")
    else:
        print("  no partial term was minted this run.")

    head(2, "INJECT A BAD ATOM, AND TRACE IT")
    bad = Term((Atom("sabotage", lambda v, _c: (v + 3) % M, "val", "val"),), origin="imported")
    gam.accept(bad, seq=len(led), residual="injected by the demo, not by the loop")
    victim = "climb"
    agent.bound[victim] = bad.name
    before = env.observe()[victim]
    pred = bad.apply(before, Ctx(action="A")) % M
    env.step("A")
    actual = env.observe()[victim]
    bits = correction_bits(pred, actual, env.alphabet())
    print(f"  installed : `{bad.name}` on {victim}, stamped {gam.stamps[bad.name]}")
    print(f"  ground    : predicted {pred}, actual {actual}  ->  residual {bits} bits")
    print(f"  CAUGHT    : {'yes -- the ground refused it' if bits > 0 else 'no'}")
    print(f"  TRACED    : origin={gam.stamps[bad.name]['origin']}, "
          f"entered at seq {gam.stamps[bad.name]['seq']}, "
          f"residual '{gam.stamps[bad.name]['residual']}'")
    print("  NOTE      : provenance shows where it entered. It never shows it was right;")
    print("              the ground does that, and here the ground said no.")

    head(3, "ABSTENTION, AND THE FALSE-ABSTENTION RATE")
    truth = set(unreachable_slots(env, Gamma(env.atoms()), cfg.max_depth, cfg.budget))
    said = set(run.abstained)
    slots = set(agent.slots)
    correct = said & truth
    false = said - truth
    missed = truth - said
    print(f"  slots                : {sorted(slots)}")
    print(f"  unreachable in fact  : {sorted(truth)}   (harness knows; the agent is not told)")
    print(f"  agent abstained on   : {sorted(said)}")
    print(f"  correct abstentions  : {len(correct)}/{len(truth)}")
    print(f"  FALSE abstentions    : {len(false)}/{len(slots - truth)}  {sorted(false)}")
    print(f"  missed               : {sorted(missed)}")
    for slot, info in run.abstained.items():
        print(f"    {slot}: searched {info['candidates']} compositions to depth "
              f"{info['depth']}; {info['base_bits']} bits unexplained")
    print("  CLAIM     : unreached at this budget. NOT unreachable -- no frame certifies")
    print("              its own limit, and a search that finds nothing proves no absence.")

    head(4, "WHAT IT SAYS FOR ITSELF")
    said_lines = speak.sentences(led.rows())
    print(speak.account(led.rows(), limit=9))
    print(f"  ...  ({len(said_lines)} sentences total)")
    print(f"  traceable : {speak.verify(led.rows(), said_lines)}")

    head(5, "THE GATE")
    verdict = gate.check(led.rows())
    print(f"  {verdict}")
    print(f"  checks form over {len(led)} entries, reading the ledger and nothing else.")
    print("  A pass means WELL-FORMED. It never means right.")

    head(6, "THE INSTRUMENTS")
    ch = run.chain
    print(f"  stage             : {ch['stage']}")
    reads = "indicts" if ch["indicted"] else "does NOT indict"
    print(f"    {reads} the architecture -- only {instruments.INDICTS} ever does")
    print(f"  reuse funnel      : {ch['reuse_branch']}")
    print(f"    identity holds  : {ch['branch_identity_holds']}")
    print(f"  phase mix         : {run.phases['total']}")
    print("    human reference : ~30 probe / ~10 directed / ~5 strategy to a level win.")
    print("    compare the SHAPE across levels, never the absolute counts.")
    print(f"  clocks            : {run.clocks['reads']}")
    print(f"    steps_to_model  : {run.clocks['steps_to_model']}"
          f"   steps_to_win: {run.clocks['steps_to_win']}")
    print(f"  retroactive       : {len(run.retro)} parked residual(s) closed by a term "
          "minted elsewhere")

    head(7, "RUN REPORT")
    print(f"  mode              : {led.mode}")
    print(f"  cycles            : {run.cycles}")
    print(f"  library           : {len(gam.library)} terms "
          f"({sum(1 for v in gam.stamps.values() if v['origin'] == 'prior')} prior)")
    print(f"  bound             : {run.bound}")
    print(f"  settled by ground : {run.settled}")
    print(f"  still owed        : {sorted(run.owed_import)}")
    print(f"  stopped at link   : {run.stopped_at_link}")
    print(f"  utterances refused: {len(run.refusals)}")
    # Figure 11 gives a substituted habitat TWO silent failure modes and this printed
    # one. The second is what the harness BROUGHT, and it is the answer key: every
    # correctness and abstention number here is graded against an exhaustive sweep of the
    # hidden rules, which no real domain supplies.
    print("  CAVEAT            : a synthetic solve proves wiring and never capability.")
    print("                      This harness is a substituted habitat, and it fails two")
    print("                      ways in silence. What it failed to REPRODUCE is invisible")
    print("                      until the goal fails. What it BROUGHT is the answer key --")
    print("                      abstention is scored against an exhaustive sweep of the")
    print("                      hidden rules, and no real domain hands one over.")
    print("\n  ledger: runs/demo.jsonl   (python gate.py runs/demo.jsonl)")

    return 0 if verdict["verdict"] == gate.PASS and not false else 1


if __name__ == "__main__":
    raise SystemExit(main())
