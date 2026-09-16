import time
import pytest
import regions

def test_gdacs_caching_and_expiration():
    # Clear cache state
    regions._gdacs_cache["timestamp"] = 0.0
    regions._gdacs_cache["data"] = []

    # Inject dummy data into cache
    dummy_data = [{"title": "Test Flood", "event_type": "Flood", "country": "Testland", "coordinates": [0.0, 0.0], "pub_date": "2026"}]
    regions._gdacs_cache["timestamp"] = time.time()
    regions._gdacs_cache["data"] = dummy_data

    # Call with non-expired TTL -> should return dummy_data instantly from cache
    alerts = regions.fetch_gdacs_live_flood_alerts(ttl=60)
    assert alerts == dummy_data

    # Force expiration by setting timestamp far in the past
    regions._gdacs_cache["timestamp"] = time.time() - 1000.0

    # Call with expired TTL (and mocked/real fetch)
    # The cache should update with fresh list or fallback
    fresh_alerts = regions.fetch_gdacs_live_flood_alerts(ttl=60)
    assert isinstance(fresh_alerts, list)

def test_gdacs_fallback_on_error(monkeypatch):
    # Set cache with known fallback data
    fallback_data = [{"title": "Cached Flood", "event_type": "Flood", "country": "Fallback", "coordinates": [1.0, 1.0], "pub_date": "2026"}]
    regions._gdacs_cache["timestamp"] = 0.0  # Force fetch attempt
    regions._gdacs_cache["data"] = fallback_data

    # Mock urlopen to raise an exception
    def mock_urlopen(*args, **kwargs):
        raise Exception("Network failure test")

    monkeypatch.setattr(regions.urllib.request, "urlopen", mock_urlopen)

    # Calling fetch should catch exception and return fallback data
    alerts = regions.fetch_gdacs_live_flood_alerts(ttl=60)
    assert alerts == fallback_data
