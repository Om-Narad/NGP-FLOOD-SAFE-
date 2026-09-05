from typing import List, Tuple

def _get_road_counts(zone, roads: List) -> Tuple[int, int]:
    """
    Single-pass performance helper to count connected and open roads for a zone.
    Avoids multiple list allocations and intermediate list comprehensions.
    """
    total_count = 0
    open_count = 0
    zone_id = zone.id
    for r in roads:
        if zone_id in r.connects_zone_ids:
            total_count += 1
            if r.status == "open":
                open_count += 1
    return total_count, open_count


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
    # Bolt optimization: Single-pass iteration avoids allocating connected road lists
    total_count, open_count = _get_road_counts(zone, roads)
    if total_count == 0:
        return 50

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


def generate_rationale(zone, roads: List) -> str:
    """
    Generates human-readable AI rationale based on road access ratio.
    """
    # Bolt optimization: Single-pass iteration avoids allocating connected road lists
    total_count, open_count = _get_road_counts(zone, roads)
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
