## 2026-09-05 - [Single-Pass Road Counting in Priority Scoring]
**Learning:** In Python list filter operations that process road networks for each zone, chained list comprehensions `[r for r in roads if zone.id in r.connects_zone_ids]` and subsequent filtering allocate unnecessary intermediate list objects. Replacing them with a single-pass counting helper `_get_road_counts` avoids list allocations and reduces road iteration passes.
**Action:** Use single-pass count/aggregate loops when filtering road or network connections across elements in backend scoring algorithms.
