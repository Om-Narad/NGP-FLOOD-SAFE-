# Bolt's Journal - Critical Learnings

## 2026-08-07 - Linear Road Scans in Computed Priority & Feed Renders
**Learning:** In SentinelPlan, `computeZonePriority` and `PriorityActionFeed` were performing $O(N)$ linear `.find()` scans on the `roads` array for every zone's connected road ID on every state recalculation and component re-render. Pre-building a `Map` lookup table for `roads` reduces lookup complexity from $O(Z \cdot K \cdot R)$ to $O(R + Z \cdot K)$ and attaching `connectedRoads` directly to computed zone objects eliminates redundant UI render searches completely.
**Action:** Always construct a `Map` or hash table when mapping relational IDs across state objects in React context providers and pass pre-computed relational objects to child views.
