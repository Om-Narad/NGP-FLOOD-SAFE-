from typing import List

# ⚡ Bolt Optimization:
# Single-pass counts over connected roads eliminate redundant list allocations
# and multiple list traversals during priority scoring and rationale generation.

def calculate_priority(zone, roads: List) -> int:
    """
    Calculates priority score for a zone based on exposed population
    and the status of connected evacuation roads.
    Target base scores when all roads open:
      - Zone 1 (2400 pop) ~ 84 (Critical, >=75)
      - Zone 2 (1600 pop) ~ 62 (Warning, 50-74)
      - Zone 3 (1100 pop) ~ 41 (Stable, <50)
      - Zone 4 (700 pop)  ~ 26 (Stable)
    """
    # Performance Optimization: Single-pass iteration to count total and open connected roads
    total_count = 0
    open_count = 0
    zone_id = zone.id

    for r in roads:
        if zone_id in r.connects_zone_ids:
            total_count += 1
            if r.status == "open":
                open_count += 1

    if total_count == 0:
        return 50

    # Base priority mapping based on population
    people = zone.people_exposed
    if people >= 2000:
        base_score = 84
    elif people >= 1500:
        base_score = 62
    elif people >= 1000:
        base_score = 41
    else:
        base_score = 26

    # Penalty for blocked roads
    blocked_count = total_count - open_count
    blocked_penalty = blocked_count * 15

    if open_count == 0:
        score = 98
    else:
        score = base_score + blocked_penalty

    return min(max(score, 10), 100)


def generate_rationale(zone, roads: List) -> str:
    """
    Generates human-readable AI rationale based on road access ratio.
    """
    # Performance Optimization: Single-pass iteration to count total and open connected roads
    total_count = 0
    open_count = 0
    zone_id = zone.id

    for r in roads:
        if zone_id in r.connects_zone_ids:
            total_count += 1
            if r.status == "open":
                open_count += 1

    if total_count == 0:
        return "No evacuation routes assigned."

    if open_count == 0:
        return f"CRITICAL ISOLATION — 0 of {total_count} routes remain open. Emergency airlift required."
    elif open_count == 1 and total_count > 1:
        return f"CRITICAL — Evacuation bottleneck: only {open_count}/{total_count} routes remain open."
    elif open_count < total_count:
        return f"WARNING — {total_count - open_count} route(s) compromised ({open_count}/{total_count} open)."
    else:
        return f"Normal evacuation route access ({open_count}/{total_count} open). Stable."
