import time
import pytest
from unittest.mock import patch, MagicMock
import regions

SAMPLE_RSS_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <channel>
    <title>GDACS Alerts</title>
    <item>
      <title>Flood Alert in Region A</title>
      <gdacs:eventtype>FL</gdacs:eventtype>
      <gdacs:country>Country A</gdacs:country>
      <geo:lat>24.5</geo:lat>
      <geo:long>91.5</geo:long>
      <pubDate>Wed, 07 Aug 2026 12:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Earthquake Alert</title>
      <gdacs:eventtype>EQ</gdacs:eventtype>
      <gdacs:country>Country B</gdacs:country>
      <geo:lat>10.0</geo:lat>
      <geo:long>20.0</geo:long>
      <pubDate>Wed, 07 Aug 2026 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


@pytest.fixture(autouse=True)
def reset_gdacs_cache():
    """Resets global cache state before and after each test."""
    regions._gdacs_cache = None
    regions._gdacs_cache_time = 0.0
    yield
    regions._gdacs_cache = None
    regions._gdacs_cache_time = 0.0


def test_fetch_gdacs_live_flood_alerts_populates_cache():
    """Verifies that the first call executes network request and populates the cache."""
    mock_response = MagicMock()
    mock_response.read.return_value = SAMPLE_RSS_XML
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        alerts = regions.fetch_gdacs_live_flood_alerts(ttl=60)
        assert len(alerts) == 1
        assert alerts[0]["title"] == "Flood Alert in Region A"
        assert alerts[0]["event_type"] == "Flood"
        assert alerts[0]["country"] == "Country A"
        assert alerts[0]["coordinates"] == [24.5, 91.5]
        assert mock_urlopen.call_count == 1

        # Check cache state
        assert regions._gdacs_cache == alerts
        assert regions._gdacs_cache_time > 0


def test_fetch_gdacs_live_flood_alerts_cache_hit_avoids_network():
    """Verifies that subsequent calls within TTL use the cache without calling urllib."""
    mock_response = MagicMock()
    mock_response.read.return_value = SAMPLE_RSS_XML
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        # First call: triggers fetch
        alerts_1 = regions.fetch_gdacs_live_flood_alerts(ttl=60)
        assert mock_urlopen.call_count == 1

        # Second call: within TTL, should hit cache
        alerts_2 = regions.fetch_gdacs_live_flood_alerts(ttl=60)
        assert mock_urlopen.call_count == 1
        assert alerts_1 == alerts_2


def test_fetch_gdacs_live_flood_alerts_cache_expiry():
    """Verifies that when TTL expires, the cache is refreshed."""
    mock_response = MagicMock()
    mock_response.read.return_value = SAMPLE_RSS_XML
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        # First call
        regions.fetch_gdacs_live_flood_alerts(ttl=0.05)
        assert mock_urlopen.call_count == 1

        # Wait for TTL to expire
        time.sleep(0.06)

        # Second call should trigger another network call
        regions.fetch_gdacs_live_flood_alerts(ttl=0.05)
        assert mock_urlopen.call_count == 2


def test_fetch_gdacs_live_flood_alerts_fallback_on_network_failure():
    """Verifies graceful fallback to cached alerts if network fails on refresh."""
    # Seed cache
    cached_data = [{"title": "Cached Disaster", "event_type": "Flood", "country": "Test", "coordinates": [0.0, 0.0]}]
    regions._gdacs_cache = cached_data
    regions._gdacs_cache_time = time.time() - 100  # Expired cache

    with patch("urllib.request.urlopen", side_effect=Exception("Connection timed out")):
        alerts = regions.fetch_gdacs_live_flood_alerts(ttl=60)
        # Should return stale cache instead of empty list
        assert alerts == cached_data
