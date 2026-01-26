## 2024-05-23 - Backtester Loop Optimization
**Learning:** Converting Pandas DataFrame `iloc` iteration to NumPy array iteration provided an 8.4x speedup (1.85s -> 0.22s) in `backtester.py`. `pd.Series` access inside loops is a major bottleneck.
**Action:** Always extract DataFrame columns to NumPy arrays before iterating if row-by-row processing is required.

## 2024-05-23 - TA-Lib 0.11.0 Breaking Changes
**Learning:** `ta` library v0.11.0 removed `volume_rate_of_change` and `pivot_points`, and changed `donchian_channel` signature.
**Action:** Check library changelogs when upgrading. Implement manual fallbacks for simple indicators if library functions are deprecated.
