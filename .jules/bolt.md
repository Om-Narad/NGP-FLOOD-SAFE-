## 2026-09-24 - React Context Memoization and Map Lookups
**Learning:** React Context value literals without `useMemo` trigger cascading re-renders across all consumer components on any state change. Additionally, repeated linear array lookups (`.find()`) inside render loops and recalculation functions scale as $O(N \cdot M)$.
**Action:** Always memoize context `value` objects with `useMemo`, wrap action handlers with `useCallback`, and pre-compute `Map` data structures for $O(1)$ entity lookups during render and priority scoring.
