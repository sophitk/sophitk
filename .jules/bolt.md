## 2024-05-23 - Pandas Iteration Bottleneck
**Learning:** Iterating over a pandas DataFrame using `iloc` or `itertuples` inside a tight loop is extremely slow. Accessing Series attributes (like `bar['close']`) inside the loop adds significant overhead.
**Action:** Convert necessary columns to numpy arrays before the loop and iterate using integer indexing. Refactor helper methods to accept primitive values (float, int) instead of pandas Series or Row objects. This resulted in a ~25x speedup (1.15s -> 0.046s for 10000 bars).

## 2024-05-23 - Library Version Mismatches
**Learning:** The `ta` library version 0.11.0 has missing functions (`volume_rate_of_change`, `relative_vigor_index`, `pivot_points`) compared to what the code expected.
**Action:** Always verify library version capabilities. Implemented manual calculations for missing indicators using vectorized pandas operations, which is also fast.
