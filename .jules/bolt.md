## 2024-05-22 - Backtester Loop Optimization
**Learning:** Iterating over pandas DataFrames using `iloc` in a loop is significantly slower than `itertuples()`. Replacing `iloc` access with `itertuples()` combined with numpy array access for signals reduced backtest execution time by ~9.5x (1.05s to 0.11s for 5000 candles).
**Action:** Always prefer `itertuples()` or vectorization over `iloc` loops for performance-critical code. When using `itertuples()`, ensure helper methods can handle attribute access (e.g., `bar.close`) instead of dictionary access (`bar['close']`).
