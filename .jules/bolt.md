## 2024-05-22 - [Pandas Loop Optimization]
**Learning:** Iterating over a DataFrame with `iloc` inside a loop (`for i in range(len(df)): row = df.iloc[i]`) creates a new Series object for every iteration, causing massive overhead (O(N) allocations).
**Action:** Extract columns to NumPy arrays (`col = df['col'].values`) before the loop and iterate using integer indices. This reduced backtest time for 10k rows from 1.53s to 0.25s (~6x speedup).
