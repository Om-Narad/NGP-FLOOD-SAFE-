# Bolt's Performance Journal

## 2026-10-06 - Map-based O(1) road resolution in Zone priority calculation
**Learning:** In SentinelPlan's state evaluation pipeline, calculating priorities for $N$ zones against $M$ roads was performing $O(M)$ linear searches per zone ($O(N \cdot M)$ overall) on every state/region update and UI re-render.
**Action:** Always construct an $O(1)$ lookup Map for `roads` when evaluating zone priorities or rendering road associations across multiple list items.
