# Bolt's Journal - Critical Learnings

## 2026-08-07 - Relational Lookups in Context State Calculation
**Learning:** In React Context state pipelines where zones depend on relational roads (`zone.roadIds`), calling `roads.find()` inside `map` across $N$ zones causes $O(N \cdot K \cdot M)$ searches on every render/state update. Passing pre-built `Map` instances in `useMemo` and attaching computed relations directly to context objects turns relational resolution into $O(1)$ lookups and eliminates redundant array searches in consumer components.
**Action:** When computing relational derived state in Context or components, always pre-construct `Map` instances for foreign key lookups and attach resolved relations to the memoized payload.
