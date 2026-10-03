from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_and_rationale_all_open():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Test Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-1"]),
        Road(id="road-2", name="Road 2", geometry={}, status="open", connects_zone_ids=["zone-1"]),
    ]

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 84
    assert rationale == "Normal evacuation route access (2/2 open). Stable."

def test_calculate_priority_and_rationale_partially_blocked():
    zone = Zone(
        id="zone-2",
        name="Test Zone 2",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=1600,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Test Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-2"]),
        Road(id="road-2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["zone-2"]),
    ]

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 62 + 15  # 77
    assert rationale == "CRITICAL — Evacuation bottleneck: only 1/2 routes remain open."

def test_calculate_priority_and_rationale_all_blocked():
    zone = Zone(
        id="zone-3",
        name="Test Zone 3",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=1100,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Test Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="blocked", connects_zone_ids=["zone-3"]),
        Road(id="road-2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["zone-3"]),
    ]

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 98
    assert rationale == "CRITICAL ISOLATION — 0 of 2 routes remain open. Emergency airlift required."

def test_calculate_priority_no_connected_roads():
    zone = Zone(
        id="zone-4",
        name="Test Zone 4",
        geometry={"type": "Polygon", "coordinates": []},
        people_exposed=700,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Test Shelter",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["other-zone"]),
    ]

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 50
    assert rationale == "No evacuation routes assigned."
