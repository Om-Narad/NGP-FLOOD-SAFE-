## 2026-09-07 - Map-based road resolution in SentinelContext
**Learning:** Re-computing zone priority and re-rendering feed items repeatedly called `Array.prototype.find` to resolve road objects by ID, scaling at $O(Z \times R \times N)$. Constructing a `Map(roads.map(r => [r.id, r]))` reduces lookups to $O(1)$ Hash Map accesses and attaching resolved objects to computed zones eliminates redundant scans during JSX rendering.
**Action:** Pass pre-indexed Maps to Context calculation functions and attach resolved objects directly to state items when calculating derived UI data.
