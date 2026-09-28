## 2026-09-28 - Precomputing Relational Road Objects in SentinelContext

**Learning:** In SentinelPlan's React context architecture, `computeZonePriority` evaluates priority for all zones whenever state changes. Doing $O(M)$ linear searches for road IDs both inside `computeZonePriority` and during `PriorityActionFeed` item rendering caused redundant $O(N \cdot M)$ scans on every render frame.
**Action:** Always construct an $O(1)$ Map lookup when computing relational state in `useMemo`, and attach precomputed relational objects (`connectedRoads`) onto derived state objects so child UI components don't re-query arrays during render loops.
