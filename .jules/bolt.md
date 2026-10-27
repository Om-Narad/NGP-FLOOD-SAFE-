# Bolt's Journal - Critical Performance Learnings

## 2026-10-27 - Map lookups and precomputed filtering for road-zone relations
**Learning:** In dual-tier dashboard architectures (React + FastAPI) tracking connected geospatial objects, iterating over arrays with `find()` or list comprehensions inside component render loops and multi-step scoring logic creates $O(N \times M)$ bottlenecks.
**Action:** Always pre-build `Map` lookup maps in React contexts/components and pass precomputed filtered relation subsets into chained backend scoring functions.
