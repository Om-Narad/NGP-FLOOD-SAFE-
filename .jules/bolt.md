## 2026-09-08 - O(1) Road Lookup & Zone Priority Optimization
**Learning:** In SentinelPlan's architecture, zone priority computation and list rendering were repeatedly searching the `roads` array using `Array.find` ($O(M)$) for every zone ($N$) on every render. Indexing roads into a `Map` ($O(1)$) and storing `connectedRoads` on zone objects during priority computation eliminates $O(N \cdot M)$ searches during UI re-renders and accordion toggles.
**Action:** Always pre-index referenced entity arrays into Maps when computing derived state in React context providers.
