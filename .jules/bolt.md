## 2026-08-07 - Zone Priority and Road Map Lookups
**Learning:** In SentinelContext, zone priorities and component rendering repeatedly performed O(N) Array.prototype.find linear scans over roads for every zone ID. Pre-indexing roads into a Map in useMemo reduces priority recalculations and component rendering from O(Z * K * R) to O(R + Z * K).
**Action:** Always pre-index referenced list structures into a Map in React Context memoized selectors before mapping over dependent items.
