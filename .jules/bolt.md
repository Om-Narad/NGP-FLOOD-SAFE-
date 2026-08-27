# Bolt's Journal - Critical Learnings

## 2026-08-27 - Single-Pass Road Count Optimization in Scoring
**Learning:** In `BACKEND/scoring.py`, calculating priority scores and AI rationales previously filtered `roads` multiple times per zone via separate list comprehensions. Replacing multiple iterations with a single-pass helper (`_get_connected_and_open_counts`) reduces loop iterations by ~50% and eliminates redundant list allocations during frequent road-status recalculation endpoints (`/api/roads/{road_id}/toggle`).
**Action:** When computing multi-metric aggregations over collections, compute counts/states in a single linear pass rather than chaining multiple list comprehensions.
