# Bolt's Performance Journal

## 2026-10-10 - Constant-Time Hash Map Road Lookups in React Context & Feeds
**Learning:** In React applications managing relational datasets (e.g., zones and connected roads), performing `Array.prototype.find()` on every render or recalculation scales linearly (O(N * M)). Memoizing a `Map` in React context transforms nested linear lookups into constant time O(1) hash map accesses, eliminating redundant array iterations across child components during state updates and re-renders.
**Action:** When child components or context computation functions reference entities by ID across render loops, index the lookup array into a memoized `Map` at the provider or container level.
