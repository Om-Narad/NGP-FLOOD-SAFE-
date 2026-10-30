import time
from unittest.mock import patch, MagicMock
import regions

def test_gdacs_caching():
    # Reset cache state before test
    regions._GDACS_CACHE_DATA = None
    regions._GDACS_CACHE_TIMESTAMP = 0.0

    mock_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:gdacs="http://www.gdacs.org" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
      <channel>
        <item>
          <title>Test Flood Alert</title>
          <gdacs:eventtype>FL</gdacs:eventtype>
          <gdacs:country>India</gdacs:country>
          <geo:lat>26.18</geo:lat>
          <geo:long>91.74</geo:long>
          <pubDate>Thu, 07 Aug 2026 14:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>"""

    mock_response = MagicMock()
    mock_response.read.return_value = mock_xml
    mock_response.__enter__.return_value = mock_response

    with patch('urllib.request.urlopen', return_value=mock_response) as mock_urlopen:
        # First call should hit network (urlopen)
        alerts1 = regions.fetch_gdacs_live_flood_alerts()
        assert len(alerts1) == 1
        assert alerts1[0]['title'] == 'Test Flood Alert'
        assert mock_urlopen.call_count == 1

        # Second call immediately after should return cached data without hitting urlopen
        alerts2 = regions.fetch_gdacs_live_flood_alerts()
        assert alerts2 == alerts1
        assert mock_urlopen.call_count == 1  # Still 1 call!

        # Fast forward time beyond TTL (301s)
        regions._GDACS_CACHE_TIMESTAMP = time.time() - 301

        # Third call should hit network again after cache expiry
        alerts3 = regions.fetch_gdacs_live_flood_alerts()
        assert alerts3 == alerts1
        assert mock_urlopen.call_count == 2
