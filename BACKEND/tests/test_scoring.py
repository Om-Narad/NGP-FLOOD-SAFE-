import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_and_rationale():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter 1",
        rationale=""
    )

    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": []}),
        Road(id="road-2", name="Road 2", status="blocked", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": []})
    ]

    # Without precomputed connected_roads
    score1 = calculate_priority(zone, roads)
    rationale1 = generate_rationale(zone, roads)

    # With precomputed connected_roads
    connected = [r for r in roads if zone.id in r.connects_zone_ids]
    score2 = calculate_priority(zone, roads, connected_roads=connected)
    rationale2 = generate_rationale(zone, roads, connected_roads=connected)

    assert score1 == score2
    assert rationale1 == rationale2
    assert score1 == 84 + 15  # 84 base score for >=2000 pop + 15 penalty for 1 blocked road
    assert "CRITICAL" in rationale1

def test_calculate_priority_all_blocked():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=1000,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter 1",
        rationale=""
    )

    roads = [
        Road(id="road-1", name="Road 1", status="blocked", connects_zone_ids=["zone-1"], geometry={"type": "LineString", "coordinates": []})
    ]

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 98
    assert "CRITICAL ISOLATION" in rationale
