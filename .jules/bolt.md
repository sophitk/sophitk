## 2024-03-20 - Pandas Iteration Anti-Pattern
**Learning:** Using `df.iloc[i]` inside a loop is extremely slow because it creates a new Pandas Series object for each iteration.
**Action:** Convert DataFrame columns to NumPy arrays (e.g., `df['close'].values`) before the loop and access them by index. This resulted in a 10x speedup (1.26s -> 0.13s).
