# Bolt Performance Journal

## 2026-08-07 - O(1) Map Indexing for Linked Geographic Entities in React Context

**Learning:** In SentinelPlan's state architecture, zones contain lists of connected road IDs. During state re-computation in `useMemo` and inside component render loops (`PriorityActionFeed`), calling `roads.find(r => r.id === id)` repeatedly caused O(Z * K * R) operations per calculation/render cycle.

**Action:** Always pre-index linked collections into a `Map` (`new Map(roads.map(r => [r.id, r]))`) when deriving state in context providers, and attach resolved entities (`connectedRoads`) directly to computed zone objects so UI components do not perform redundant array scans during render frames.
