## 2026-09-03 - Pre-indexed Road Mapping for Zone Priority Evaluation
**Learning:** In disaster management telemetry, re-calculating zone priority scores involves matching zones with connected evacuation roads. Doing linear array searches (`roads.find` / list comprehensions) inside nested zone loops results in $O(N \times M)$ overhead whenever state updates or road statuses toggle.
**Action:** Build an indexed lookup map (`zone_to_roads` / `roadsMap`) prior to zone iterations to achieve $O(1)$ road lookups and avoid redundant memory allocations.
