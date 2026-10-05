## 2026-10-05 - React Context Value Memoization & Derived Props
**Learning:** Instantiating inline object literals as React Context provider values causes all consumer components to re-render whenever the provider updates, even for unrelated state changes (like toast auto-dismissals).
**Action:** Always wrap context `value` objects in `useMemo`, memoize handler functions with `useCallback`, and expose pre-computed array lookups on derived data objects to avoid repeated $O(N \cdot M)$ searches during component rendering.
