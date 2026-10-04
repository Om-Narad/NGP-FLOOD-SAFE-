## 2026-10-04 - Optimize Zone Priority Road Lookup with O(1) Map
**Learning:** In React context providers or state evaluation loops, passing arrays to helper functions that perform `.find()` inside mapping loops creates an O(Z * K * R) bottleneck. Converting arrays to an `O(1)` Map prior to evaluating zones reduces computation complexity to `O(R + Z * K)`, speeding up zone priority re-scoring by ~3.3x.
**Action:** When computing properties across nested relational entities (e.g. zones connected to roads), construct `Map` lookups outside the inner evaluation loop or `useMemo` map calls.
