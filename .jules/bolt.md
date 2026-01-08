# Bolt's Journal ⚡

## 2024-05-22 - [Vectorization in Backtesting]
**Learning:** In Python backtesting loops, iterating over pandas DataFrames (rows) is extremely slow. Converting columns to NumPy arrays and iterating over index-based arrays is significantly faster (often 10-100x).
**Action:** When optimizing loop-based backtests, always look for opportunities to convert DataFrame columns to NumPy arrays before the loop.

## 2024-05-23 - [Indicator Calculation Efficiency]
**Learning:** Re-calculating indicators inside a loop or repeatedly is a major bottleneck. Pre-calculating all indicators on the full DataFrame before the backtest loop is essential.
**Action:** Ensure all `ta` library calls or custom indicator calculations happen once on the vectorized data.
