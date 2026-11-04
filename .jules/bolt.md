## 2026-08-07 - GDACS Live Flood Telemetry Caching
**Learning:** External RSS feeds (like GDACS) in synchronous backend endpoints introduce ~2000ms latency per request and block event loops/threads, but alert feeds update on multi-minute intervals where fresh HTTP fetches on every client call are wasteful.
**Action:** Implement thread-safe in-memory caching with double-checked locking and shallow copies of cached lists to protect data integrity while achieving >99.9% latency reduction and resilience against upstream network timeouts.
