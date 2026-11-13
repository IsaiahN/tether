# Doctrine audit — the whole build against the rules

Nothing fixed. This is the list.

Framing that organises it: **the framework is a kernel, and the bug class is code that
went around a native function instead of through it.** Every finding below is either a
bypassed contract, an instrument reporting something the mechanism does not do, or a
decision taken in code that the agent should have taken.

Severity is about **cascade**, not size. A wrong number I can fix. A wrong number that
other numbers are computed from is what this audit is for.

---

## TIER 1 — instruments that report things the mechanism does not do

These are the worst because everything downstream reads them, including me.

### 1. There is no action policy. Every action is a probe draw.

```python
action = action or self.drive.choose(ACTIONS, self.cycle)   # tether.py:511
...
return sorted(actions)[(cycle * 7 + self._seed) % len(actions)]   # probe.py:71
```

`drive.choose` is a deterministic sweep over the action list. **Nothing about Γ, the
bound terms, the residual, or the objective ever enters action selection.** There is no
branch anywhere that selects an action because a term predicts it will help.

One line later:

```python
phase = I.DIRECTED if self.bound.get(focal) else I.PROBE   # tether.py:514
```

So an action drawn by the identical mechanism is labelled DIRECTED whenever a term
happens to be bound to the focal slot.

**Cascade.** The phase mix is the *stated* transfer instrument — "phase-1 share shrinking
across levels IS the transfer claim, and it needs no win to read." It currently reports
`probe 0.375 / directed 0.625` for behaviour that is **100% probe**. I published that
number in a demo section and in a commit message. `steps_to_win` is measuring luck, and
every `advance` in the DS ladder was reached by a fixed action sweep.

`_link()` is honest about this — *"no goal composition built"* — so the code contains
both the true statement and the instrument contradicting it.

### 2. `Drive.err` aggregates across slots. Hard-rule violation.

```python
for s in self.slots:
    ...
    self.drive.note(action, r.bits > 0)     # tether.py:174, inside the per-slot loop
```

One scalar EMA fed by every slot. The hard rule: **"No aggregation across slots. R is
indexed per object slot. Averaging is how a live signal disappears."**

Two consumers, both load-bearing:

- `bored()` → the probe trigger (`EPS = 0.02`)
- `clocks.note(self.drive.err, …)` → **`steps_to_model`** (`eps = 0.05`)

**Cascade, and it scales the wrong way.** One permanently unexplained slot contributes
`1/n` to the error. At 5 slots that is 0.2 and both thresholds hold. At 20 slots it is
0.05 and **`steps_to_model` declares "modelled" with a slot fully unexplained**. At 50
slots it is 0.02 and **the probe fires as though nothing is left to learn**. ARC has far
more than five slots, so this fails precisely where it starts to matter, and it fails
silently and in the flattering direction.

### 3. The WANT is hardcoded, and it is now simply false.

```python
name, deg = self.env.objective()                     # name is computed...
want = G.compose(G.WANT, G.compose("ALL", G.compose(
    "BECOME", G.Leaf(G.T.OBJECT, "slot"), G.Leaf(G.T.ATTR, 0))))   # ...and discarded
```

The agent states `ALL(BECOME(slot, 0))` as its objective on every step of every world.
`snaps` generates four objective families with varying targets, so the utterance is
usually **stating a goal the agent does not have.**

Doctrine: *"a hardcoded procedure that pre-answers a question the agent should ask is a
FAULT, even when it is correct."* Here it is not even correct.

**Cascade.** `speak.py` renders the utterance as the agent's account of itself.
Legibility is the instrument, and the instrument is asserting something false. The BET's
DERIVE is composed against this WANT, so the whole dependency chain hangs off a constant.

### 4. `focal` is chosen by alphabetical order.

```python
focal = self.slots[0]
focal = next((s for s in self.slots if s in self.owed_import), focal)
```

A hardcoded attention policy. The agent should attend by residual mass — that quantity
exists, per slot, and is not consulted.

**Cascade.** Both the utterance and the phase label are computed from this one slot, so
**renaming a slot changes the phase histogram.** An instrument that moves when you rename
a variable is not measuring the agent.

---

## TIER 2 — kernel bypasses

### 5. The agent imports the world's constants.

```python
from world import ACTIONS, M        # tether.py:20
```

The `Env` protocol exists so a domain is filled through eight named members, and `bind()`
refuses an adapter that cannot fill them. **There is no member for the action set and
none for the value space**, so the loop reaches past the contract into another module's
globals.

- `M` is the entire cost model: `correction_bits` returns `log2(M)`. The agent is handed
  the size of the value space, which in ARC is a per-level fact.
- `ACTIONS` is static. **`available_actions` growth is an IMPORT** — the user's point,
  and Figure 6 lists nature as a source. As written the action set cannot grow, so the
  IMPORT step is unreachable on the one channel most likely to use it.

The contract being incomplete is what *forced* the bypass. That is the kernel failure in
its exact form: no syscall existed, so the caller went around.

### 6. `snaps` imports `_atoms` from `world`.

```python
from world import ACTIONS, DELTA, M, _atoms    # snaps.py:32
```

Two problems. A private name crosses a module boundary; and **the generated worlds are
generated over the atom set designed for the hand-built toy.** `in_closure` — the
denominator of every abstention number in this repo — is defined relative to a vocabulary
chosen for a different world. The generality of the generator is silently bounded by that
choice, and nothing in the record says so.

### 7. `snaps.deviate` decides the curriculum; the agent never sees DS.

Correct as an experimental control, and worth stating so it does not drift: DS is a
harness fact. If any part of the agent ever reads it, the ladder stops measuring transfer
and starts measuring instruction.

---

## TIER 3 — implicit decisions taken in code

### 8. The identity default is an unstamped prior.

```python
term = self.gamma.library[self.bound.get(slot, IDN)]
```

An unbound slot is predicted to **not change**. That is a persistence prior — a real and
defensible one, and one of the six loadable shapes. But it is applied invisibly: not
stamped `prior`, not recorded as a choice, not falsifiable.

**Cascade.** For an unbound slot, "residual" means *it moved*, not *my model was wrong* —
there is no model. So density(R) is inflated at the start by every slot that simply
changes, and `bored()` reads that inflated value.

### 9. `PAY` carries a step count, not a price.

```python
pay = G.compose(G.PAY, G.price(float(len(self.trace)), len(self.trace)))
```

Value and evidence-count are the same number. The grammar defines PRICE as *"a cost claim
with its evidence count"*. This is a stub in a slot the gate checks the *shape* of but not
the *meaning* of, so it passes. Figure 8's surplus accounting has no real input.

### 10. Five unanchored constants sit in the decision path.

| | | anchored? |
|---|---|---|
| `probe.ALPHA = 0.1` | error EMA weight | no |
| `probe.EPS = 0.02` | "explains everything" | no |
| `probe.WARM = 12` | before boredom is allowed | no |
| `gamma.REJECTION_HALFLIFE = 8.0` | how fast a refutation fades | no |
| `instruments.Clocks.eps = 0.05` | "modelled" | no |

`MAX_ACTIONS` got a provenance line because it was anchored to human play. These five
have no stated basis. Doctrine names invented magic numbers as a known failure mode, and
`Clocks.eps` and `EPS` are two different thresholds for the same idea, which is how you
can tell neither was derived.

### 11. The bracket channel has never run.

`env.transform()` returns `None` in both worlds, so R has three channels and two carry.
This is *stated* in the ledger rather than hidden, which satisfies "nothing silent" — but
a third of R is untested, and `snaps` was the opportunity to exercise it and did not.

---

## What follows from the list

Findings 1–4 mean **several numbers I have reported in this repo describe something the
code does not do.** The phase mix is the clearest: it is published as the transfer claim
and it is measuring a label, not a behaviour.

Findings 1 and 2 have the same shape — a quantity is computed at the wrong granularity or
from the wrong source, and then an instrument reads it as though it were the real thing.
That is the cascade the audit was for: not the wrong value, but the wrong value being
depended upon.

Finding 5 is the one that will hurt most in ARC, because the missing contract members are
exactly the two facts ARC varies per level.
