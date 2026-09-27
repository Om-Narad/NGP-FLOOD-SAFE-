## 2026-09-27 - Map vs Array.find in Zone Priority Computation
**Learning:** Using `Map` lookups instead of `Array.prototype.find()` inside React rendering loops and `useMemo` zone processing reduces time complexity from $O(N \times M \times R)$ to $O(N \times M)$, delivering instant UI feedback when toggling roads or re-evaluating risk priority.
**Action:** When mapping sub-entity lists (e.g. connected roads to zones or responders to alerts), pre-build a `Map` lookup table before looping.
