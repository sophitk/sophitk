## 2024-05-23 - Pandas Iteration Performance
**Learning:** Iterating over Pandas DataFrame rows using `iloc` or `iterrows` is significantly slower than iterating over numpy arrays.
**Action:** When iterating over a DataFrame in a hot loop (like backtesting), convert necessary columns to numpy arrays first using `.to_numpy()` or `.values` and iterate using index. This reduced execution time from ~1.3s to ~0.09s (approx 14x speedup) for 10k rows.
**Learning:** When falling back to default values for missing columns in numpy arrays, use `np.full(len(df), np.nan)` instead of `np.zeros` if `0` is a valid value but not the correct default (e.g. for price or ATR).
