# MANIFEST -- derived by build_library.py, never edited by hand

## Files

| file | role | written by | read by |
|---|---|---|---|
| given.json | GIVEN: 4048 entries + sources, records, pending | build_library | library_runtime.old_files (Library.load, inherited.load, libagree) |
| frame.json | GIVEN vocabulary: 133 rows (READING, DOMAIN, CLUSTER, SOURCE) | build_library | old_files (Library.load, inherited.load, compile_term.readings) |
| index.json | DERIVED: index + tag | build_library | old_files (Library.load, inherited.load) |
| grammar.json | GIVEN, verbatim | nobody | nobody (no code opens it) |
| BUILD_REPORT.md | DERIVED report | build_library | people |
| MANIFEST.md | DERIVED: this file | build_library | people |
| library.db | DERIVED: the same rows as the four JSON, NOT committed | build_library | nothing until store step (5) |
| runtime.json, learnings.json | BUILT, absent | -- | Library.load if present |

## Entry fields, per kind

- PERCEPT: SOURCE ['symbol', 'status', 'name', 'domain', 'super_category', 'definition', 'tags', 'attributes', 'encodings', 'reach_tier', 'sources', 'used_by', 'used_in_domains', 'reads_weight', '@grounding', 'condition', 'symbol_collision', '@reads_explicit', 'working_set', 'aliases', 'merged_from', 'decomposition', 'role_of', 'chemistry']; DERIVED ['kind', 'grid', 'reads', 'affects', 'substrate', 'run', 'roles']
- COMPOSITE: SOURCE ['recipe', 'ingredients', 'bond', 'bond_status', 'recipe_tier', 'calls', 'depth', 'called_by', 'name', 'domain', 'super_category', 'definition', 'condition', 'tags', 'attributes', 'encodings', 'reach_tier', 'chemistry', 'sources', 'aliases', 'merged_from', 'role_of', 'working_set', 'definition_long', 'orientation', 'source_defect']; DERIVED ['kind', 'run', 'reads', 'affects', 'substrate', 'grid', 'roles']
- PRIMITIVE: SOURCE ['name', 'domain', 'status', 'in_type', 'out_type', 'also_accepts', 'operand_type', 'reads_operand', 'reads_ctx', 'elem_type', 'arm', 'on_arc_path', 'builder', 'defined_at', 'definition', 'realises', 'role_hint', 'sources', 'form', 'tags', 'reach_tier', 'reading', 'admitted', 'lit_by']; DERIVED ['kind', 'grid', 'reads', 'affects', 'substrate', 'run', 'roles']
- RELATION: SOURCE ['part', 'section', 'condition', 'status', 'arity', 'status_2026_09', 'on a grid', 'what it affords', 'section_as_parsed', 'what it removes', 'also', 'observable', 'direction', 'detectable as', 'contact required', 'ratio', 'after', 'what breaks']; DERIVED ['kind', 'reads', 'substrate', 'run', 'roles']

- folded build inputs (SOURCE): ['@grounding', '@reads_explicit']
