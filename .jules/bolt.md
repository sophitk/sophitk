## 2026-01-23 - Backtester Loop Optimization
**Learning:** Iterating over Pandas DataFrames with `iloc` inside a loop is extremely slow. Converting columns to NumPy arrays and iterating over a simple integer range yielded a ~10x performance improvement (1.32s -> 0.13s for 10k rows) in `backtester.py`.
**Action:** When implementing sequential logic that requires iteration (like backtesting), always convert DataFrame columns to NumPy arrays first.
