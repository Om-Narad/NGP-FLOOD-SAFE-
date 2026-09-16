## 2026-09-16 - GDACS Live RSS Feed In-Memory TTL Caching
**Learning:** Live external RSS/XML feeds (such as GDACS disaster telemetry) fetched synchronously inside FastAPI endpoint handlers introduce blocking HTTP latency (~1.8s per request). In-memory TTL caching (5 minutes) completely eliminates network overhead for repeated API calls without sacrificing freshness.
**Action:** Always wrap external RSS/API telemetry endpoints with an in-memory TTL cache to maintain sub-millisecond response times.
