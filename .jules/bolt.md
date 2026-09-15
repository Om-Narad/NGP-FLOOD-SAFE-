## 2026-08-07 - Context Value Memoization & O(1) Road Lookup Optimization
**Learning:** SentinelContext created inline object references on every render, causing re-renders across all dashboard components. Additionally, zone priority scoring performed O(N) array `.find()` calls per connected road in render loops.
**Action:** Wrap context value in `useMemo` and state callbacks in `useCallback`. Build pre-indexed `Map` structures for O(1) road lookups during zone computations and card renders.
