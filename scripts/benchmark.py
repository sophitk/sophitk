import time
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtester import CryptoBacktester
from strategy import CryptoTradingStrategy

def benchmark():
    # Create large sample data
    periods = 5000
    dates = pd.date_range('2024-01-01', periods=periods, freq='1h')

    # Generate realistic-looking price data
    np.random.seed(42)
    close = 40000 + np.cumsum(np.random.randn(periods) * 100)
    high = close + np.random.rand(periods) * 50
    low = close - np.random.rand(periods) * 50
    open_ = close + np.random.randn(periods) * 20
    volume = np.random.uniform(1000, 5000, periods)

    df = pd.DataFrame({
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }, index=dates)

    # Run strategy analysis first (we only benchmark backtest loop)
    backtester = CryptoBacktester()
    analysis = backtester.strategy.analyze_market(df)

    print(f"Benchmarking backtest execution with {periods} candles...")

    start_time = time.time()
    results = backtester._execute_backtest(analysis, 'BTC/USDT', '1h')
    end_time = time.time()

    duration = end_time - start_time
    print(f"Execution time: {duration:.4f} seconds")
    print(f"Candles per second: {periods/duration:.2f}")

    return duration

if __name__ == "__main__":
    benchmark()
