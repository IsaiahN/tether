# tether — the minimal kernel

The minimal **Tether** kernel, version 7 (2026-08-22). It is the decision architecture and
nothing else: residual routing, gated minting, provenance, and an abstention that names what it
searched. No library, no lineage, no foundation model.

It runs on a toy symbolic world (`world.py`): named slots holding typed values, each with a
hidden per-slot rule, and a ground that is exact match on the next state. One slot, `OPAQUE`, is
quadratic while every atom is affine with a modulus, so it is provably outside `closure(Γ)` for
any budget. The agent is told nothing about this; it has to find out, and say so.

`demo.py` is the trust demo, four things in one run:

1. a person locates one wrong term, by id, step, and the residual it answered;
2. an injected bad atom is caught by the ground and traced by provenance to its entry;
3. the agent abstains on the slot it cannot reach, and states the budget it spent;
4. the false-abstention rate is reported beside the abstention rate.

It predates the library, the lineage, and the Kaggle and ARC work, and it is **kept minimal on
purpose**, so the architecture can be read whole in about 1,600 lines.

## The three branches

- **[`core`](https://github.com/IsaiahN/tether/tree/core)** (this one): the minimal kernel. The
  Tether loop, gate and abstention on a toy symbolic world, about 1,600 lines. Read this first to
  see the architecture whole.
- **[`general-agent`](https://github.com/IsaiahN/tether/tree/general-agent)**: the full general
  learning agent. Domain-agnostic: the library of ~4,000 human-prior entries, the lineage
  (generations, merge, graft), search, minting, the narrator. Where general work lands first.
- **[`arc-solver-agent`](https://github.com/IsaiahN/tether/tree/arc-solver-agent)**:
  `general-agent` plus the ARC-AGI-3 interface and the Kaggle runner. The competition build: it
  receives `general-agent` by merge and adds only what ARC needs.

Swap the interface, keep the lineage.

## Run it

Python 3.11 or later, no dependencies.

    python demo.py        # the trust demo, in seconds
    python test_gate.py   # the gate's checks, one defect each

The figures it is built from are described in *Arrival of the Fittest: The Tether Architecture*
([Medium](https://medium.com/@IsaiahNwukor/arrival-of-the-fittest-the-tether-architecture-1de7edf641ec)
· [Substack](https://adventuresinml.substack.com/p/arrival-of-the-fittest-the-tether)).
