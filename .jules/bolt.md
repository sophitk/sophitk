## 2024-05-23 - Data Access in Loops
**Learning:** Iterating over Pandas DataFrame rows using `iloc` or `itertuples` is significantly slower than iterating over NumPy arrays.
**Action:** When performing row-by-row operations in a loop (especially for backtesting or simulation), convert necessary DataFrame columns to NumPy arrays (`df['col'].values`) before the loop and access them by index. This can yield 10x-100x speedups.

## 2024-05-23 - ta Library Version Mismatches
**Learning:** The `ta` library version 0.10.2 is missing several functions that might be expected in newer versions or documentation (`volume_rate_of_change`, `relative_vigor_index`, `pivot_points`).
**Action:** Always verify the installed library version and available attributes. If functions are missing, implement fallbacks or manual calculations if feasible, and document the deviation.
