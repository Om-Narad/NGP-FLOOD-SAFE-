## 2026-09-12 - O(1) Map Lookups for Relational Data in React State

**Learning:** When React components re-render or re-compute scores across relational entities (like zones referencing roads by ID), nested `Array.prototype.find()` calls cause an O(Z * R) bottleneck on every state change and render pass.

**Action:** Convert relational array datasets into a memoized `Map` (`useMemo(() => new Map(data.map(item => [item.id, item])), [data])`) at the context layer, providing O(1) lookup time across scoring calculations and child component renders.
