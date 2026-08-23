# Bolt's Journal - Critical Performance Learnings

## 2026-08-23 - Map Lookups for Zone Priority Scoring
**Learning:** `computeZonePriority` was doing repeated `Array.find()` calls inside `map()` over `zones` for every state re-render, leading to O(N*M) lookups where N is zones and M is roads. Pre-constructing a `Map` of roads by ID reduces lookup complexity to O(1) per zone road ID, achieving O(N + M) performance overall.
**Action:** Always pre-build key-value maps/dictionaries for multi-element relational lookups in React `useMemo` hooks.
