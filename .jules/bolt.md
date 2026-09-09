## 2026-09-09 - Zone Priority Calculation Lookup Optimization

**Learning:** Calculating zone priorities across all zones re-evaluates road status links. Pre-building an in-memory `Map<id, Road>` prior to mapping over zones reduces time complexity from O(Z * R) to O(Z + R).

**Action:** Whenever iterating over items with relational IDs, convert lookup arrays to `Map` instances in `useMemo` hooks to avoid linear `Array.prototype.find` overhead during frequent re-renders or state recalculations.
