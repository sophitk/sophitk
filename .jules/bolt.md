## 2024-05-22 - Pandas Iteration Anti-Pattern
**Learning:** Using `df.iloc[i]` inside a tight loop (like backtesting execution) creates a new Series object for every row, leading to massive overhead.
**Action:** Always extract columns to NumPy arrays before iterating by index in performance-critical loops. In this case, it yielded a 12x speedup.
