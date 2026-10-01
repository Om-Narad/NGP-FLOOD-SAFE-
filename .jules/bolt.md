## 2026-10-01 - O(1) Hash Map Road Lookups in React Context & Feed
**Learning:** Iterating over zones while repeatedly calling `Array.prototype.find()` on road arrays created an $O(Z \cdot K \cdot R)$ nested loop during state recomputations and list renders. Pre-indexing road entities in a `Map` reduces calculation complexity to $O(R + Z \cdot K)$.
**Action:** When computing multi-entity relational state in React context or list items, pre-build a `Map` for lookups instead of performing linear searches inside `.map()` or `.filter()` callbacks.
