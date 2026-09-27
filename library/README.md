# The library — four files

| file | what it holds |
|---|---|
| `atoms.json` | 1,748 atoms keyed `DOMAIN|Name` — 586 defined (have a symbol), 42 attribute-list only, 1,120 implicit (named in recipes, defined nowhere, added so every ingredient resolves) |
| `molecules.json` | 2,294 molecules — preloaded subroutines. `calls` lists ingredients that are themselves molecules; 762 molecules call others, up to 9 deep |
| `tag_index.json` | the lookup the agent queries: `by_tag`, `by_pair`, `by_attribute` → candidate keys, split into atoms and molecules |
| `domains.json` | 61 domains with super-category, root atom and adjacency neighbours |

## How the agent uses it

1. Perception detects attributes and their deltas.
2. Each attribute maps to a **tag** (a cluster). Look up the tag or the sorted pair `TAG1+TAG2` in `tag_index.json` — a direct key read, no scan.
3. Confirm each candidate against the board with its **`condition`** (2,638 entries carry one, e.g. Solidity: `overlapArea == 0`).
4. Molecules are callable: resolve `ingredients` by key, recursing through `calls`.

## Tags on every entry

Each entry carries `tags.primary` (up to three), `tags.pairs` (the intersections to query) and `tags.scored`, where every tag lists the evidence behind it: `measured` (already in ATTRIBUTE_INDEX), `ruled`, `proposed`, `encoding`, `name`, `inherited` (from ingredients) or `used-by` (from the molecules that use it).

Coverage: 34% of entries had a measured cluster; 95% now carry at least one tag.

**Tags ending in `*` are proposals** — 17 new clusters built only from head words that occur in the unassigned list. They raise attribute-mention coverage from 22% to 47%. The cluster doc says new clusters are a ruling, so these need yours before they count as settled.

## Known limits

- **Bonds are unstated in 2,268 of 2,294 recipes** (`+` only), so isomers such as Melt and Freeze read identically until their operators are written.
- **Implicit atoms are placed in the domain that uses them most** (`used_in_domains` shows the spread). `Action` is used 115 times across many domains; its placement is a convention, not a finding.
- **`phase` is tagged TIME**, per the existing ruling. In HEAT (Melt, Freeze, Boil) it means matter-phase, which is a STATE. Worth a second look.
- **Some names appear twice** as a truncated and a full form (e.g. ADHERENCE `Principle cons` / `Principle consistency`), inherited from the source lists.
