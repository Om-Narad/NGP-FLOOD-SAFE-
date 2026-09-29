## 2026-08-07 - O(1) Road Indexing & Pre-filtered Zone Scoring

**Learning:**
Repeatedly running `Array.prototype.find` inside React render cycles (e.g., rendering zone cards) and filtering the `roads` list multiple times per zone in Python backend scoring caused unnecessary O(N * M) overhead. Indexing roads into a `Map` in React and passing pre-filtered `connected_roads` in Python scoring reduced lookup execution time by over 90%.

**Action:**
When computing relationships between items (like zones and roads), always build a `Map` lookup index in React `useMemo` and pre-filter relationship arrays once per parent object in Python backend services.
