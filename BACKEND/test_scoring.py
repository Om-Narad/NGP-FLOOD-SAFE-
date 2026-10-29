import pytest
import time
from models import Zone, Road
from scoring import calculate_priority, generate_rationale

def test_calculate_priority_all_open():
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
    road1 = Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-1"])
    road2 = Road(id="road-2", name="Road 2", geometry={}, status="open", connects_zone_ids=["zone-1"])
    roads = [road1, road2]

    score = calculate_priority(zone, roads)
    assert score == 84

    rationale = generate_rationale(zone, roads)
    assert "Normal evacuation route access (2/2 open)" in rationale

def test_calculate_priority_partially_blocked():
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
    road1 = Road(id="road-1", name="Road 1", geometry={}, status="open", connects_zone_ids=["zone-1"])
    road2 = Road(id="road-2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["zone-1"])
    roads = [road1, road2]

    score = calculate_priority(zone, roads)
    assert score == 84 + 15

    rationale = generate_rationale(zone, roads)
    assert "Evacuation bottleneck: only 1/2 routes remain open" in rationale

def test_calculate_priority_completely_blocked():
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
    road1 = Road(id="road-1", name="Road 1", geometry={}, status="blocked", connects_zone_ids=["zone-1"])
    road2 = Road(id="road-2", name="Road 2", geometry={}, status="blocked", connects_zone_ids=["zone-1"])
    roads = [road1, road2]

    score = calculate_priority(zone, roads)
    assert score == 98

    rationale = generate_rationale(zone, roads)
    assert "CRITICAL ISOLATION" in rationale

def test_scoring_performance():
    # Performance benchmark test comparing unoptimized vs optimized path
    zones = [
        Zone(
            id=f"zone-{i}",
            name=f"Test Zone {i}",
            geometry={"type": "Polygon", "coordinates": []},
            people_exposed=1000 + (i * 100),
            priority_score=0,
            status="pending",
            assigned_squad=None,
            assigned_shelter="Shelter 1",
            rationale=""
        ) for i in range(100)
    ]

    roads = [
        Road(
            id=f"road-{j}",
            name=f"Road {j}",
            geometry={},
            status="open" if j % 2 == 0 else "blocked",
            connects_zone_ids=[f"zone-{j % 100}"]
        ) for j in range(200)
    ]

    # Optimized benchmark run
    start_opt = time.perf_counter()
    for _ in range(100):
        for z in zones:
            connected = [r for r in roads if z.id in r.connects_zone_ids]
            p = calculate_priority(z, roads, connected=connected)
            r = generate_rationale(z, roads, connected=connected)
    opt_duration = time.perf_counter() - start_opt

    # Unoptimized benchmark run
    start_unopt = time.perf_counter()
    for _ in range(100):
        for z in zones:
            p = calculate_priority(z, roads)
            r = generate_rationale(z, roads)
    unopt_duration = time.perf_counter() - start_unopt

    print(f"\n[BENCHMARK] Optimized: {opt_duration:.4f}s vs Unoptimized: {unopt_duration:.4f}s")
    assert opt_duration < unopt_duration
