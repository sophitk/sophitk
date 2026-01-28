## 2024-05-23 - DataFrame Iteration Optimization
**Learning:** Iterating over Pandas DataFrame rows using `iloc` in a loop is significantly slower (orders of magnitude) than iterating over NumPy arrays.
**Action:** When implementing loops over time-series data (like backtesting), always extract columns to NumPy arrays first. This yielded a ~21x speedup (1.43s -> 0.067s) for 10,000 rows.
