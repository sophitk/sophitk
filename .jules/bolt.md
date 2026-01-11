## 2024-05-23 - Pandas Iteration Bottleneck
**Learning:** Iterating through a Pandas DataFrame row by row using `iloc` is extremely slow due to Series object creation overhead.
**Action:** Convert necessary columns to NumPy arrays before the loop and access values by index. This resulted in a ~6.7x speedup (2.65s -> 0.39s) for the backtester.
