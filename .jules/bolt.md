## 2026-10-16 - O(1) Hash Map Lookups in Computed State
**Learning:** Performing array `.find()` in repeated state computations (such as recalculating priorities for zones based on connected road status) creates an O(Z * R) bottleneck as dataset sizes grow. Creating a `Map` lookup table reduces complexity to O(Z + R).
**Action:** Always construct a `Map` or hash map when joining multiple state lists during memoized computation or render loops.
