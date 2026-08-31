## 2025-02-18 - Zone Priority Road Map Lookup Optimization

**Learning:** Replacing nested Array `.find()` linear searches inside list transformation pipelines (like `computeZonePriority`) with a pre-built `Map` indexed by key reduced calculation time by ~6.2x ($O(Z \times K \times R) \rightarrow O(R + Z \times K)$).
**Action:** When computing properties across lists with relational key references (e.g. zones to roads), always pre-index items in a `Map` before iterating.
