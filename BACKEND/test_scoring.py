import pytest
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_all_open():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="Road 2", status="open", connects_zone_ids=["zone-1"], geometry={})
    ]

    # Test without precomputed connected_roads
    score1 = calculate_priority(zone, roads)
    assert score1 == 84

    # Test with precomputed connected_roads
    connected = [r for r in roads if zone.id in r.connects_zone_ids]
    score2 = calculate_priority(zone, roads, connected_roads=connected)
    assert score2 == score1

def test_calculate_priority_blocked_road():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="Road 2", status="blocked", connects_zone_ids=["zone-1"], geometry={})
    ]

    connected = [r for r in roads if zone.id in r.connects_zone_ids]
    score = calculate_priority(zone, roads, connected_roads=connected)
    # base_score 84 + 1 * 15 = 99
    assert score == 99

def test_generate_rationale():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=1000,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="Road 2", status="blocked", connects_zone_ids=["zone-1"], geometry={})
    ]

    connected = [r for r in roads if zone.id in r.connects_zone_ids]
    rationale = generate_rationale(zone, roads, connected_roads=connected)
    assert "CRITICAL — Evacuation bottleneck: only 1/2 routes remain open." in rationale
