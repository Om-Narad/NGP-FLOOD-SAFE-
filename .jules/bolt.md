## 2026-10-25 - O(1) Map Lookup for Zone-Road Priority Computation
**Learning:** Array search operations (`Array.prototype.find`) inside repeated iterations or `useMemo` hooks calculating metrics across dataset entities (zones & connected roads) scale as O(M * K * N). Converting entity arrays to a `Map` once per calculation reduces lookups to O(1) time complexity.
**Action:** Always construct lookup Maps when correlating relational array data in React state calculation hooks before mapping through nested records.
