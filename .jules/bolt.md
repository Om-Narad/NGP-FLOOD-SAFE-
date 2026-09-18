# Bolt's Journal

Critical learnings and codebase-specific performance insights.

## 2026-09-18 - Hash Map Lookups for Zone Priority Computation
**Learning:** In `SentinelContext.jsx`, computing zone priority repeatedly searched through the `roads` array using `.find()` inside a loop over `zones`. Replacing this nested $O(Z \times R)$ array search with an $O(1)$ Map index drastically reduces calculation overhead during frequent state updates and re-renders.
**Action:** Always construct indexed Map/Dictionary lookups before performing multi-item associations in React context selectors and memoized values.
