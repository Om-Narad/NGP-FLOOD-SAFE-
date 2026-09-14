# Bolt's Performance Journal

## 2026-09-14 - Map Lookups and Deferred Evaluation for Component Collections
**Learning:** Performing repeated array `.find()` lookups inside nested loops or React render maps scales as $O(N \times M)$ on every state update or render frame. Converting lookups to $O(1)$ Map queries and deferring non-visible computations (e.g. accordion details) eliminates unnecessary work and keeps main thread framerates high.
**Action:** Always construct a Map for repetitive key-based entity lookups and lazy-evaluate hidden sub-component attributes in React card lists.
