# Bolt Performance Journal

## 2026-09-11 - Map Lookup Optimization in Zone Scoring
**Learning:** React state re-computations that iterate over collections to perform array linear scans (`Array.find`) inside nested loops (`Array.map`) cause quadratic performance $O(Z \times R)$ on state updates. Using `Map` pre-indexing drops lookups to $O(1)$, reducing algorithm time to $O(Z \times M)$.
**Action:** When mapping over dependent entities in `useMemo` or state calculation functions, pre-index referenced collections in a `Map` keyed by unique ID before running nested iterations.
