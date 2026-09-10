# Bolt's Journal - Critical Learnings

## 2026-09-10 - O(1) Road Lookups in React Context Zone Priority Calculation
**Learning:** Computing zone priority score iterated over `roadIds` and performed `roadsList.find(r => r.id === id)` linear search for each ID per zone on every render/state update. Building a Map lookup table reduces complexity from O(Z * R) to O(Z + R).
**Action:** Construct Map indexed by road ID when matching roads to zones or processing entity relationships in React state pipelines.
