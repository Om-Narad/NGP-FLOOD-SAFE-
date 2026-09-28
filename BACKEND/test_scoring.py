from scoring import calculate_priority, generate_rationale
from models import Zone, Road

def test_calculate_priority_all_open():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=2400,
        priority_score=0,
        status="pending",
        assigned_squad="",
        assigned_shelter="",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={}),
        Road(id="road-2", name="Road 2", status="open", connects_zone_ids=["zone-1"], geometry={})
    ]
    score = calculate_priority(zone, roads)
    assert score == 84

def test_generate_rationale():
    zone = Zone(
        id="zone-1",
        name="Test Zone",
        geometry={},
        people_exposed=1000,
        priority_score=0,
        status="pending",
        assigned_squad="",
        assigned_shelter="",
        rationale=""
    )
    roads = [
        Road(id="road-1", name="Road 1", status="open", connects_zone_ids=["zone-1"], geometry={})
    ]
    rationale = generate_rationale(zone, roads)
    assert "Normal evacuation route access" in rationale
