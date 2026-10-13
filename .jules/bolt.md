## 2026-10-13 - Context Value Object Memoization & O(1) Map Lookups
**Learning:** Creating unmemoized context value objects in top-level providers causes unnecessary re-renders across all consumer components on every state change. Additionally, computing derived zone priority scores with array `.find()` lookups on connected roads resulted in $O(Z \times R)$ time complexity.
**Action:** Always wrap context value objects in `useMemo` and provider actions in `useCallback`. Index list relations into `Map` data structures ($O(1)$ lookups) before executing batch computations.
