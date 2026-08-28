## 2026-08-28 - React.memo Optimization on Priority Action Feed List Items
**Learning:** In list views with stateful items (such as selected/expanded cards or action buttons), rendering list items inline causes every item in the list to re-render when a single item is toggled or updated.
**Action:** Extract list item components, wrap with `React.memo`, and pass memoized callbacks via `useCallback` and memoized derived values via `useMemo` to eliminate unnecessary re-renders across unaffected items.
