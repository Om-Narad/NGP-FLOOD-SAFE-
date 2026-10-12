import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_all_open():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter A",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": [[0, 0], [1, 1]]}),
        Road(id="road-2", name="Road 2", status="open", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": [[1, 1], [2, 2]]})
    ]
    score = calculate_priority(zone, roads)
    assert score == 84
    rationale = generate_rationale(zone, roads)
    assert "Normal evacuation route access" in rationale

def test_calculate_priority_all_blocked():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter A",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="blocked", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": [[0, 0], [1, 1]]}),
        Road(id="road-2", name="Road 2", status="blocked", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": [[1, 1], [2, 2]]})
    ]
    score = calculate_priority(zone, roads)
    assert score == 98
    rationale = generate_rationale(zone, roads)
    assert "CRITICAL ISOLATION" in rationale
