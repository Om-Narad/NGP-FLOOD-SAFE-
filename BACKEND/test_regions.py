import time
from unittest.mock import patch
from regions import (
    fetch_gdacs_live_flood_alerts,
    _GDACS_CACHE_TTL
)
import regions

def test_gdacs_caching_performance():
    """
    Tests that fetch_gdacs_live_flood_alerts uses in-memory TTL caching,
    ensuring subsequent calls execute in sub-millisecond time.
    """
    # First call - populates cache
    t0 = time.perf_counter()
    res1 = fetch_gdacs_live_flood_alerts()
    t1 = time.perf_counter()
    first_duration = t1 - t0

    # Second call - MUST hit in-memory TTL cache
    t2 = time.perf_counter()
    res2 = fetch_gdacs_live_flood_alerts()
    t3 = time.perf_counter()
    cached_duration = t3 - t2

    # Assert results are identical
    assert res1 == res2
    # Verify cached call completed in under 1 millisecond (< 0.001s)
    assert cached_duration < 0.001, f"Cached call took {cached_duration:.6f}s, expected < 0.001s"

    print(f"\n[BENCHMARK] First call duration: {first_duration:.4f}s")
    print(f"[BENCHMARK] Cached call duration: {cached_duration * 1000:.3f}ms")


def test_gdacs_cache_fallback_on_error():
    """
    Tests that if network request fails while cache exists,
    cached data is returned as fallback.
    """
    # Ensure cache has sample data
    regions._gdacs_cache = [{"title": "Cached Flood", "event_type": "Flood", "country": "Test", "coordinates": [0.0, 0.0], "pub_date": ""}]
    regions._gdacs_cache_time = time.time() - (_GDACS_CACHE_TTL + 10)  # Expired cache

    # Simulate network failure
    with patch("urllib.request.urlopen", side_effect=Exception("Network down")):
        alerts = fetch_gdacs_live_flood_alerts()
        assert len(alerts) == 1
        assert alerts[0]["title"] == "Cached Flood"
