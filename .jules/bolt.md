## 2024-05-23 - Optimizing grouped indicators and handling dependency breakages
**Learning:** `ta` library version updates can break existing code (e.g. `donchian_channel` signature change, removal of `relative_vigor_index`). Grouping rolling statistics (mean, std) for indicators like Bollinger Bands manually is safer and avoids redundant recalculations found in library calls.
**Action:** When optimizing technical indicators, check if multiple indicators share the same rolling window calculations and vectorize them manually.
