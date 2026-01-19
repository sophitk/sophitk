## 2024-05-23 - Pandas Iteration Anti-Pattern
**Learning:** Iterating over Pandas DataFrames using `df.iloc[i]` inside a loop is extremely slow because it creates a new Series object for each row.
**Action:** Always convert necessary columns to NumPy arrays (`df['col'].values`) before the loop and iterate using integer indices. This yields ~10x performance improvement.
