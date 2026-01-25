## 2024-05-23 - Backtesting Loop Optimization
**Learning:** Pandas `DataFrame.iloc` and `Series` access inside a tight loop is extremely slow due to overhead. Converting columns to NumPy arrays and iterating with integer indexing improved backtest performance by ~16x (1.47s -> 0.08s for 10k rows).
**Action:** Always extract columns to NumPy arrays before iterating over DataFrame rows in performance-critical loops.
