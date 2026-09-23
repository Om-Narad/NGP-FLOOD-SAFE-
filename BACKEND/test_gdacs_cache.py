import pytest
import time
from fastapi.testclient import TestClient
from main import app
from regions import fetch_gdacs_live_flood_alerts, _GDACS_CACHE, _GDACS_CACHE_TTL

client = TestClient(app)

def test_get_regions_endpoint():
    """Verify /api/regions returns all regions quickly with correct structure."""
    response = client.get("/api/regions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 6
    assert data[0]["id"] == "assam"

def test_gdacs_cache_behavior():
    """Verify fetch_gdacs_live_flood_alerts caches data and avoids redundant network calls."""
    # Populate cache manually to test hit
    mock_data = [{"title": "Test Flood", "event_type": "Flood", "country": "TestLand", "coordinates": [0.0, 0.0], "pub_date": "2026-08-07"}]
    _GDACS_CACHE["timestamp"] = time.time()
    _GDACS_CACHE["data"] = mock_data

    # Call function without force_refresh — should hit cache
    res = fetch_gdacs_live_flood_alerts(force_refresh=False)
    assert res == mock_data

def test_gdacs_live_endpoint():
    """Verify /api/gdacs-live endpoint returns cached data structure."""
    response = client.get("/api/gdacs-live")
    assert response.status_code == 200
    json_resp = response.json()
    assert "alerts" in json_resp
    assert "count" in json_resp
    assert json_resp["source"] == "GDACS Global Disaster Alert & Coordination System"
