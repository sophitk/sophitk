## 2024-05-23 - Backtester Loop Optimization
**Learning:** Iterating over Pandas DataFrames with `iloc` inside a loop is extremely slow. Converting columns to NumPy arrays and iterating with integer indices resulted in a ~15x performance improvement (reduced execution time from ~1.4s to ~0.09s for 5000 rows).
**Action:** Always extract DataFrame columns to NumPy arrays before iterating in performance-critical loops. Refactor helper methods to accept scalar values instead of Series.

## 2024-05-23 - Dependency Management in Python 3.12
**Learning:** Python 3.12 requires `numpy>=1.26.0` and `scikit-learn>=1.3.2` to avoid build failures (`setuptools` issues). The `ta` library v0.10.2 is missing several functions assumed by the codebase (`volume_rate_of_change`, `relative_vigor_index`, `pivot_points`), requiring manual implementation or alternatives.
**Action:** Check dependency compatibility carefully when upgrading Python versions. Verify library APIs haven't changed.
