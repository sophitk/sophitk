## 2024-05-22 - [Optimizing Redundant Rolling Calculations]
**Learning:** Pandas rolling window calculations (like `.rolling().max()`) are computationally expensive. When the same rolling calculation is needed multiple times (e.g., for different Fibonacci levels), calculating it once and storing the result yields significant performance gains.
**Action:** Always check for redundant rolling calculations when optimizing pandas-based data processing pipelines. Store intermediate results in variables.
