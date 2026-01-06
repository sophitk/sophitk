## 2024-05-23 - NumPy Iteration vs DataFrame.iloc
**Learning:** Iterating over pandas DataFrames using `.iloc` inside a loop is extremely slow (approx. 2.27s for 10k rows in this case). Converting columns to NumPy arrays and iterating over indices reduced execution time to ~0.09s (25x speedup).
**Action:** When optimizing loop-heavy backtesting logic, always prioritize converting Series/DataFrames to NumPy arrays before the loop. Avoid accessing `df.iloc[i]` or `series[i]` inside hot loops.
