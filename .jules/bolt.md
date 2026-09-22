# Bolt's Journal

## 2026-09-22 - Optimize road lookups with Map in React state calculations
**Learning:** Performing `Array.prototype.find()` inside mapping loops over React state arrays (e.g. zones and road connections) causes unnecessary $O(N \times M)$ overhead during state updates and re-renders. Building a temporary `Map` indexed by entity ID once per recalculation turns lookups into $O(1)$ operations.
**Action:** When calculating derived state across relational items in React contexts or components, construct a lookup `Map` first before looping over items.
