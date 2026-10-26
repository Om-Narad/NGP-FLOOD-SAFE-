import time
import pytest
from regions import fetch_gdacs_live_flood_alerts, _GDACS_CACHE, _GDACS_CACHE_TTL

def test_gdacs_caching_performance():
    """
    Tests that fetch_gdacs_live_flood_alerts uses in-memory TTL caching,
    ensuring subsequent calls execute in sub-millisecond time.
    """
    # First call - fetches from network or cached state
    t0 = time.perf_counter()
    res1 = fetch_gdacs_live_flood_alerts()
    t1 = time.perf_counter()
    first_call_duration = t1 - t0

    # Second call - MUST hit in-memory TTL cache
    t2 = time.perf_counter()
    res2 = fetch_gdacs_live_flood_alerts()
    t3 = time.perf_counter()
    second_call_duration = t3 - t2

    # Verify both calls returned the same cached list reference
    assert res1 == res2
    # Verify cached call completed in under 1 millisecond (0.001s)
    assert second_call_duration < 0.001, f"Cached call took {second_call_duration:.6f}s, expected < 0.001s"

    print(f"\n[BENCHMARK] First call duration: {first_call_duration:.4f}s")
    print(f"[BENCHMARK] Cached call duration: {second_call_duration * 1000:.3f}ms")
