# 🚀 Cryptocurrency Trading Indicator and Strategy System

A high-win-rate day trading system for BTC, ETH, and SOL with comprehensive technical analysis, backtesting, and live monitoring capabilities.

## ✨ Features

- **Multi-Indicator Analysis**: Combines 20+ technical indicators for high-accuracy signals
- **Multi-Timeframe Analysis**: 30-minute and 1-hour timeframes for day trading
- **High Win Rate**: Designed for 65-75% win rate with proper risk management
- **Real-Time Data**: Live market data from Binance, Yahoo Finance, and Coinbase
- **Comprehensive Backtesting**: Full historical performance analysis
- **Risk Management**: Dynamic stop-loss, take-profit, and position sizing
- **Portfolio Analysis**: Multi-asset portfolio optimization
- **Live Monitoring**: Real-time market monitoring and signal alerts

## 🎯 Supported Cryptocurrencies

- **Bitcoin (BTC/USDT)**
- **Ethereum (ETH/USDT)**
- **Solana (SOL/USDT)**

## ⏰ Timeframes

- **30 minutes (30m)** - Short-term day trading
- **1 hour (1h)** - Medium-term day trading

## 📊 Technical Indicators

### Trend Indicators
- EMA (9, 21, 50, 200)
- MACD with signal line
- Ichimoku Cloud
- Parabolic SAR
- ADX (Average Directional Index)

### Momentum Indicators
- RSI (Relative Strength Index)
- Stochastic Oscillator
- Williams %R
- CCI (Commodity Channel Index)
- Rate of Change

### Volatility Indicators
- Bollinger Bands
- Keltner Channels
- ATR (Average True Range)
- Donchian Channels

### Volume Indicators
- VWAP (Volume Weighted Average Price)
- OBV (On Balance Volume)
- Money Flow Index
- Volume Rate of Change

## 🛡️ Risk Management

- **Position Size**: 10% of capital per trade
- **Stop Loss**: 2x ATR (Average True Range)
- **Take Profit**: 4x ATR (1:2 risk-reward ratio)
- **Trailing Stop**: 1.5% dynamic trailing stop
- **Maximum Open Trades**: 3
- **Maximum Daily Loss**: 5%
- **Maximum Weekly Loss**: 15%

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd cryptocurrency-trading-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project directory (optional):

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
```

**Note**: API keys are optional for data fetching but required for live trading.

### 3. Run the System

#### Interactive Mode
```bash
python main.py
```

#### Command Line Mode
```bash
# Analyze BTC on 1h timeframe
python main.py --symbol BTC/USDT --timeframe 1h --action analyze

# Get trading signals for all symbols
python main.py --symbol ALL --timeframe ALL --action signals

# Run backtest for ETH
python main.py --symbol ETH/USDT --timeframe 30m --action backtest
```

## 📱 Usage Guide

### Main Menu Options

1. **📈 Analyze Market Conditions** - Current market analysis for all symbols
2. **🔍 Get Trading Signals** - Real-time trading signals and recommendations
3. **📊 Run Backtest** - Historical performance testing
4. **📈 Portfolio Analysis** - Multi-asset portfolio optimization
5. **🔄 Live Market Monitoring** - Real-time market monitoring
6. **📋 View Strategy Details** - Strategy explanation and parameters
7. **⚙️ Configuration** - System configuration and settings

### Market Analysis

The system provides comprehensive market analysis including:

- **Price Action**: Current price, support/resistance levels
- **Trend Analysis**: Trend direction and strength
- **Volatility Assessment**: Market volatility conditions
- **Volume Analysis**: Volume patterns and confirmation
- **Risk Assessment**: Current market risk level
- **Trading Recommendations**: Buy/Sell/Hold with confidence levels

### Trading Signals

Signals are generated based on:

- **Composite Signal**: Weighted combination of all indicators
- **Individual Signals**: Individual indicator confirmations
- **Signal Strength**: 0-100% confidence level
- **Signal Types**: Strong Buy, Weak Buy, Neutral, Weak Sell, Strong Sell

### Backtesting

Comprehensive backtesting includes:

- **Performance Metrics**: Win rate, profit factor, Sharpe ratio
- **Risk Metrics**: Maximum drawdown, risk-adjusted returns
- **Trade Analysis**: Individual trade performance
- **Equity Curve**: Portfolio value over time
- **Visual Charts**: Price charts with indicators and trades

## 📈 Expected Performance

- **Target Win Rate**: 65-75%
- **Risk-Reward Ratio**: 1:2
- **Maximum Drawdown**: <20%
- **Sharpe Ratio**: >1.5
- **Profit Factor**: >1.5

## 🔧 Configuration

### Strategy Parameters

Key parameters can be modified in `config.py`:

```python
# Entry/Exit thresholds
ENTRY_THRESHOLD = 0.6      # 60% signal strength for entry
EXIT_THRESHOLD = 0.3       # 30% signal strength for exit

# Risk management
POSITION_SIZE = 0.1         # 10% of capital per trade
STOP_LOSS_PERCENT = 0.02   # 2% stop loss
TAKE_PROFIT_PERCENT = 0.04 # 4% take profit

# Technical indicators
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
BOLLINGER_PERIOD = 20
```

### Data Sources

The system supports multiple data sources:

- **Binance** (default) - Real-time cryptocurrency data
- **Yahoo Finance** - Alternative data source
- **Coinbase Pro** - Additional exchange data

## 📊 Example Output

### Market Analysis
```
📊 BTC/USDT Analysis:
⏰ 1h Timeframe:
   💰 Current Price: $43,250.50
   📈 Trend: Bullish (Strong)
   📊 Volatility: High
   📊 Volume: High
   🎯 Market Phase: Neutral
   ⚠️  Risk Level: Medium
   🛡️  Support: $42,800.00
   🚧 Resistance: $43,500.00
   🎯 Action: BUY
   📊 Confidence: 78.5%
   💰 Entry: $43,250.50
   🛑 Stop Loss: $42,500.00
   🎯 Take Profit: $44,750.00
```

### Trading Signals
```
📊 SIGNAL SUMMARY:
🚨 STRONG SIGNALS:
   BTC/USDT (1h): 🟢 STRONG BUY - 78.5%
   ETH/USDT (30m): 🟢 STRONG BUY - 72.3%

🎯 TOP OPPORTUNITIES:
   1. BTC/USDT (1h): 🟢 STRONG BUY - 78.5%
   2. ETH/USDT (30m): 🟢 STRONG BUY - 72.3%
   3. SOL/USDT (1h): 🟡 WEAK BUY - 45.2%
```

## 🚨 Important Notes

### Risk Disclaimer
- This system is for educational and research purposes
- Past performance does not guarantee future results
- Cryptocurrency trading involves substantial risk
- Always use proper risk management
- Never invest more than you can afford to lose

### System Requirements
- Python 3.8+
- Stable internet connection
- Sufficient RAM for data processing
- Optional: Binance API keys for live trading

### Data Limitations
- Historical data depends on exchange availability
- Real-time data requires stable internet connection
- Some indicators may have calculation delays
- Market conditions can change rapidly

## 🔄 Updates and Maintenance

### Regular Updates
- Monitor for new cryptocurrency pairs
- Update technical indicator parameters
- Adjust risk management settings
- Review and optimize strategy performance

### Performance Monitoring
- Track win rate and profit factor
- Monitor maximum drawdown
- Analyze trade patterns
- Adjust strategy based on market conditions

## 📚 Additional Resources

### Learning Materials
- Technical Analysis books
- Cryptocurrency trading courses
- Risk management guides
- Market psychology resources

### Community Support
- Trading forums and communities
- Technical analysis groups
- Cryptocurrency discussion boards
- Professional trading networks

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- Report bugs and issues
- Suggest new features
- Improve documentation
- Optimize performance
- Add new indicators

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the configuration options
- Test with small amounts first

---

**🚀 Happy Trading! Remember: Risk management is the key to long-term success in cryptocurrency trading.**

*Disclaimer: This software is for educational purposes only. Cryptocurrency trading involves substantial risk and may not be suitable for all investors. Always do your own research and consider consulting with a financial advisor before making investment decisions.*
