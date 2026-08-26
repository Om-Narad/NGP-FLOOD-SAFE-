# Bolt's Performance Journal

## 2026-08-26 - Map Lookups and Context Memoization for Zone Priority Calculations
**Learning:** Nested array `.find()` lookups during context state computation and component render loops cause $O(Z \cdot K \cdot R)$ time complexity, leading to redundant scans whenever context state changes. Constructing an $O(1)$ `Map` during `useMemo` computation yields an ~11x speedup, and pre-computing `roadObjs` on calculated zone objects removes render-time searches in list items. Additionally, memoizing context Provider `value` prevents cascading re-renders across all consumer components.
**Action:** Always pre-build indexed `Map` lookups for relational data in `useMemo` context calculations and pass pre-resolved relational objects to list components. Always memoize React context `value` objects with `useMemo`.
