"""
SentinelPlan Zone Scoring & AI Rationale Engine
===============================================
Calculates real-time priority scores and human-readable evacuation rationales for flood zones.
Optimized for high-throughput multi-region evaluations.
"""

from typing import List, Optional

def calculate_priority(zone, roads: List, connected_roads: Optional[List] = None) -> int:
    """
    Calculates priority score for a zone based on exposed population
    and the status of connected evacuation roads.

    PERFORMANCE OPTIMIZATION:
    Accepts optional `connected_roads` pre-indexed mapping to bypass O(R) linear searching
    per zone, reducing evaluation complexity from O(Z * R) to O(Z + R). Uses single-pass sum
    generator expressions for fast count calculation.
    """
    connected = connected_roads if connected_roads is not None else [r for r in roads if zone.id in r.connects_zone_ids]
    if not connected:
        return 50

    total_count = len(connected)
    open_count = sum(1 for r in connected if r.status == "open")

    # Base priority mapping or population formula
    if zone.people_exposed >= 2000:
        base_score = 84
    elif zone.people_exposed >= 1500:
        base_score = 62
    elif zone.people_exposed >= 1000:
        base_score = 41
    else:
        base_score = 26

    # Penalty for blocked roads
    blocked_count = total_count - open_count
    blocked_penalty = round(blocked_count * 15)

    if open_count == 0:
        score = 98
    else:
        score = base_score + blocked_penalty

    return min(max(score, 10), 100)


def generate_rationale(zone, roads: List, connected_roads: Optional[List] = None) -> str:
    """
    Generates human-readable AI rationale based on road access ratio.

    PERFORMANCE OPTIMIZATION:
    Accepts optional `connected_roads` pre-indexed mapping to avoid redundant list scans,
    achieving O(1) road lookup per zone call.
    """
    connected = connected_roads if connected_roads is not None else [r for r in roads if zone.id in r.connects_zone_ids]
    if not connected:
        return "No evacuation routes assigned."

    total_count = len(connected)
    open_count = sum(1 for r in connected if r.status == "open")

    if open_count == 0:
        return f"CRITICAL ISOLATION — 0 of {total_count} routes remain open. Emergency airlift required."
    elif open_count == 1 and total_count > 1:
        return f"CRITICAL — Evacuation bottleneck: only {open_count}/{total_count} routes remain open."
    elif open_count < total_count:
        return f"WARNING — {total_count - open_count} route(s) compromised ({open_count}/{total_count} open)."
    else:
        return f"Normal evacuation route access ({open_count}/{total_count} open). Stable."
