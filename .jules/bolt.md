## 2024-05-23 - Pandas Iteration Optimization
**Learning:** Iterating over a Pandas DataFrame using `range(len(df))` and `.iloc[i]` is extremely slow because it creates a new Series object for each row. Using `df.itertuples()` is significantly faster (observed ~10x improvement in this case) as it yields named tuples.
**Action:** Always prefer `itertuples()` for row-wise iteration when vectorization is not possible. Remember that `itertuples()` yields named tuples, so access changes from dictionary-style `['col']` to attribute-style `.col`.
