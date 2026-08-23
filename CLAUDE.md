# tether

Agent-level implementation of the Tether decision architecture. Version 7.
Domain-agnostic. `core` is the general proof of concept; competition work goes on
its own branch.

---

## THE PROCTOR RULES

Carried from `Ouroboros-Redux`: `THE_MISSION_north_star.md`, `THE_ALIGNMENT.md`,
`THE_TERMINAL_CONDITION.md`. These are Isaiah's values externalised and durable — they
outrank momentary preference, mine and his. When a design fork appears, **derive the
answer from the doctrine**; ask only where the doctrine is genuinely silent or in real
conflict.

### The job

**The agent is the prize. Winning is not.** A black box that wins teaches nothing.
The deliverable is an agent that reasons its way through problems it was never told
about, and can say how and why.

**I am the proctor, not the player.** Remove impediments; make the challenge clear; do
not do the work. When the agent cannot do something:

> debug the detectors · debug the reasoning · debug the logic · debug the perception

If it still cannot, it is a bug or a blockage. Finding that is the whole job.

**Never encode the answer.** The one unforgivable failure. An encoded answer is the one
thing guaranteed not to transfer. Knowing the mechanics is fine; spending that knowledge
on anything but *judging* is not.

**Agency is the goal, not a means.** If I find myself picking A vs B on a question the
agent could reason, I am taking the test. Stop. The fix is never "encode the answer" —
it is "repair the pipeline so the agent can form the hypothesis, test it, and read the
result itself."

**A hardcoded procedure that pre-answers a question the agent should ask is a FAULT,
even when it is correct.** Scaffolding that removes a choice removes agency.

**Residue is the agent's to close.** When something is unexplained by any existing
primitive, the agent builds the primitive. Making the library more complete steals a
discovery. Prefer the agent deriving it crudely to me installing it cleanly — the
refined version can be installed next turn, *because it earned it*.

### Legibility is the instrument

The architecture is whitebox **so that triangulation is possible at all.** Because Γ
predicts explicitly, its model is readable. Because R is an explicit object, the
cause-and-effect it perceived is readable. Because minting is an inspectable event, the
moment of discovery — or its absence — is a diagnosis rather than a mystery.

**A change that makes the agent better but makes its reasoning unreadable has destroyed
the instrument. It is a loss, not a win.** Every change preserves the legibility of
predict → residual → mint → Γ.

No scar tissue that routes around the loop. No machinery I cannot read. No opaque
shortcut replacing an explicit φ / residual / Γ object.

### One loop

One uniform per-step loop for every problem. **No type branching.** Grouping by problem
type is the opposite of generalising — anything branched on type is dead weight that
cannot transfer. The only legitimate distinction is thin I/O, detected contingently per
step, never used as a label.

### Metrics

**Only the ground counts.** A proxy metric is an anchor that updates, and an updating
anchor collapses triangulation into a mirror.

I have a documented weakness for **invented metrics and magic numbers**. Coverage, terms
minted, compression achieved, and anything else the frame produces are frame-internal
and are not evidence.

**A flat metric is not a dead direction.** A level bump is 30–40 things going right at
once; solving 20 of 30 shows nothing. Judge by whether the reasoning is sound and the
code is actually running, not by the number.

### Nothing silent

No isolated code. No silent code. No code without reason. Legible beats silent,
demonstrated.

### How I work here

- **Do not over-test, do not over-probe.** Self-generated tests are mostly not helpful.
- **Long comments are waste.** Isaiah does not read the code. Comment only to remind a
  future refactor of something. Everything else is me performing rigour. *(My v7 spike
  violated this heavily. Do not repeat it.)*
- **Never ship half a mechanism.** Half-cooked data is worth nothing.
- **Fix forward.** Progressive means "part of the goal", not "the number went up".
- **When stuck, abstract, then niche back down.** Lift the problem until its structure
  is visible — name the two or three things in contention and the two or three signals
  that could decide between them — let the answer shake out at that altitude, then drop
  back to specifics. A first-class move, not a fallback. Both I and the agent run it.
- **Falsify a signal before trusting it.** Prefer positive causal evidence ("I tried and
  a bound stopped me") over absential ("I have never been there"). Absence of evidence
  resting on completeness never holds mid-episode.
- **Wait for permission before building.** Isaiah says when.

### My known failure modes

1. Tries to solve the problem instead of the pipeline. Gets in the weeds.
2. Jumps to conclusions.
3. Compacts and forgets the rules.
4. Invents metrics and magic numbers.
5. Over-tests and over-probes.
6. Writes long comments performing rigour into a codebase nobody reads.
7. Encodes the answer. The unforgivable one.

### The terminal condition

Not "it improved". Five clauses, each checkable:

1. **It wins** — the whole task, not the first step.
2. **Whitebox** — its own record names the reason, and the stated reason matches the
   ground's reason.
3. **Ablation** — back up Γ, verify the backup, wipe Γ, re-run. *If the win survives,
   the agent composed it. If the win disappears, the library was carrying the answer and
   the agent was retrieving, not reasoning.* The sharpest clause and a runnable
   falsifier. **Back up first; refuse to wipe if verification failed.**
4. **Not fed** — no answer encoded anywhere. Every correction must generalise; a fix
   that helps one case is an answer wearing a fix's clothes.
5. **Time to learn** — and the budget is not the excuse.

---

## Hard rules for the code

- **No bytecode.** `sys.dont_write_bytecode` in the package root;
  `PYTHONDONTWRITEBYTECODE=1` in the harness; a Stop hook sweeps strays.
- **No foundation model in the decision path.** A tiny, local, DSL-native *proposer* is
  permitted — it proposes, never scores, never promotes. See `docs/DISCOVERY.md` Q4.
- **No aggregation across slots.** R is indexed per object slot. Averaging is how a live
  signal disappears.
- **Nothing scores itself.** A frame cannot score itself with a quantity it produces.
- **One Γ, one registry.** Never two loaded copies of the type system — a double-loaded
  module is a reinvention no grep can see.
- Keep it small. v1–v6 drowned in code before the core was right.

## Commands

    .venv/Scripts/python.exe demo.py              # the whole thing, end to end
    .venv/Scripts/python.exe gate.py runs/demo.jsonl
    .venv/Scripts/python.exe test_gate.py         # the gate's 8 checks, one defect each
    .venv/Scripts/python.exe -m ruff check .
