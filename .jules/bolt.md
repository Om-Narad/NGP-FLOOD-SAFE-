## 2026-08-07 - Zone Road Lookups Optimization
**Learning:** In React applications with connected entities (such as zones referencing road IDs), performing linear array searches (`Array.prototype.find`) inside loop mappings or unmemoized card components scales as O(Z * K * R) on every state update or render.
**Action:** Pre-index relational arrays into `Map` instances (`new Map(items.map(i => [i.id, i]))`) within `useMemo`, and defer nested entity lookups to only render when UI sections (such as accordion cards) are expanded.
