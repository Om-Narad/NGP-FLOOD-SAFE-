import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_and_rationale():
    road1 = Road(id="road-1", name="Road 1", geometry={"type": "LineString", "coordinates": []}, status="open", connects_zone_ids=["zone-1"])
    road2 = Road(id="road-2", name="Road 2", geometry={"type": "LineString", "coordinates": []}, status="open", connects_zone_ids=["zone-1"])

    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=2500,
        priority_score=0,
        status="pending",
        assigned_shelter="Shelter A",
        rationale=""
    )

    roads = [road1, road2]
    # Test priority when all roads open
    priority = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)
    assert priority == 84
    assert "Normal evacuation route access" in rationale

    # Test with pre-filtered connected_roads
    conn_roads = [road1, road2]
    priority_fast = calculate_priority(zone, roads, connected_roads=conn_roads)
    rationale_fast = generate_rationale(zone, roads, connected_roads=conn_roads)
    assert priority_fast == priority
    assert rationale_fast == rationale

    # Test when a road is blocked
    road1.status = "blocked"
    priority_blocked = calculate_priority(zone, roads, connected_roads=conn_roads)
    rationale_blocked = generate_rationale(zone, roads, connected_roads=conn_roads)
    assert priority_blocked > priority
    assert "Evacuation bottleneck" in rationale_blocked or "compromised" in rationale_blocked
