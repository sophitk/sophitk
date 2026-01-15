## 2024-05-23 - Pandas Iteration Anti-Pattern
**Learning:** Iterating over a DataFrame using `for i in range(len(df)): row = df.iloc[i]` creates a new Series object for every row, causing massive overhead. In `backtester.py`, this was the primary bottleneck.
**Action:** Convert necessary columns to NumPy arrays (`df['col'].values`) before the loop and access elements by index (`col_array[i]`). This resulted in a ~16x speedup (2.24s -> 0.14s for 10k rows).
