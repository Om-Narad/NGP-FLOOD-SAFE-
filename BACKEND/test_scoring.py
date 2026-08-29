import pytest
from pydantic import BaseModel
from typing import List
from scoring import calculate_priority, generate_rationale

class MockRoad(BaseModel):
    id: str
    status: str
    connects_zone_ids: List[str]

class MockZone(BaseModel):
    id: str
    people_exposed: int

def test_no_connected_roads():
    zone = MockZone(id="zone-1", people_exposed=2500)
    roads = [MockRoad(id="road-1", status="open", connects_zone_ids=["zone-2"])]
    assert calculate_priority(zone, roads) == 50
    assert generate_rationale(zone, roads) == "No evacuation routes assigned."

def test_all_roads_open():
    zone = MockZone(id="zone-1", people_exposed=2400)
    roads = [
        MockRoad(id="road-1", status="open", connects_zone_ids=["zone-1"]),
        MockRoad(id="road-2", status="open", connects_zone_ids=["zone-1"])
    ]
    assert calculate_priority(zone, roads) == 84
    assert generate_rationale(zone, roads) == "Normal evacuation route access (2/2 open). Stable."

def test_partially_blocked_roads():
    zone = MockZone(id="zone-1", people_exposed=1600)
    roads = [
        MockRoad(id="road-1", status="open", connects_zone_ids=["zone-1"]),
        MockRoad(id="road-2", status="blocked", connects_zone_ids=["zone-1"]),
        MockRoad(id="road-3", status="open", connects_zone_ids=["zone-1"])
    ]
    # base_score 62 + blocked_penalty 15 = 77
    assert calculate_priority(zone, roads) == 77
    assert "WARNING — 1 route(s) compromised" in generate_rationale(zone, roads)

def test_bottleneck_one_open_road():
    zone = MockZone(id="zone-1", people_exposed=1100)
    roads = [
        MockRoad(id="road-1", status="open", connects_zone_ids=["zone-1"]),
        MockRoad(id="road-2", status="blocked", connects_zone_ids=["zone-1"])
    ]
    # base_score 41 + blocked_penalty 15 = 56
    assert calculate_priority(zone, roads) == 56
    assert "CRITICAL — Evacuation bottleneck: only 1/2 routes remain open." in generate_rationale(zone, roads)

def test_all_roads_blocked():
    zone = MockZone(id="zone-1", people_exposed=700)
    roads = [
        MockRoad(id="road-1", status="blocked", connects_zone_ids=["zone-1"]),
        MockRoad(id="road-2", status="blocked", connects_zone_ids=["zone-1"])
    ]
    assert calculate_priority(zone, roads) == 98
    assert "CRITICAL ISOLATION — 0 of 2 routes remain open." in generate_rationale(zone, roads)
