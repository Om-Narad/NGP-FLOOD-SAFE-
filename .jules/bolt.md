## 2026-09-21 - Map indexing for relation lookups in React Context & Feed
**Learning:** Performing `Array.prototype.find()` lookups inside nested loops/maps over state collections (e.g., matching connected roads per hazard zone) creates an unnecessary $O(Z \times R)$ quadratic bottleneck whenever state updates or re-renders trigger.
**Action:** Pre-index relational entities into a `Map` ($O(R)$ construction) using `useMemo` or prior to batch operations, reducing element lookup time to $O(1)$ and total execution to $O(Z + R)$.
