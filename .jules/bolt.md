# Bolt's Performance Journal

## 2026-03-31 - External RSS/Telemetry Caching Bottleneck
**Learning:** Synchronous external network requests to external telemetry sources (such as the GDACS RSS feed) directly inside FastAPI request handlers block worker threads for 1.8s–2.5s per invocation. In high-traffic disaster dashboards, repeated fetches for the same public feed compound latency and degrade backend throughput.
**Action:** Always add in-memory TTL caching with a thread lock around external telemetry feeds. Ensure graceful fallback to stale cached data when upstream feeds experience transient timeouts or downtime.
