## 2026-08-30 - Map Lookup Optimization in Zone Priority Computation
**Learning:** In state management contexts like `SentinelContext`, re-computing derived priority scores for $Z$ zones against $R$ roads using array searching (`Array.prototype.find`) leads to unnecessary $O(Z \cdot R)$ overhead during state updates (such as road status toggling). Pre-indexing roads into a `Map` reduces priority recalculation time complexity to $O(Z + R)$.
**Action:** When computing relationship graph properties between entity collections in React state/reducers, construct Map indexes before iteration loops.
