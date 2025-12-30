## 2024-05-23 - Loop Optimization in Pandas
**Learning:** Replacing `df.iloc[i]` inside a loop with `itertuples()` and converting Series to numpy arrays (`.values`) for indexed access resulted in a ~20x speedup.
**Action:** Always check for `iloc` or `loc` inside loops iterating over DataFrames. Prefer `itertuples()` or vectorization.
