## 2024-05-22 - Backtesting Loop Performance
**Learning:** Iterating Pandas DataFrames row-by-row (`iloc`) in `backtester.py` was a massive bottleneck (2.5s for 10k rows). Converting to NumPy arrays reduced execution time to ~0.012s (200x speedup).
**Action:** Always extract primitive arrays (`to_numpy()`) before iterating over time-series data in this codebase. Handle `np.datetime64` vs `pd.Timestamp` carefully in helper functions.

## 2024-05-22 - Dependency Fragility
**Learning:** Python 3.12 requires `numpy>=1.26.0` to avoid build failures, but `requirements.txt` pinned `1.24.3`. Also `ta` library had deprecated function calls causing runtime crashes.
**Action:** Verify environment compatibility early and check for library deprecations (especially `ta` and `pandas`) before optimizing logic.
