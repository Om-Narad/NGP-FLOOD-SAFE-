import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_all_open():
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-1"]),
        Road(id="road-2", name="Road 2", geometry={}, status="open", connects_zone_ids=["zone-1"]),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        assigned_shelter="Shelter",
        rationale=""
    )
    score = calculate_priority(zone, roads)
    assert score == 84

def test_calculate_priority_with_blocked_roads():
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="blocked", connects_zone_ids=["zone-1"]),
        Road(id="road-2", name="Road 2", geometry={}, status="open", connects_zone_ids=["zone-1"]),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        assigned_shelter="Shelter",
        rationale=""
    )
    score = calculate_priority(zone, roads)
    assert score == 99  # base_score 84 + 15 penalty = 99

def test_calculate_priority_all_blocked():
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="blocked", connects_zone_ids=["zone-1"]),
        Road(id="road-2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["zone-1"]),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        assigned_shelter="Shelter",
        rationale=""
    )
    score = calculate_priority(zone, roads)
    assert score == 98

def test_generate_rationale():
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-1"]),
        Road(id="road-2", name="Road 2", geometry={}, status="open", connects_zone_ids=["zone-1"]),
    ]
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        assigned_shelter="Shelter",
        rationale=""
    )
    rationale = generate_rationale(zone, roads)
    assert "Normal evacuation route access" in rationale
