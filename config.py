import os
from dotenv import load_dotenv

load_dotenv()

# Trading Configuration
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
TIMEFRAMES = ['30m', '1h']

# API Configuration
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', '')

# Trading Parameters
INITIAL_CAPITAL = 10000  # USDT
POSITION_SIZE = 0.1  # 10% of capital per trade
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.04  # 4% take profit

# Technical Indicators Parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2
EMA_FAST = 9
EMA_SLOW = 21
STOCHASTIC_K = 14
STOCHASTIC_D = 3

# Risk Management
MAX_OPEN_TRADES = 3
MAX_DAILY_LOSS = 0.05  # 5% max daily loss
MAX_WEEKLY_LOSS = 0.15  # 15% max weekly loss