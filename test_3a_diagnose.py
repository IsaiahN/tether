"""3a DIAGNOSE (TETHER_3A_DIAGNOSE; Isaiah 2026-10-17 03:37, 04:59; the reviewer PART 2c, 05:00,
05:01) on the pure diagnose.diagnose over scripted trace rows. Fixtures only (a substituted habitat,
Fig 11 :70: wiring, never capability); the in-agent reading is C-3A-DIAGNOSE.

  T1  a swap with no own act: world_changed; MF-T1 the same with an own act in the gap is not
  T2  a transposition of the agent's own two moves: order
  T3  one noisy row (the miss does not persist): noise
  T4  a wandering swapper is credited as an actor after MIN_REPEAT changes, never on the first;
      a motionless bystander is never credited (MF: one coincidence credits nobody)
  T5  a spot shuffler and a swapper on one board at once: each counted on its own slot
  T6  the remembered value now on another object of the same canonical form: moved
  T7  the press landed elsewhere than intended: slip
  T8  the hazard prior: after world changes on a spot, D3 runs before D2 there
  T9  two causes at once on two objects in one step: two verdicts, no global mode
  T10 an own move changes a relational slot of an untouched object (the reviewer 09:05): not
      world_changed, and what moved with the body is never an actor; MF-T10 the same change with
      the body still is world_changed
  T11 the agent moves AND o2 moves itself in the same row, o2.proximity changes: a compound,
      credited to both; o2's kind credited only from the second repeat (the reviewer 09:20)
  T12 part 2's no visible cause credits an unseen actor; 3a rules the change own: the credit is
      held out of the order and withdrawn (the reviewer 09:40); MF-T12 a world change keeps it
"""
import sys

sys.dont_write_bytecode = True

import diagnose as D  # noqa: E402

MIN_REPEAT = 2


def rows_for(slot: str, vals: list, aim: list, landed: list) -> list:
    out = []
    for i in range(len(vals) - 1):
        out.append((i, {slot: vals[i]}, f"A{i}", {slot: vals[i + 1]}, aim[i], landed[i]))
    return out


def run(rows, slot, owner, ok, *, hz, changed=None, moved=None, persists=True, swap_ok=None,
        reach=frozenset(), body=None, omoved=frozenset(), unseen=None):
    return D.diagnose(rows, slot, owner, persists=persists,
                      predicts=lambda r: r[0] in ok,
                      predicts_with=lambda r, a: (swap_ok or set()) >= {(r[0], a)},
                      alt_predicts=lambda _r: False,
                      changed_of=lambda i: (changed or {}).get(i, set()),
                      touching_now=set(), kind=slot.split(".")[1],
                      kind_of=lambda o: o.rstrip("0123456789"),
                      moved_to=lambda _v: moved, hazard=hz, min_repeat=MIN_REPEAT,
                      own_reach=lambda i: i in reach,
                      own_owners=lambda i: (body or {}).get(i, set()),
                      owner_moved=lambda i: i in omoved, unseen=unseen)


def main() -> int:
    # T1: o1.row held on rows 0-1; then it changed on rows 2-3 while the agent pressed o9
    rows = rows_for("o1.row", [1, 1, 1, 4, 6], [None, None, "o9", "o9"],
                    [None, None, "o9", "o9"])
    v = run(rows, "o1.row", "o1", {0, 1}, hz=D.Hazard(), changed={2: {"swap3"}})
    assert v["verdict"] == "world_changed" and v["stale"], v
    rows_own = rows_for("o1.row", [1, 1, 1, 4, 6], [None, None, "o9", "o1"],
                        [None, None, "o9", "o1"])
    v2 = run(rows_own, "o1.row", "o1", {0, 1}, hz=D.Hazard(), changed={2: {"swap3"}})
    assert v2["verdict"] != "world_changed", v2                          # MF-T1
    print("T1 world_changed; MF-T1 with an own act:", v2["verdict"])

    # T2: own moves on rows 2-3, each right with the other's action
    rows = rows_for("o1.col", [0, 0, 0, 2, 3], [None, None, "o1", "o1"],
                    [None, None, "o1", "o1"])
    v = run(rows, "o1.col", "o1", {0, 1}, hz=D.Hazard(), swap_ok={(3, "A2"), (2, "A3")})
    assert v["verdict"] == "order" and v["swap"] == [2, 3], v
    print("T2 order", v["swap"])

    v = run(rows, "o1.col", "o1", {0, 1}, hz=D.Hazard(), persists=False)          # T3
    assert v["verdict"] == "noise", v
    print("T3 noise")

    # T4: a swapper ("swap") changes in each gap; a bystander ("by") is next to it but never changes
    hz = D.Hazard()
    seen = []
    for n in range(3):
        rows = rows_for(f"o{n}.colour", [1, 1, 1, 5], [None, None, "o9"], [None, None, "o9"])
        v = run(rows, f"o{n}.colour", f"o{n}", {0, 1}, hz=hz, changed={2: {"swap7"}})
        seen.append(v["credited"])
    assert seen == [[], ["swap"], ["swap"]], seen
    assert hz.near["by"] == 0 and not hz.credited("by", MIN_REPEAT), hz.near
    hz1 = D.Hazard()
    run(rows_for("o1.colour", [1, 1, 1, 5], [None, None, "o9"], [None, None, "o9"]),
        "o1.colour", "o1", {0, 1}, hz=hz1, changed={2: {"swap7"}})
    assert not hz1.credited("swap", MIN_REPEAT)                          # MF: one coincidence
    print("T4 credited by event:", seen, "; bystander never; one coincidence credits nobody")

    # T5: slot A shuffles with nothing changing beside it (unseen); slot B is changed by the swapper
    hz = D.Hazard()
    for _ in range(2):
        run(rows_for("a1.row", [0, 0, 0, 3], [None] * 3, [None] * 3), "a1.row", "a1", {0, 1},
            hz=hz)
        run(rows_for("b1.row", [0, 0, 0, 3], [None] * 3, [None] * 3), "b1.row", "b1", {0, 1},
            hz=hz, changed={2: {"swap2"}})
    assert hz.world["spot"]["a1.row"] == 2 and hz.world["spot"]["b1.row"] == 2, hz.world
    assert hz.world["actor"][D.UNSEEN] >= 2 and hz.world["actor"]["swap"] >= 1, hz.world
    print("T5 spot counts", dict(hz.world["spot"]), "actor", dict(hz.world["actor"]))

    rows = rows_for("o1.row", [1, 1, 1, 4], [None, None, "o9"], [None, None, "o9"])     # T6
    v = run(rows, "o1.row", "o1", {0, 1}, hz=D.Hazard(), moved="o7")
    assert v["verdict"] == "moved" and v["to"] == "o7", v
    print("T6 moved to", v["to"])

    rows = rows_for("o1.row", [1, 1, 1, 4], [None, None, "o1"], [None, None, "o2"])     # T7
    v = run(rows, "o1.row", "o1", {0, 1}, hz=D.Hazard())
    assert v["verdict"] == "slip" and v["rows"] == [2], v
    print("T7 slip on row", v["rows"])

    hz = D.Hazard()                                                                    # T8
    for _ in range(2):
        run(rows_for("o1.row", [1, 1, 1, 4], [None] * 3, [None] * 3), "o1.row", "o1", {0, 1},
            hz=hz)
    v = run(rows_for("o1.row", [1, 1, 1, 4], [None] * 3, [None] * 3), "o1.row", "o1", {0, 1},
            hz=hz)
    assert v["order"] == "D3D2", v
    print("T8 order after world changes:", v["order"])

    # T9 (the reviewer 08:31; Isaiah 04:59 "several things around the board at once"): in ONE step
    # two objects are contradicted by two different causes -- a1 changed with no own act, b1's
    # press landed elsewhere -- one shared hazard, two verdicts, no global mode
    hz = D.Hazard()
    va = run(rows_for("a1.row", [0, 0, 0, 3], [None, None, "z9"], [None, None, "z9"]),
             "a1.row", "a1", {0, 1}, hz=hz, changed={2: {"swap4"}})
    vb = run(rows_for("b1.row", [0, 0, 0, 3], [None, None, "b1"], [None, None, "c1"]),
             "b1.row", "b1", {0, 1}, hz=hz)
    assert va["verdict"] == "world_changed" and vb["verdict"] == "slip", (va, vb)
    assert hz.world["spot"]["b1.row"] == 0 and hz.own["spot"]["a1.row"] == 0, (hz.world, hz.own)
    print("T9 one step, two objects:", va["verdict"], "/", vb["verdict"])

    # T10: the avatar a0 moves on row 2 (unaimed at o2); o2.proximity (relative to a0) changes, and
    # the pair owner a0~o2 changes with it. Own act through a relation: no world change, no actor
    hz = D.Hazard()
    rows = rows_for("o2.proximity", [3, 3, 3, 4], [None, None, "a0"], [None, None, "a0"])
    v = run(rows, "o2.proximity", "o2", {0, 1}, hz=hz, changed={2: {"a0", "a0~o2"}},
            reach={2}, body={2: {"a0", "a0~o2"}})
    assert v["verdict"] != "world_changed" and v["actors"] == [D.UNSEEN], v
    assert v["own_reach"] == [2] and not hz.world["spot"] and not hz.near, (v, hz.world)
    vm = run(rows_for("o2.proximity", [3, 3, 3, 4], [None, None, "z9"], [None, None, "z9"]),
             "o2.proximity", "o2", {0, 1}, hz=D.Hazard(), changed={2: {"swap1"}})
    assert vm["verdict"] == "world_changed", vm                         # MF-T10
    print("T10 own act through a relation:", v["verdict"], "; MF-T10 body still:", vm["verdict"])

    hz = D.Hazard()                                                                   # T11
    got = []
    for _ in range(2):
        v = run(rows_for("o2.proximity", [3, 3, 3, 5], [None, None, "a0"], [None, None, "a0"]),
                "o2.proximity", "o2", {0, 1}, hz=hz, changed={2: {"a0", "a0~o2", "o2"}},
                reach={2}, body={2: {"a0", "a0~o2"}}, omoved={2})
        assert v["verdict"] == "compound" and v["actors"] == ["o"], v
        got.append(v["credited"])
    assert got == [[], ["o"]], got
    assert hz.own["spot"]["o2.proximity"] == 2 and hz.world["spot"]["o2.proximity"] == 2, hz.own
    print("T11 compound, credited both; owner kind credited by repeat:", got)

    hz = D.Hazard()                                                                   # T12
    hz.unseen("o2.proximity", "proximity", +1)          # part 2, on trace row 2
    v = run(rows_for("o2.proximity", [3, 3, 3, 4], [None, None, "a0"], [None, None, "a0"]),
            "o2.proximity", "o2", {0, 1}, hz=hz, changed={2: {"a0"}}, reach={2},
            body={2: {"a0"}}, unseen=("proximity", 2))
    assert v["verdict"] == "model_too_small" and v.get("withdrawn") and v["order"] == "D2D3", v
    assert hz.world["spot"]["o2.proximity"] == 0 and hz.world["actor"][D.UNSEEN] == 0, hz.world
    hz = D.Hazard()
    hz.unseen("o2.proximity", "proximity", +1)
    vm = run(rows_for("o2.proximity", [3, 3, 3, 4], [None, None, "z9"], [None, None, "z9"]),
             "o2.proximity", "o2", {0, 1}, hz=hz, changed={2: {"swap1"}}, unseen=("proximity", 2))
    assert vm["verdict"] == "world_changed" and not vm.get("withdrawn"), vm       # MF-T12
    assert hz.world["spot"]["o2.proximity"] == 2, hz.world     # the credit back, plus D3's own
    print("T12 ruled own: credit withdrawn, order", v["order"], "; MF-T12 world keeps it")
    print("3a_diagnose: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
