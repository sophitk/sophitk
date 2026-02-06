## 2026-02-06 - Loop Vectorization in Backtester
**Learning:** Iterating over pandas DataFrame with `.iloc` inside a loop is extremely slow (O(N) * overhead). Converting columns to NumPy arrays before iteration reduces execution time by ~128x (from 2.4s to 0.019s for 10k rows).
**Action:** Always extract DataFrame columns to NumPy arrays before iterating in performance-critical loops. Use `df['col'].to_numpy()` and index via integer `i`.
