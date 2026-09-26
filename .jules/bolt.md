## 2026-09-26 - O(1) Pre-Indexed Zone-Road Lookups
**Learning:** Relational lookups between zones and roads were executing linear array scans (`Array.find` on frontend, list comprehensions on backend) during re-renders and road state toggles.
**Action:** Always pre-index roads into a `Map` or dictionary mapping `zone_id -> connected_roads` before batch processing zones to convert $O(N \times M)$ scans into $O(N + M)$ map lookups.
