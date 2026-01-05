## 2024-01-05 - DataFrame Iteration vs Numpy Arrays
**Learning:** Iterating over pandas DataFrames using `iloc` or `itertuples` in a loop is significantly slower than converting columns to NumPy arrays and iterating over them, especially for simple arithmetic or logic checks.
**Action:** When optimizing tight loops in backtesting or data processing, convert pandas Series/DataFrames to NumPy arrays (`.to_numpy()`) before the loop.
