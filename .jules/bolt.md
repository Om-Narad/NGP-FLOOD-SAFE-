## 2026-08-07 - Zone Priority Score Computation Optimization
**Learning:** In React contexts recalculating derivative status arrays over collections (zones and roads), linear array search methods like `Array.prototype.find()` inside loop operations create $O(Z \times R)$ time complexity bottlenecks and unnecessary garbage collection.
**Action:** Pre-index lookup entities into a `Map` ($O(1)$ lookup time) inside `useMemo` before computing derived state across collections.
