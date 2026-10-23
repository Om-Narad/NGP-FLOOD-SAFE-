from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_and_rationale():
    road1 = Road(id="r1", name="Road 1", geometry={}, status="open", connects_zone_ids=["z1"])
    road2 = Road(id="r2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["z1"])
    roads = [road1, road2]

    zone = Zone(
        id="z1",
        name="Zone 1",
        geometry={},
        people_exposed=2500,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter A",
        rationale=""
    )

    connected = [r for r in roads if zone.id in r.connects_zone_ids]

    score = calculate_priority(zone, roads, connected=connected)
    rationale = generate_rationale(zone, roads, connected=connected)

    assert score == 99  # base 84 + 15 penalty = 99
    assert "CRITICAL — Evacuation bottleneck: only 1/2 routes remain open." in rationale

def test_no_connected_roads():
    roads = []
    zone = Zone(
        id="z1",
        name="Zone 1",
        geometry={},
        people_exposed=1000,
        priority_score=0,
        status="pending",
        assigned_squad=None,
        assigned_shelter="Shelter A",
        rationale=""
    )

    score = calculate_priority(zone, roads)
    rationale = generate_rationale(zone, roads)

    assert score == 50
    assert rationale == "No evacuation routes assigned."
