# Bolt's Performance Journal

## 2026-08-07 - Synchronous External Network Requests in API Handlers
**Learning:** Endpoints like `/api/gdacs-live` that issue synchronous `urllib` HTTP requests to external RSS/REST services block thread pool execution and introduce 300ms–4000ms response latencies per request.
**Action:** Always implement an in-memory TTL cache (or background async refresher) for external telemetry and feed endpoints so API hits serve instantly (< 1ms).
