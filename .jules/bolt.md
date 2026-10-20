## 2026-10-20 - Map Lookups for React Context Re-computations

**Learning:** In SentinelContext, zone priority calculation (`computeZonePriority`) was performing repeated $O(M)$ array lookups (`roadsList.find()`) for every road ID in every zone on state updates ($O(N \cdot M)$). Creating a pre-indexed `Map` once per context update reduces complexity to $O(N + M)$ without architectural changes.
**Action:** When computing derived state over collection relationships in React Context or `useMemo`, pre-index foreign keys into a `Map` or hash table prior to mapping over the primary list.
