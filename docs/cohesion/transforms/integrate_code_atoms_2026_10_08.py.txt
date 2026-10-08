"""Integrate the atoms the code builds (the seat's export, Drive 1dMTYaj9..., seat-act e50406d, 77 atoms
under any arm) into the ONE library, each in ONE place (Isaiah 2026-10-08: "we need cohesive library").

- The 27 EXTRACT atoms (one per ATTRIBUTE_TYPE row: colour, row, ... add_n) are PERCEPTION. They live
  in readings.json only; each reading records the code that reads it and the arm that publishes it.
- The 50 OPERATIONS live in agent_atoms.json as the PRIMITIVE layer: type signature, arm, where the
  code defines it, its meaning (from the code's own builder docstring, in brief), and -- where it
  executes one of the grammar's operators or NSM quantifiers -- WHICH one, so the grammar and its
  executable forms are joined, not duplicated.
Superfluous export fields (verbatim comment blocks, factory sites) are not carried: the code is the
record of those (fn_at points at it)."""
import json
# name: (in, out, also_accepts, operand_type, reads_ctx, elem_type, arm, builder, fn_at, meaning, realises)
OPS = {
 # PREDICT -- what the agent can bet an action does
 "idn": ("val","val",[],None,[],None,None,"predict","arc_predict.py:65","the value unchanged (the loop cannot run without it)",None),
 "translate": ("val","val",[],"@same",["operands"],None,None,"predict","arc_predict.py:79","add another slot's value (a displacement, never a constant)",None),
 "recolour": ("val","val",[],"COLOUR",["operands"],None,None,"predict","arc_predict.py:84","take another slot's colour",None),
 # SHAPE facts -- quantities read off the object's own cells
 "holes": ("SHAPE","EXTENT",[],None,[],None,None,"_shape_facts","arc_atoms.py:592","enclosed background regions in the shape",None),
 "parity": ("POSITION","BOOL",[],None,[],None,None,"_shape_facts","arc_atoms.py:601","even or odd",None),
 "centroid": ("OBJECT","POSITION",[],None,["obj"],None,None,"_shape_facts","arc_atoms.py:604","mean row of the object's own cells (one coordinate: a slot holds one)",None),
 "touching_n": ("OBJECT","EXTENT",[],None,["obj","touching"],None,None,"_shape_facts","arc_atoms.py:622","how many objects it is in contact with",None),
 "area": ("OBJECT","EXTENT",[],None,["obj"],None,None,"_shape_facts","arc_atoms.py:633","filled cell count (what h and w cannot give)",None),
 "perimeter": ("SHAPE","EXTENT",[],None,[],None,None,"_shape_more","arc_atoms.py:692","outline length",None),
 "corners": ("SHAPE","EXTENT",[],None,[],None,None,"_shape_more","arc_atoms.py:707","corner cells of the outline",None),
 "bbox_area": ("SHAPE","EXTENT",[],None,[],None,None,"_shape_more","arc_atoms.py:686","height times width of the bounding box",None),
 "orbit_size": ("SHAPE","EXTENT",[],None,[],None,None,"_shape_more","arc_atoms.py:735","how many distinct outlines under rotation and reflection",None),
 "canonical": ("SHAPE","SHAPE",[],None,[],None,None,"_shape_more","arc_atoms.py:724","the outline normalised under rotation and reflection",None),
 "symmetric": ("SHAPE","BOOL",[],None,[],None,None,"_shape_more","arc_atoms.py:745","unchanged under a reflection",None),
 "is_square": ("SHAPE","BOOL",[],None,[],None,None,"_shape_more","arc_atoms.py:751","height equals width",None),
 # TRANSFORM
 "rotate": ("SHAPE","SHAPE",[],None,[],None,None,"_transform","arc_atoms.py:453","turn the outline by 90 degrees",None),
 "reflect": ("SHAPE","SHAPE",[],None,[],None,None,"_transform","arc_atoms.py:459","mirror the outline",None),
 # BRIDGE
 "owner": ("val","OBJECT",[],None,["obj"],None,None,"_owner","arc_atoms.py:414","the object a slot's value belongs to (makes OBJECT-typed atoms reachable)",None),
 # CONTACT
 "touching": ("OBJECT","BOOL",[],None,["obj","touching"],None,None,"_contact","arc_atoms.py:782","shares a cell face with another object (the two-place relation, second operand from context)","NSM TOUCH(X, Y)"),
 # RELATE -- two values of one attribute
 "same": ("COLOUR","PRED",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],"@same",["operands"],None,None,"_relate","arc_atoms.py:805","equals another slot's value","≡ (identity test) / NSM THE SAME"),
 "other": ("COLOUR","PRED",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],"@same",["operands"],None,None,"_relate","arc_atoms.py:808","differs from another slot's value","¬≡ / NSM OTHER"),
 "above": ("POSITION","PRED",["EXTENT","DELTA"],"@same",["operands"],None,None,"_relate","arc_atoms.py:811","is greater than another slot's value (order, only on ordered types)","⋛ (comparison) / NSM MORE, ABOVE"),
 # OVER THE GROUP -- one attribute across every other object
 "all_same": ("COLOUR","PRED",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_over_group","arc_atoms.py:869","every object agrees on this attribute (empty group = unreadable, not true)","NSM ALL + THE SAME"),
 "any_same": ("COLOUR","PRED",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_over_group","arc_atoms.py:869","some other object shares this value","NSM SOME + THE SAME"),
 "none_same": ("COLOUR","PRED",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_over_group","arc_atoms.py:869","no other object shares this value","NSM NOT + SOME + THE SAME"),
 "count": ("COLOUR","EXTENT",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_over_group","arc_atoms.py:838","how many objects share this value (a cardinality, not a truth)","NSM MANY / quantity"),
 "rank_in": ("POSITION","EXTENT",["EXTENT","DELTA"],None,["group"],None,None,"_group_more","arc_atoms.py:907","position in the group's ordering","⋛ over a group"),
 "is_max": ("POSITION","BOOL",["EXTENT","DELTA"],None,["group"],None,None,"_group_more","arc_atoms.py:924","the largest in its group","⋛ over a group / NSM MORE"),
 "is_min": ("POSITION","BOOL",["EXTENT","DELTA"],None,["group"],None,None,"_group_more","arc_atoms.py:928","the smallest in its group","⋛ over a group"),
 "sum_group": ("POSITION","EXTENT",["EXTENT","DELTA"],None,["group"],None,None,"_group_more","arc_atoms.py:932","total over the group","+ over a group"),
 "distinct": ("COLOUR","EXTENT",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_group_more","arc_atoms.py:911","how many different values in the group","NSM OTHER, counted"),
 "is_mode": ("COLOUR","BOOL",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_group_more","arc_atoms.py:915","the most common value in the group",None),
 "aligned": ("COLOUR","BOOL",["POSITION","EXTENT","DELTA","SHAPE","BOOL"],None,["group"],None,None,"_group_more","arc_atoms.py:936","lined up with others on this attribute",None),
 "abs_delta": ("DELTA","EXTENT",[],None,[],None,None,"_group_more","arc_atoms.py:940","size of a signed change",None),
 "sign": ("DELTA","BOOL",[],None,[],None,None,"_group_more","arc_atoms.py:943","direction of a signed change",None),
 # CONNECT -- predicates joined: the grammar's operators, executable
 "negate": ("PRED","PRED",[],None,[],None,None,"_connect","arc_atoms.py:982","the predicate does not hold","¬ (negation) / NSM NOT"),
 "both": ("PRED","PRED",[],"PRED",["operands"],None,None,"_connect","arc_atoms.py:985","both predicates hold","+ (conjunction) / NSM AND"),
 "either": ("PRED","PRED",[],"PRED",["operands"],None,None,"_connect","arc_atoms.py:991","at least one predicate holds","∥ (disjunction)"),
 # QUANTIFY -- close a predicate into an objective
 "all": ("PRED","OBJ",[],None,[],None,None,"_quantify","arc_atoms.py:1006","closes a predicate (does not range over a scope; byte-identical to `any`; kept until all_of is shown to reproduce it)","NSM ALL (degenerate)"),
 "any": ("PRED","OBJ",[],None,[],None,None,"_quantify","arc_atoms.py:1007","closes a predicate (byte-identical to `all`)","NSM SOME (degenerate)"),
 "none": ("PRED","OBJ",[],None,[],None,None,"_quantify","arc_atoms.py:1008","closes a negated predicate","NSM NOT SOME (degenerate)"),
 # ITERATE -- walk a cell set (arm TETHER_ITERATE, on for ARC)
 "cells": ("SHAPE","CELLS",[],None,[],None,"arc_atoms._ITERATE","_iterate","arc_atoms.py:1030","open a shape into its cells","NSM PART"),
 "cell_row": ("CELL","POSITION",[],None,[],None,"arc_atoms._ITERATE","_iterate","arc_atoms.py:1038","a cell's row",None),
 "cell_col": ("CELL","POSITION",[],None,[],None,"arc_atoms._ITERATE","_iterate","arc_atoms.py:1041","a cell's column",None),
 "count_true": ("CELLS","EXTENT",[],None,[],"BOOL","arc_atoms._ITERATE","_iterate","arc_atoms.py:1044","how many cells a predicate held on (refuses non-boolean)","NSM MANY, counted"),
 "size": ("CELLS","EXTENT",[],None,[],None,"arc_atoms._ITERATE","_iterate","arc_atoms.py:1061","how many cells there are (the denominator)",None),
 "all_of": ("CELLS","OBJ",[],None,[],"BOOL","arc_atoms._ITERATE","_iterate","arc_atoms.py:1083","the predicate held on every cell","NSM ALL"),
 "some_of": ("CELLS","OBJ",[],None,[],"BOOL","arc_atoms._ITERATE","_iterate","arc_atoms.py:1083","the predicate held on at least one cell","NSM SOME"),
 "none_of": ("CELLS","OBJ",[],None,[],"BOOL","arc_atoms._ITERATE","_iterate","arc_atoms.py:1083","the predicate held on no cell","NSM NOT SOME"),
 "one_of": ("CELLS","OBJ",[],None,[],"BOOL","arc_atoms._ITERATE","_iterate","arc_atoms.py:1083","the predicate held on exactly one cell","NSM ONE"),
}
ROLE = {"translate":"PROCESS","recolour":"PROCESS","rotate":"PROCESS","reflect":"PROCESS","idn":"STATE","owner":"RELATION",
        "touching":"RELATION","same":"RELATION","other":"RELATION","above":"RELATION"}
for n,(i,o,*_r) in OPS.items():
    ROLE.setdefault(n, "MEASURE" if o=="EXTENT" else "TEST" if n in ("negate","both","either") else "STATE")
EXTRACT = {  # reading -> (arm, defined_at) from the export; perception, not operations
 "colour":(None,"arc_atoms.py:95"),"row":(None,"arc_atoms.py:95"),"col":(None,"arc_atoms.py:95"),"h":(None,"arc_atoms.py:96"),
 "w":(None,"arc_atoms.py:96"),"drow":(None,"arc_atoms.py:96"),"dcol":(None,"arc_atoms.py:96"),"shape":(None,"arc_atoms.py:97"),
 "completed":(None,"arc_atoms.py:123"),"contact":("arc_world._OBSERVER","arc_atoms.py:112"),"bbox":("arc_world._OBSERVER","arc_atoms.py:137"),
 "inside":("arc_world._OBSERVER","arc_atoms.py:175"),"dh":("arc_percept._OBSERVER","arc_atoms.py:128"),"dw":("arc_percept._OBSERVER","arc_atoms.py:128"),
 "dcells":("arc_percept._OBSERVER","arc_atoms.py:128"),"colour_changed":("arc_percept._OBSERVER","arc_atoms.py:134"),
 "dholes":("arc_percept._SHAPE_DELTA (on for ARC)","arc_atoms.py:143"),"dperimeter":("arc_percept._SHAPE_DELTA (on for ARC)","arc_atoms.py:143"),
 "age":("arc_percept._INSTRUMENTS","arc_atoms.py:148"),"speed":("arc_percept._INSTRUMENTS","arc_atoms.py:154"),"stability":("arc_percept._INSTRUMENTS","arc_atoms.py:169"),
 "add_n":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:181"),"rem_n":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:181"),
 "add_row":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:181"),"add_col":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:182"),
 "rem_row":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:182"),"rem_col":("arc_percept._CELL_CHANGE (import-time)","arc_atoms.py:182"),
}
R = json.load(open("readings.json"))
for r,(arm,at) in EXTRACT.items():
    assert r in R["readings"], r
    R["readings"][r]["code"] = {"extract_atom": r, "defined_at": at, "arm": arm, "source": "seat export 2026-10-08, seat-act e50406d"}
R["meta"]["code_note"] = "27 readings are also built as OBJECT->type extract atoms by arc_atoms._extract (one per ATTRIBUTE_TYPE row). They are PERCEPTION and are recorded HERE only, never again among the agent's operations."
json.dump(R, open("readings.json","w"), ensure_ascii=False, indent=1)
atoms = {}
for n,(i,o,also,opt,ctx,elem,arm,builder,at,meaning,real) in OPS.items():
    atoms[f"AGENT|{n}"] = {"name": n, "domain": "AGENT", "status": "executable", "in_type": i, "out_type": o,
        "also_accepts": also, "operand_type": opt, "reads_operand": opt is not None, "reads_ctx": ctx, "elem_type": elem,
        "arm": arm, "on_arc_path": True, "builder": builder, "defined_at": at, "definition": meaning,
        "realises": real, "role_hint": ROLE[n],
        "sources": ["seat export 2026-10-08 (seat-act e50406d)"]}
json.dump({"meta": {"source": "arc_atoms.three_spaces + arc_predict.predict, seat-act e50406d (seat export 2026-10-08)",
                    "count": len(atoms),
                    "what": "the agent's executable OPERATIONS (BUILT; kept apart from the GIVEN library for the ablation). Perception readings are in readings.json, not here. `realises` names the grammar operator or NSM prime an operation executes, joining grammar.json to its code.",
                    "superseded_by_metaprogramming": "negate/both/either are the executable forms of ¬ + ∥; under the one bind(bond, l, r) they are what a junction calls, not separate vocabulary. all/any are degenerate (byte-identical, no scope) and are superseded by all_of/some_of once shown to reproduce their bindings."},
           "atoms": atoms}, open("agent_atoms.json","w"), ensure_ascii=False, indent=1)
print("operations", len(atoms), "| readings annotated", len(EXTRACT))
