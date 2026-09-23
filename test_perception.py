"""Perception regression guards -- one real defect each, all caught this session by the
composition->board round-trip (see memory generator-roundtrip-audit). Reintroducing any fails here.
The sparse public games hid all four; a scene built to test one primitive makes each unmissable."""

import sys

import arc_percept
import detectors
import observer

sys.dont_write_bytecode = True


def _obj(board: list, colour: int) -> dict:
    for o in arc_percept.components(board):
        if o["colour"] == colour:
            return o
    raise AssertionError(f"no object of colour {colour}")


def test_contain_fires_on_containment():
    """`contains` was cell-superset (ca>=cb), never true for distinct objects: Contain was dead."""
    board = [[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 2, 3, 2, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]]
    ring, inner = _obj(board, 2), _obj(board, 3)
    lit = {d["atom"] for d in detectors.light_relation(ring, inner)}
    assert "Contain" in lit, f"Contain must fire on a container holding an object, got {lit}"


def test_topology_only_true_holes():
    """holes was bbox_area - cells, counting concavity -- an L-shape false-fired Topology."""
    ring = _obj([[2, 2, 2], [2, 0, 2], [2, 2, 2]], 2)
    lshape = _obj([[3, 0], [3, 0], [3, 3]], 3)
    assert arc_percept.holes_of(ring["cells"]) == 1, "a ring has one enclosed hole"
    assert arc_percept.holes_of(lshape["cells"]) == 0, "an L-shape has NO enclosed hole"


def test_holes_counts_regions_not_cells_and_floods_from_a_margin():
    """THE CASE THE OLD SUITE NEVER REACHED, and the reason the second implementation survived.

    `sensors_heavy._holes` seeded its flood from the bbox BORDER cells, so an object occupying
    its own border blocked the flood and every interior cell read as enclosed. A 3x3 ring and
    an L-shape -- the only two shapes tested -- both happen to come out right under that bug,
    which is why it sat in the tree. A 5x5 ring does not: the old code returns 9 (the interior
    CELLS) where the answer is 1 (one enclosed REGION). Measured 56 disagreements of 263
    objects on wa30 before the two were merged.
    """
    ring5 = _obj([[2, 2, 2, 2, 2], [2, 0, 0, 0, 2], [2, 0, 0, 0, 2],
                  [2, 0, 0, 0, 2], [2, 2, 2, 2, 2]], 2)
    assert arc_percept.holes_of(ring5["cells"]) == 1, "one enclosed REGION, not nine cells"
    # a figure-eight is TWO regions, which a cell count also cannot say
    fig8 = _obj([[2, 2, 2], [2, 0, 2], [2, 2, 2], [2, 0, 2], [2, 2, 2]], 2)
    assert arc_percept.holes_of(fig8["cells"]) == 2, "two enclosed regions"


def test_perimeter_is_true_edge():
    """perimeter was the bbox 2*(h+w), undercounting the hole boundary."""
    ring = _obj([[2, 2, 2], [2, 0, 2], [2, 2, 2]], 2)
    assert arc_percept.perimeter_of(ring["cells"]) == 16, "ring outer 12 + inner hole 4"


def test_adjacency_is_true_cell_contact():
    """contactPoints was a bbox-gap test -- it false-fired on objects touching only diagonally."""
    board = [[3, 3, 0], [0, 0, 4]]  # obj3 and obj4 boxes abut; cells only meet at a diagonal
    a, b = _obj(board, 3), _obj(board, 4)
    assert arc_percept.contact_faces(a, b) == 0, "diagonal touch is not adjacency"
    touch = [[3, 4]]  # now genuinely 4-adjacent
    assert arc_percept.contact_faces(_obj(touch, 3), _obj(touch, 4)) > 0


def test_background_is_not_an_object():
    """detectors read raw components once -- the background field lit Adjacency for everything."""
    field = [[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1]]  # colour 1 = the field
    obs = observer.observe([{"grid": field}])
    assert obs[0]["n_objects"] == 1, "the field (largest component) must be dropped"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
    print(f"{len(fns)} perception checks pass")
