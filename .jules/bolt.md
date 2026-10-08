## 2026-10-08 - O(1) Map Lookups for Linked Geospatial Entities
**Learning:** Re-computing priorities for nested geospatial entities (e.g., zones containing road IDs) using array `.find()` inside `.map()` loops creates an $O(Z \times R)$ bottleneck on state changes and component re-renders. Converting the array of linked entities into a `Map` prior to processing reduces lookup complexity to $O(1)$ per ID.
**Action:** Always pre-build a `Map` when referencing items by ID within render functions or calculations inside `useMemo`.
