# Bolt's Performance Journal

## 2026-08-07 - Pre-computed Entity Lookups in React Context Memoization
**Learning:** Performing `Array.prototype.find()` lookups inside component render loops (e.g. mapping over zones and looking up connected roads by ID inside JSX) creates O(Z * R) linear overhead on every render frame and state update. By converting linear lists to `Map` lookups during context level `useMemo` and attaching pre-computed entity arrays (`connectingRoads`) directly onto calculated objects, component renders are reduced to O(1) direct property access.
**Action:** When computing derived state in context providers, attach associated sub-entities directly to the memoized objects to avoid redundant `Array.find()` lookups inside consumer components.
