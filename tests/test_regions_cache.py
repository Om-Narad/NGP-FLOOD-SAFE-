"""
Unit tests for fetch_gdacs_live_flood_alerts caching behavior.
"""

import time
import io
import urllib.request
import pytest
from unittest.mock import patch, MagicMock

import regions
from regions import fetch_gdacs_live_flood_alerts, _GDACS_CACHE

SAMPLE_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <channel>
    <title>GDACS Alerts</title>
    <item>
      <title>Flood in Testland</title>
      <gdacs:eventtype>FL</gdacs:eventtype>
      <gdacs:country>Testland</gdacs:country>
      <geo:lat>12.34</geo:lat>
      <geo:long>56.78</geo:long>
      <pubDate>Mon, 01 Jan 2026 12:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Earthquake in Otherland</title>
      <gdacs:eventtype>EQ</gdacs:eventtype>
      <gdacs:country>Otherland</gdacs:country>
      <geo:lat>0.0</geo:lat>
      <geo:long>0.0</geo:long>
      <pubDate>Mon, 01 Jan 2026 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""

@pytest.fixture(autouse=True)
def reset_cache():
    """Resets the module-level cache before each test."""
    _GDACS_CACHE["alerts"] = []
    _GDACS_CACHE["last_fetched"] = 0.0
    _GDACS_CACHE["ttl_seconds"] = 60.0
    yield
    _GDACS_CACHE["alerts"] = []
    _GDACS_CACHE["last_fetched"] = 0.0


def test_fetch_parses_and_caches_live_flood_alerts():
    mock_response = MagicMock()
    mock_response.read.return_value = SAMPLE_XML
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        alerts = fetch_gdacs_live_flood_alerts()

        assert len(alerts) == 1
        assert alerts[0]["title"] == "Flood in Testland"
        assert alerts[0]["country"] == "Testland"
        assert alerts[0]["coordinates"] == [12.34, 56.78]
        assert mock_urlopen.call_count == 1

        # Second call immediately within TTL should hit cache without network call
        cached_alerts = fetch_gdacs_live_flood_alerts()
        assert cached_alerts == alerts
        assert mock_urlopen.call_count == 1  # No additional network call


def test_cache_refreshes_after_ttl_expires():
    mock_response = MagicMock()
    mock_response.read.return_value = SAMPLE_XML
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        # First call: populates cache
        fetch_gdacs_live_flood_alerts()
        assert mock_urlopen.call_count == 1

        # Fast forward time beyond TTL
        _GDACS_CACHE["last_fetched"] = time.time() - 61.0

        # Second call: TTL expired, should make another network call
        fetch_gdacs_live_flood_alerts()
        assert mock_urlopen.call_count == 2


def test_fetch_falls_back_to_cached_data_on_error():
    # Pre-populate cache
    cached_data = [{"title": "Cached Flood", "event_type": "Flood", "country": "Oldland", "coordinates": [1.0, 2.0], "pub_date": ""}]
    _GDACS_CACHE["alerts"] = cached_data
    _GDACS_CACHE["last_fetched"] = time.time() - 100.0  # Expired cache

    # Simulate network failure on refresh
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Network unreachable")):
        alerts = fetch_gdacs_live_flood_alerts()
        # Should return cached data rather than failing or returning empty list
        assert alerts == cached_data
