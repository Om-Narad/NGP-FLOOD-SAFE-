## 2026-08-21 - Caching Synchronous RSS Feed Endpoints in FastAPI
**Learning:** Synchronous network calls in FastAPI endpoints (such as fetching external XML RSS feeds via `urllib.request.urlopen`) block the execution thread for up to 4 seconds per request. Uncached endpoints reading external feeds cause high response latency and can hang the backend if external services slow down.
**Action:** Implement time-based in-memory TTL caching for external API/RSS data fetches to achieve <1ms response times on subsequent reads and protect against external API slowdowns.
