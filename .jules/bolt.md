## 2024-03-21 - Vectorization in Loops
**Learning:** Python loops over pandas DataFrames (using `.iloc`) are extremely slow. Converting columns to NumPy arrays (`.values`) before the loop provides massive speedups (6x or more).
**Action:** Always extract values to NumPy arrays or basic Python lists before iterating over time-series data.
