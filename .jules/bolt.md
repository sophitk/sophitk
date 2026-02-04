## 2024-05-22 - [Broken Dependencies in Optimization]
**Learning:** The `ta` library (v0.10.2) removed several functions (`volume_rate_of_change`, `pivot_points`, `rvi`), causing "standard" calls to fail. Blindly replacing or wrapping libraries can hide these breaks.
**Action:** Always check library changelogs or inspect `dir(module)` when "standard" functions are missing. Implement manual fallbacks for removed simple indicators.
