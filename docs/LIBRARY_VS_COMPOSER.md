# Library vs Composer — why this works

*Isaiah, 2026-09-14. His framing, verbatim. The theory of why the training pays down the
combinatorial bill, and why the composer — not the library — is the thing.*

---

## Why this works:
Everything comes down to **libraries vs composers**. 

If libraries were all that were needed, a dictionary could solve arc, or a physical library would be sentient. Human writing is the compression of human thought patterns into words and sentences. 

LLMs tokenize the words and compressed thought patterns into a retrieval geometry, and forcibly extract meaning, allowing them to gain context and resynthesize text into a relevant form still recognizable, legible and meaningful for humans. 

Again the library is not the solution alone, because a LLM even with a larger training set, had to be RL'd into learning math, and other tasks through RLHF or the "harness". But what I have understood is that your library can be very tiny, provided that the agent has been pre-trained on the expected compositions & refutations in general, instead of blind brute-forcing learning (that makes pre-training pay a portion of the bill, but its still coming from an outside source/frame that actually paid the bill in collecting the initial dataset).

The blind brute-force method is the expensive way to **"pay the bill"**, and must be heavily compressed as a result. Evolution/natural selection makes this faster by having diversification of many species, with variation in large populations and letting the **"winners carry the solution forward" via lineage compression** in DNA for the environment selection pressures they are pitted against. (evolution pays the bill/tests in body count).

On the individual level, **paying the bill** means learning a curriculum of what to do and not to do (similar to school), and aligning your own proprioception, reification, adaptation, and reasoning to that corpus, so you can respond in like kind. This is what tether does, but with objects instead of words and in a transparent manner.

This is why it is possible to **"start cold"** but it will literally take an equivalency to generations of hard won learning with agents (to pay down the combinatorial explosion problem). 

So the viable alternative is to use reinforcement learning to pre-train the mappings, and allow composition and refutation to settle relevant mappings in the library. 

**The organization and categorization of the library is what the composer does.** The lookup and reachability of that library depends on the composer and their compositions. **No neural networks or GPUs are required for this process.**

Because ultimately, the composer was always meant to be the librarian who was sorting the data, and retrieving it in a specific manner in the first place.   

## The asymmetry — pretraining negates the wrong far more than it names the right

*Isaiah, 2026-09-14.*

Pretraining is mainly there to negate the combinatorial explosion of ways things can go **wrong**, more than to tell you the right answers. And the two are not the same size.

**The right answers are a thin set. The wrong ones are almost everything.** So a prior that tells you where **not** to look prunes vastly more than a prior that tells you where to look — and it does it without committing you to a particular answer. Knowing the door isn't on three walls leaves you a wall to search; being told where the door is leaves you nothing to find.

Which is also why it's the **safe** form. A negative prior can't hand over the solution — it can only shrink the space the composer still has to work in. That is the composer becoming a librarian: **the aisles aren't removed, they're marked dead.**

And this project has it exactly backwards right now. F133 built the what-to-do half and it was over the line — precisely because a positive prior carries the answer. The what-not-to-do half — refutation cache, demotion, conflict-driven clause learning — is still unbuilt, and it is not merely the second blade of the scissors. **It is the blade that was always going to do the work.**

One qualification: pure negative pruning has a limit. *Not here* narrows; it never proposes. You still need something that **generates** candidates — and in this architecture that is minting and the closure walk, which already exist and are cheap. **So the honest split: generation is already there and cheap; what's missing is the thing that stops it generating the same dead candidates forever** — 174 bets a cycle, 99% failing, and nothing remembering that they failed. That makes the refutation cache the highest-value unbuilt mechanism in the project.

## The library is a parts bin, not a lookup table — and promotion stocks it

*Isaiah, 2026-09-14. The piece that makes the two halves one mechanism.*

The minting process is made cheaper by the reusable parts in the library. That is the nuance beyond "composer as librarian," and it's the thing I kept missing.

The library isn't a lookup table the composer searches. It's the **parts bin the composer builds from**. A new term isn't *found* in it — it's *assembled* out of it. So a well-sorted, well-stocked library doesn't just make retrieval cheap; it makes **invention** cheap, because the pieces are already paid for.

And that's precisely what promotion is buying. A term that pays repeatedly becomes primitive — and every later composition that uses it pays **nothing** for the part it's made of. The compounding, with the interest paid in reduced minting cost rather than in recall.

Which is why the promotion zero mattered so much and why ten firings is a real result. Without it, every mint starts from atoms. With it, mints start from whatever the ground has already settled. That's the difference between building a machine from raw metal and building it from components.

**The correction to "composer-as-librarian":** the librarian framing — sorted storage and its user — is one direction of value. The other — **the library as accumulated capital the composer spends down on new work** — is the direction that makes a small library workable at all. The argument was never that a tiny library *contains* what's needed. It's that a tiny library **of the right parts** makes the needed thing **cheap to build**. It isn't holding answers, it's holding parts. That is a better statement of the thesis, because it explains *why* the library can be small.

**The flywheel's failure mode, before the numbers arrive (reviewer, 2026-09-14).** Working: promotions rise, the unit count rises, refutations **retract as it does**, and mint cost per term falls. Broken in the way that mimics success: promotions rise, refutations **never retract**, and the cache slowly forbids the aisles the growing parts bin just made affordable — reach-failure falls (because fewer bets get made) while reach falls with it. Same tell as before (reach-failure down, reach down), now with a mechanism under it: a refutation that does not retract on unit growth strangles the flywheel it was meant to serve. The paired run is still the check; what is new is that it names the line of code that produces the failure — the `units_now > units_then` retraction. (Note this is a *second* failure mode distinct from the one already measured: the gap-shape key lost doors *within* a unit level even though it retracted correctly; the composition-keyed cache must avoid both — a fine-enough key AND a retraction that fires on every new unit.)

## The SAT precedent — and why there are THREE organs, not two halves

*Reviewer, 2026-09-14, marked as SAT practice rather than anything measured here.*

**Conflict-driven clause learning is exactly re-derivation stocking a parts bin.** When a search dies, derive a clause **already entailed** by the original set — nothing added, just made explicit — and every later branch gets it cheaply. That is the flywheel, found independently in the 1990s, and it is the single technique that beat this class of explosion in practice. So the refutation cache is not a guess; it is what the industry converged on.

**And it comes with a counterintuitive finding: more parts is NOT monotonically better.** Solvers delete learned clauses aggressively, and they have to — a clause database that only grows makes every step slower, and past a point the solver spends more time consulting the bin than the bin saves. Deletion policy is among the most tuned parts of a modern solver; solvers that keep everything lose to solvers that forget.

**Which splits demotion off as its own organ.** Refutation prunes the **search**; demotion prunes the **bin**. Different organs, not two halves of one thing. Without the second, promotion stocks parts faster than they are used, lookup cost rises with bin size, and the flywheel eventually runs **backwards** — and the failure looks like health: promotions rising, library growing, everything reading as accumulation working, while cost per cycle climbs because every mint consults a bigger bin. That is the 174-bets shape returning with a better story attached. The curve already shows the sensitivity — **0.98s at cycle 0 against 29.1s at cycle 8, cause named as closure enumeration scaling with library size.** A bin that only grows is that curve, permanently.

**The open question, not the answer: what retires a part?** Promotion has a condition; demotion does not yet, and the symmetric counter prunes terms that are WRONG, not parts that are UNUSED. A part that is never wrong and never used is the case neither mechanism catches, and it costs lookup forever. The SAT answer is activity-based — a clause used in recent conflicts is kept, an inactive one deleted — and tether has no usage/activity signal on a part yet. So the three organs are: **promotion** (stock the bin), **refutation** (prune the search — CDCL), **demotion** (prune the bin — deletion policy, and the underspecified one).

---

*Seat's note on how this frames the build: the pre-RL baseline (174 composition-bets/cycle at 99%
reach-failure, `runs/PRE_RL_BASELINE_ls20.json`) is the composer that is not yet a librarian —
enumerating the shelves because it has not learned where things are. "Did the RL teach retrieval"
is therefore `reach-failure falls, bets/cycle falls` — the composer becoming the librarian. And
those two numbers are exactly what the refutation cache attacks: 174 bets a cycle at 99% failure is
the composer re-generating dead candidates because nothing remembers they failed. So the
what-NOT-to-do half (refutation cache, demotion, conflict-driven clause learning) is not the second
blade of the scissors — it is the load-bearing one, the safe form of a prior (it cannot carry the
answer), and the direct fix for the reach-failure metric.

The parts-bin half is already in the cost function: `mint` prices a candidate as
`term_bits(gamma.length(term, units), alphabet)` — its length in UNITS, and a settled term is one
unit — so a composition built from a promoted part is priced as if that part were a single atom.
`PRICED IN UNITS, so a settled sub-composition costs what the ground already paid for it` is the
comment at the site. That is why F135 unblocking promotion (2→10, verified) is load-bearing rather
than cosmetic: each promotion lowers the price of everything later built on it — the flywheel
(promotion stocks the bin → mints start from components → more clear the bargain → more settle →
more promote). And it re-frames the door-loss: as the bin grows a unit, the same gap-shape gets
cheaper to build and its closure re-opens — which is exactly the `units_now > units_then`
invalidation. The two halves are coupled through the unit count. See `TRAINING_PLAN.md`,
`DEMAND_LOG.md`, and the memory note `composer-is-the-librarian`.*
