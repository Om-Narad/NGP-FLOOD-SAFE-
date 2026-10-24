## 2026-10-24 - O(1) Map Lookups for Zone Priority and Feeds
**Learning:** Performing `Array.prototype.find` inside iterative calculations (such as computing zone priority across multiple connected roads) scales linearly $O(Z \times R)$. Memoizing an ID-indexed `Map` reduces road lookups to constant time $O(1)$.
**Action:** When mapping relationships between entities (e.g. zones and roads), memoize a `Map` indexed by entity ID in Context/store to avoid repeated $O(N)$ linear array scans during render loops or state recalculations.
