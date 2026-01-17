## 2024-05-22 - Replacing `ta` Library Calls with Manual Implementation
**Learning:** The `ta` library functions (v0.11.0) often recalculate rolling windows internally for each indicator call. For grouped indicators like Bollinger Bands or Keltner Channels, this results in significant redundancy.
**Action:** When calculating multiple related indicators (e.g., upper, middle, lower bands), manually calculate the underlying rolling statistics (mean, std, max, min) once using Pandas/NumPy and derive the bands. This yielded a ~6x speedup (0.47s vs 2.92s) for 10k rows.
