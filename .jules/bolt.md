## 2026-10-28 - Map-based road indexing for zone priority calculation
**Learning:** Linear array searches (`Array.find`) inside nested state computation loops (such as mapping over $Z$ zones, each searching $R$ roads by ID) create $O(Z \cdot R)$ scaling bottlenecks on every state update or re-render.
**Action:** Always construct a memoized `Map` (`roadsMap`) for ID-based lookups when computing derived relational state in React Context or custom hooks.
