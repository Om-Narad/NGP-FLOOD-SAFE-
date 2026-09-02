## 2026-08-07 - Replace linear `.find()` in React render and memoization loops with pre-built Maps
**Learning:** Performing `array.find()` inside React component render loops or memoized computation routines introduces an O(N * M) performance bottleneck that degrades rendering performance as datasets scale.
**Action:** Pre-index lookup datasets into a JS `Map` using `useMemo` or inside calculation scopes to turn repetitive O(M) linear array scans into O(1) hash map lookups.
