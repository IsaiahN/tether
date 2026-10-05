# THE TERMINAL CONDITION — when the heartbeat stops

**Isaiah, 2026-08-06, verbatim:**

> *"keep that heartbeat going every 30 mins to an hour until we get an agent that is beating all the
> games completed GAME WIN, not just level 1 cleared. on all 25 games, and an agent that can explain
> its reasoning of how it did it (whitebox) and an agent that could compose on the fly the answers to
> beat the game if we ablated its library, it could still recompose. and an agent that wasnt fed the
> answers directly so that the reasoning was shaped as it played. and an agent that gets time to
> learn. so we have a generalized learner"*

This supersedes the weaker gate in `THE_RESTORE.md` §0, which said only "levels move." **Levels
moving is not the condition. Winning every game is.**

---

## THE FIVE CLAUSES, EACH AS A THING THAT CAN BE CHECKED

**1. GAME WIN ON ALL 25 — not a level, the whole game.**
`levels_completed == win_levels` for every game on the public set. **183 of 183.** Today: **3 of 183
levels, and 0 of 25 games.** Three games have cleared their *first* level and no game has ever been
completed. The distance is not "22 more games" — it is 180 more levels, and no game has demonstrated
it can survive past its own level 1.

**2. WHITEBOX — it explains how.**
For each win, the agent's own record (`mem3`, the five keys) names the relation the game actually
requires, judged against `subgoals/` and the solution replays, which it never reads. Not "a log
exists" — the stated reason must match the ground truth's reason.

**3. ABLATION — empty its library and it re-composes.**
⭐ **This is the sharpest clause and it is a runnable falsifier.** **Back up Γ, verify the backup,
then** wipe Γ and re-run. **If the win survives, the agent composed it. If the win disappears, the
library was carrying the answer and the agent was retrieving, not reasoning.** This is the OOD test
performed locally, and it can be run the day there is a win to run it on. Nothing in the project
currently passes it, because nothing currently wins.

**The backup is a mechanism, not a note.** Isaiah: *"always backup a copy so we dont waste time
rebuilding in case the agent is broken."* A Γ store is hours of play; wiping it to answer a question
and then finding the agent broken means paying twice for nothing. So `tools/ablate.py` takes the
snapshot **first**, verifies it file-count and byte-for-byte, and **refuses to wipe if verification
failed**:

```
python tools/ablate.py snapshot      # back up Γ + bank, verify, print the tag
python tools/ablate.py wipe          # snapshot, VERIFY, then empty Γ
python tools/ablate.py restore <tag> # put it back
python tools/ablate.py list          # what exists
```

**The residual bank is deliberately NOT wiped.** Γ holds the promoted library — what the agent
*inherited*. The bank holds evidence of play. The ablation asks what the agent can **derive**, not
what it can remember having seen, so removing the bank would be testing a different question.

**4. NOT FED — the reasoning was shaped by play, never by us.**
`answer_lint` clean, `newhorse.audit` clean, no game-id literal in any agent module, no `_find_*`
detector written to make a key non-zero, and no per-game rule. The proctor holds the answers and
spends them only on judging. **Every correction must generalise: a fix that helps one game is an
answer wearing a fix's clothes** (Gate 19 — a lever scoring 0 on the delta table does not get built).

**5. TIME TO LEARN — and the budget is not the excuse.**
Measured 2026-08-06: **24 of 25 runs end on `unearned_reset`, exactly one on the action cap.** The
agent already gets a median of ~11× the actions a level actually needs, and up to 137× on `r11l`. It
does not run out of time. It dies without having learned anything new from dying. **Raising the
budget is not the lever, and this clause is currently satisfied while the agent still fails.**

---

## WHERE IT ACTUALLY STANDS, 2026-08-06

| clause | state |
|---|---|
| 1. game win ×25 | **0 of 25.** 3 of 183 levels. |
| 2. whitebox | the organ exists (M-1); the agent is **silent on the winning path of 6 of 7 games measured** |
| 3. ablation | **untestable — nothing wins to ablate** |
| 4. not fed | **holding.** lint clean, audit clean, no per-game rule shipped |
| 5. time | **satisfied, and it is not the constraint** |

**The binding wall is clause 2, upstream of everything.** The agent is silent on its own winning path
in nearly every game — not posing the wrong objective, posing none. Fixing what the composer can
*say* (M-2, M-6 — both landed at +0) cannot help while it has nothing to say it *about*.

---

## OPERATIONAL LIMIT, STATED PLAINLY

The heartbeat is `d69f6934`, every 29 minutes, **session-only**. It is not written to disk, it dies
when this session ends, and it auto-expires after 7 days regardless. It cannot run to a condition
that may take weeks. **For a heartbeat that survives the terminal closing, the mechanism is a cloud
schedule (`/schedule`), not this one** — and that is a decision for Isaiah, not something to assume.
