import time
from unittest.mock import patch, MagicMock
import pytest

from regions import (
    fetch_gdacs_live_flood_alerts,
    _gdacs_cache,
    _gdacs_cache_lock,
    GDACS_CACHE_TTL_SECONDS
)

MOCK_XML_RESPONSE = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <channel>
    <title>GDACS Alerts</title>
    <item>
      <title>Flood in Test Region</title>
      <gdacs:eventtype>FL</gdacs:eventtype>
      <gdacs:country>Testland</gdacs:country>
      <geo:lat>12.34</geo:lat>
      <geo:long>56.78</geo:long>
      <pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


@pytest.fixture(autouse=True)
def reset_cache():
    """Resets the module-level GDACS cache before each test."""
    with _gdacs_cache_lock:
        _gdacs_cache["data"] = None
        _gdacs_cache["timestamp"] = 0.0
    yield
    with _gdacs_cache_lock:
        _gdacs_cache["data"] = None
        _gdacs_cache["timestamp"] = 0.0


def test_fetch_gdacs_live_flood_alerts_caches_response():
    """Test that subsequent calls within TTL use cache and do not make network calls."""
    mock_urlopen = MagicMock()
    mock_response = MagicMock()
    mock_response.read.return_value = MOCK_XML_RESPONSE
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        # 1st call: Should hit network
        alerts_1 = fetch_gdacs_live_flood_alerts(ttl_seconds=10.0)
        assert len(alerts_1) == 1
        assert alerts_1[0]["title"] == "Flood in Test Region"
        assert alerts_1[0]["country"] == "Testland"
        assert mock_urlopen.call_count == 1

        # 2nd call: Should return cached copy without network call
        alerts_2 = fetch_gdacs_live_flood_alerts(ttl_seconds=10.0)
        assert alerts_2 == alerts_1
        assert mock_urlopen.call_count == 1  # No additional network request


def test_fetch_gdacs_live_flood_alerts_ttl_expiration():
    """Test that expired TTL causes a cache refresh."""
    mock_urlopen = MagicMock()
    mock_response = MagicMock()
    mock_response.read.return_value = MOCK_XML_RESPONSE
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        # 1st call with very small TTL
        alerts_1 = fetch_gdacs_live_flood_alerts(ttl_seconds=0.05)
        assert mock_urlopen.call_count == 1

        # Wait for TTL to expire
        time.sleep(0.06)

        # 2nd call after expiration should re-fetch
        alerts_2 = fetch_gdacs_live_flood_alerts(ttl_seconds=0.05)
        assert mock_urlopen.call_count == 2
        assert alerts_2 == alerts_1


def test_fetch_gdacs_live_flood_alerts_fallback_on_network_failure():
    """Test that network failures fall back to cached data if available."""
    mock_urlopen = MagicMock()
    mock_response = MagicMock()
    mock_response.read.return_value = MOCK_XML_RESPONSE
    mock_urlopen.return_value.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", mock_urlopen):
        # Prime cache
        alerts_1 = fetch_gdacs_live_flood_alerts(ttl_seconds=1.0)
        assert len(alerts_1) == 1

    # Now make urlopen fail
    failing_urlopen = MagicMock(side_effect=Exception("Network error"))
    with patch("urllib.request.urlopen", failing_urlopen):
        # Force refresh or expired TTL should catch exception and fallback to cached data
        alerts_fallback = fetch_gdacs_live_flood_alerts(force_refresh=True)
        assert len(alerts_fallback) == 1
        assert alerts_fallback[0]["title"] == "Flood in Test Region"
