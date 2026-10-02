# Bolt's Performance Journal

Critical performance learnings and insights for SentinelPlan.

## 2026-10-02 - O(1) Road Lookup Optimization in Zone Priority Calculation
**Learning:** Performing `Array.prototype.find()` across `roads` inside inner loops (like `computeZonePriority` mapped over `zones`) results in O(Z * R) operations on every state update or re-render. Converting the road array to a `Map` indexed by `road.id` reduces lookups to O(1), improving priority calculation time to O(Z + R).
**Action:** Always construct or memoize a lookup Map/dictionary when mapping over a collection and repeatedly matching items from another array by ID.
