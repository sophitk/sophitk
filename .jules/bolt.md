## 2024-05-22 - Pandas Loop Optimization
**Learning:** Iterating over DataFrame rows with `iloc` is extremely slow compared to iterating over NumPy arrays (~8.4x difference in this codebase).
**Action:** Always prefer converting columns to NumPy arrays before tight loops in backtesting engines.

## 2024-05-22 - `ta` Library Instability
**Learning:** The `ta` library (0.11.0) introduces breaking changes and missing methods (e.g., `volume_rate_of_change`) compared to older versions.
**Action:** Prefer manual vectorized implementations (pandas/numpy) for simple indicators to avoid dependency fragility and improve performance.
