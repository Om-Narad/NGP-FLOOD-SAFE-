## 2026-08-17 - O(1) Map Lookups for Dynamic Geospatial Relationships
**Learning:** In React applications managing dynamic geospatial or graph relationships (e.g. zones connecting to roads via ID arrays), using `Array.prototype.find` inside state recalculations (`useMemo`) or component render loops creates O(Z*R) computational overhead whenever road states change.
**Action:** Always pre-index relational entity lists into a Map (`new Map(roads.map(r => [r.id, r]))`) before mapping or evaluating relationships to achieve O(1) entity lookups and O(Z+R) overall time complexity.
