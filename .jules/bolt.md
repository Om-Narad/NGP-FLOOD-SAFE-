## 2026-10-17 - O(1) Road Lookups in Sentinel Context Priority Calculation

**Learning:** When calculating derived state across relational datasets (like zones and connected roads) in React context, using `Array.prototype.find` in nested loops inside `useMemo` can lead to $O(N \times R)$ work on every state update. Pre-indexing relational arrays into a `Map` reduces priority calculation to $O(N + R)$.
**Action:** When mapping over items that reference external entity IDs, always construct a `Map` or hash index first rather than scanning arrays with `.find()`.
