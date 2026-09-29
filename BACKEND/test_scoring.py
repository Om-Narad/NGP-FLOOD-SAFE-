import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_all_open():
    roads = [
        Road(id="road-1", name="R1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="R2", status="open", connects_zone_ids=["zone-1"], geometry={}),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter 1",
        rationale=""
    )

    # Test without pre-filtered connected_roads
    score_default = calculate_priority(zone, roads)
    # Test with pre-filtered connected_roads
    score_opt = calculate_priority(zone, connected_roads=roads)

    assert score_default == score_opt
    assert score_default == 84

def test_calculate_priority_one_blocked():
    roads = [
        Road(id="road-1", name="R1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="R2", status="blocked", connects_zone_ids=["zone-1"], geometry={}),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=1600,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter 1",
        rationale=""
    )

    score_default = calculate_priority(zone, roads)
    score_opt = calculate_priority(zone, connected_roads=roads)

    assert score_default == score_opt
    assert score_default == 62 + 15  # base 62 + 15 blocked penalty = 77

def test_generate_rationale_behavior():
    roads = [
        Road(id="road-1", name="R1", status="blocked", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="R2", status="blocked", connects_zone_ids=["zone-1"], geometry={}),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=1000,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter 1",
        rationale=""
    )

    rationale_default = generate_rationale(zone, roads)
    rationale_opt = generate_rationale(zone, connected_roads=roads)

    assert rationale_default == rationale_opt
    assert "CRITICAL ISOLATION" in rationale_default
