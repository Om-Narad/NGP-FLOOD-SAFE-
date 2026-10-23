## 2026-10-23 - Avoid redundant O(N) list filtering during multi-property calculations
**Learning:** Functions that evaluate properties of the same entity (e.g. `calculate_priority` and `generate_rationale` for a `Zone`) independently filtered the full list of `Road` objects. Pre-filtering connected roads once per zone and passing them directly reduces list traversals from 4x per zone to 1x.
**Action:** When evaluating multiple metrics or explanations for an item against a collection, pass pre-filtered references or generator expressions to avoid repeated O(N) filter passes.
