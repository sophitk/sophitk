#!/usr/bin/env python3
"""
Cryptocurrency Trading Indicator and Strategy System
High-win-rate day trading system for BTC, ETH, and SOL
Timeframes: 30m and 1H
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
import pandas as pd

from config import SYMBOLS, TIMEFRAMES
from data_fetcher import CryptoDataFetcher
from strategy import CryptoTradingStrategy
from backtester import CryptoBacktester

def print_banner():
    """Print application banner"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🚀 CRYPTOCURRENCY TRADING SYSTEM 🚀                     ║
║                                                                              ║
║  High-Win-Rate Day Trading Strategy for BTC, ETH, and SOL                  ║
║  Timeframes: 30m and 1H                                                    ║
║  Features: Multi-indicator analysis, backtesting, and live signals         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

def print_menu():
    """Print main menu options"""
    print("\n📊 MAIN MENU:")
    print("1. 📈 Analyze current market conditions")
    print("2. 🔍 Get trading signals")
    print("3. 📊 Run backtest")
    print("4. 📈 Portfolio analysis")
    print("5. 🔄 Live market monitoring")
    print("6. 📋 View strategy details")
    print("7. ⚙️  Configuration")
    print("0. 🚪 Exit")
    print("-" * 60)

def analyze_market():
    """Analyze current market conditions for all symbols"""
    print("\n🔍 ANALYZING MARKET CONDITIONS...")
    print("=" * 60)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    for symbol in SYMBOLS:
        print(f"\n📊 {symbol} Analysis:")
        print("-" * 40)
        
        for timeframe in TIMEFRAMES:
            print(f"\n⏰ {timeframe} Timeframe:")
            
            # Fetch data
            df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=200)
            
            if df.empty:
                print(f"   ❌ No data available for {timeframe}")
                continue
            
            # Clean data
            df = data_fetcher.clean_data(df)
            
            if len(df) < 50:
                print(f"   ❌ Insufficient data for {timeframe}: {len(df)} candles")
                continue
            
            # Analyze market
            analysis = strategy.analyze_market(df)
            market_conditions = analysis['market_conditions']
            
            # Display analysis
            print(f"   💰 Current Price: ${market_conditions['current_price']:.2f}")
            print(f"   📈 Trend: {market_conditions['trend_direction']} ({market_conditions['trend_strength']})")
            print(f"   📊 Volatility: {market_conditions['volatility']}")
            print(f"   📊 Volume: {market_conditions['volume_condition']}")
            print(f"   🎯 Market Phase: {market_conditions['market_phase']}")
            print(f"   ⚠️  Risk Level: {market_conditions['risk_level']}")
            print(f"   🛡️  Support: ${market_conditions['support_level']:.2f}")
            print(f"   🚧 Resistance: ${market_conditions['resistance_level']:.2f}")
            
            # Get trading recommendation
            recommendation = strategy.get_trading_recommendation(analysis)
            print(f"   🎯 Action: {recommendation['action']}")
            if recommendation['action'] != 'HOLD':
                print(f"   📊 Confidence: {recommendation['confidence']:.2%}")
                print(f"   💡 Reason: {recommendation['reason']}")
                if recommendation['entry_price']:
                    print(f"   💰 Entry: ${recommendation['entry_price']:.2f}")
                    print(f"   🛑 Stop Loss: ${recommendation['stop_loss']:.2f}")
                    print(f"   🎯 Take Profit: ${recommendation['take_profit']:.2f}")
                    print(f"   ⚖️  Risk/Reward: {recommendation['risk_reward_ratio']:.2f}")

def get_trading_signals():
    """Get current trading signals for all symbols"""
    print("\n🔍 GETTING TRADING SIGNALS...")
    print("=" * 60)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    all_signals = []
    
    for symbol in SYMBOLS:
        print(f"\n📊 {symbol} Signals:")
        print("-" * 40)
        
        for timeframe in TIMEFRAMES:
            print(f"\n⏰ {timeframe} Timeframe:")
            
            # Fetch data
            df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=200)
            
            if df.empty:
                print(f"   ❌ No data available")
                continue
            
            # Clean data
            df = data_fetcher.clean_data(df)
            
            if len(df) < 50:
                print(f"   ❌ Insufficient data")
                continue
            
            # Analyze market
            analysis = strategy.analyze_market(df)
            signals = analysis['signals']
            composite_signal = analysis['composite_signal']
            
            # Display signals
            latest_signal = composite_signal.iloc[-1] if not composite_signal.empty else 0
            signal_strength = abs(latest_signal)
            
            if latest_signal > 0.3:
                signal_type = "🟢 STRONG BUY"
            elif latest_signal > 0.1:
                signal_type = "🟡 WEAK BUY"
            elif latest_signal < -0.3:
                signal_type = "🔴 STRONG SELL"
            elif latest_signal < -0.1:
                signal_type = "🟠 WEAK SELL"
            else:
                signal_type = "⚪ NEUTRAL"
            
            print(f"   📊 Signal: {signal_type}")
            print(f"   📈 Strength: {signal_strength:.2%}")
            
            # Individual indicator signals
            print("   🔍 Individual Signals:")
            for indicator, signal_series in signals.items():
                if not signal_series.empty:
                    latest_indicator_signal = signal_series.iloc[-1]
                    if latest_indicator_signal != 0:
                        signal_icon = "🟢" if latest_indicator_signal > 0 else "🔴"
                        signal_name = indicator.replace('_', ' ').title()
                        print(f"      {signal_icon} {signal_name}: {latest_indicator_signal}")
            
            # Store signal for summary
            all_signals.append({
                'symbol': symbol,
                'timeframe': timeframe,
                'signal': latest_signal,
                'strength': signal_strength,
                'type': signal_type
            })
    
    # Display signal summary
    print("\n📊 SIGNAL SUMMARY:")
    print("=" * 60)
    
    strong_signals = [s for s in all_signals if s['strength'] > 0.3]
    if strong_signals:
        print("\n🚨 STRONG SIGNALS:")
        for signal in strong_signals:
            print(f"   {signal['symbol']} ({signal['timeframe']}): {signal['type']} - {signal['strength']:.2%}")
    else:
        print("\n✅ No strong signals detected")
    
    # Best opportunities
    if all_signals:
        best_signals = sorted(all_signals, key=lambda x: x['strength'], reverse=True)[:3]
        print("\n🎯 TOP OPPORTUNITIES:")
        for i, signal in enumerate(best_signals, 1):
            print(f"   {i}. {signal['symbol']} ({signal['timeframe']}): {signal['type']} - {signal['strength']:.2%}")

def run_backtest():
    """Run backtest for selected symbols and timeframes"""
    print("\n📊 RUNNING BACKTEST...")
    print("=" * 60)
    
    # Get user input
    print("Available symbols:", ", ".join(SYMBOLS))
    print("Available timeframes:", ", ".join(TIMEFRAMES))
    
    try:
        symbol = input("\nEnter symbol to test (or 'all' for all symbols): ").strip().upper()
        if symbol == 'ALL':
            symbols_to_test = SYMBOLS
        elif symbol in SYMBOLS:
            symbols_to_test = [symbol]
        else:
            print(f"❌ Invalid symbol: {symbol}")
            return
        
        timeframe_input = input("Enter timeframe to test (or 'all' for all timeframes): ").strip().lower()
        if timeframe_input == 'all':
            timeframes_to_test = TIMEFRAMES
        elif timeframe_input in TIMEFRAMES:
            timeframes_to_test = [timeframe_input]
        else:
            print(f"❌ Invalid timeframe: {timeframe_input}")
            return
        
        # Run backtest
        backtester = CryptoBacktester(initial_capital=10000)
        
        if len(symbols_to_test) == 1 and len(timeframes_to_test) == 1:
            # Single symbol, single timeframe
            result = backtester.run_backtest(symbols_to_test[0], timeframes_to_test[0])
            if result:
                print("\n📊 BACKTEST RESULTS:")
                print("=" * 60)
                print(backtester.generate_report(result))
                
                # Ask if user wants to plot results
                plot_choice = input("\nWould you like to plot the results? (y/n): ").strip().lower()
                if plot_choice in ['y', 'yes']:
                    backtester.plot_results(result)
        else:
            # Multiple symbols or timeframes
            if len(symbols_to_test) > 1:
                result = backtester.run_portfolio_backtest(symbols_to_test, timeframes_to_test)
            else:
                result = backtester.run_multi_timeframe_backtest(symbols_to_test[0], timeframes_to_test)
            
            if result:
                print("\n📊 PORTFOLIO BACKTEST RESULTS:")
                print("=" * 60)
                
                if 'portfolio_performance' in result:
                    perf = result['portfolio_performance']
                    print(f"Total Trades: {perf.get('total_trades', 0)}")
                    print(f"Win Rate: {perf.get('win_rate', 0):.2f}%")
                    print(f"Total Return: {perf.get('total_return', 0):.2f}%")
                    print(f"Total P&L: ${perf.get('total_pnl', 0):.2f}")
                
                # Display individual results
                for symbol, symbol_results in result.get('results', {}).items():
                    print(f"\n📊 {symbol}:")
                    for timeframe, timeframe_results in symbol_results.items():
                        if 'performance' in timeframe_results:
                            perf = timeframe_results['performance']
                            print(f"  {timeframe}: {perf.get('win_rate', 0):.2f}% win rate, "
                                  f"{perf.get('total_return', 0):.2f}% return")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Backtest interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during backtest: {e}")

def portfolio_analysis():
    """Run comprehensive portfolio analysis"""
    print("\n📊 PORTFOLIO ANALYSIS...")
    print("=" * 60)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    portfolio_summary = []
    
    for symbol in SYMBOLS:
        print(f"\n📊 {symbol} Portfolio Analysis:")
        print("-" * 40)
        
        symbol_summary = {'symbol': symbol, 'timeframes': {}}
        
        for timeframe in TIMEFRAMES:
            print(f"\n⏰ {timeframe} Timeframe:")
            
            # Fetch data
            df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=200)
            
            if df.empty:
                print(f"   ❌ No data available")
                continue
            
            # Clean data
            df = data_fetcher.clean_data(df)
            
            if len(df) < 50:
                print(f"   ❌ Insufficient data")
                continue
            
            # Analyze market
            analysis = strategy.analyze_market(df)
            market_conditions = analysis['market_conditions']
            
            # Calculate risk score
            risk_score = 0
            if market_conditions['risk_level'] == 'High':
                risk_score = 3
            elif market_conditions['risk_level'] == 'Medium':
                risk_score = 2
            else:
                risk_score = 1
            
            # Calculate opportunity score
            opportunity_score = 0
            if market_conditions['trend_strength'] == 'Strong':
                opportunity_score += 2
            if market_conditions['volatility'] == 'High':
                opportunity_score += 1
            if market_conditions['volume_condition'] == 'High':
                opportunity_score += 1
            
            # Overall score
            overall_score = opportunity_score - risk_score
            
            print(f"   📊 Risk Score: {risk_score}/3")
            print(f"   🎯 Opportunity Score: {opportunity_score}/4")
            print(f"   ⭐ Overall Score: {overall_score}/4")
            
            # Store summary
            symbol_summary['timeframes'][timeframe] = {
                'risk_score': risk_score,
                'opportunity_score': opportunity_score,
                'overall_score': overall_score,
                'market_conditions': market_conditions
            }
        
        portfolio_summary.append(symbol_summary)
    
    # Display portfolio recommendations
    print("\n🎯 PORTFOLIO RECOMMENDATIONS:")
    print("=" * 60)
    
    # Sort by overall score
    for symbol_summary in portfolio_summary:
        symbol = symbol_summary['symbol']
        best_timeframe = None
        best_score = -10
        
        for timeframe, data in symbol_summary['timeframes'].items():
            if data['overall_score'] > best_score:
                best_score = data['overall_score']
                best_timeframe = timeframe
        
        if best_timeframe and best_score > 0:
            print(f"✅ {symbol} ({best_timeframe}): Strong opportunity (Score: {best_score})")
        elif best_timeframe and best_score == 0:
            print(f"⚠️  {symbol} ({best_timeframe}): Moderate opportunity (Score: {best_score})")
        else:
            print(f"❌ {symbol}: No good opportunities detected")

def live_monitoring():
    """Live market monitoring"""
    print("\n🔄 LIVE MARKET MONITORING...")
    print("=" * 60)
    print("Press Ctrl+C to stop monitoring")
    print("-" * 60)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🕐 {current_time}")
            print("=" * 40)
            
            for symbol in SYMBOLS:
                print(f"\n📊 {symbol}:")
                
                # Get real-time data
                df = data_fetcher.get_realtime_data(symbol)
                
                if df.empty:
                    print(f"   ❌ No real-time data")
                    continue
                
                # Get market info
                market_info = data_fetcher.get_market_info(symbol)
                
                if market_info:
                    print(f"   💰 Price: ${market_info.get('last_price', 0):.2f}")
                    print(f"   📈 24h Change: {market_info.get('change_24h', 0):.2f}%")
                    print(f"   📊 24h Volume: {market_info.get('volume_24h', 0):.0f}")
                    print(f"   💸 Spread: ${market_info.get('spread', 0):.4f}")
                
                # Analyze for signals
                for timeframe in TIMEFRAMES:
                    df_tf = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
                    
                    if not df_tf.empty:
                        df_tf = data_fetcher.clean_data(df_tf)
                        
                        if len(df_tf) >= 50:
                            analysis = strategy.analyze_market(df_tf)
                            recommendation = strategy.get_trading_recommendation(analysis)
                            
                            if recommendation['action'] != 'HOLD':
                                print(f"   🎯 {timeframe}: {recommendation['action']} - "
                                      f"Confidence: {recommendation['confidence']:.2%}")
            
            # Wait before next update
            import time
            time.sleep(60)  # Update every minute
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Live monitoring stopped by user")

def view_strategy_details():
    """Display strategy details and configuration"""
    print("\n📋 STRATEGY DETAILS:")
    print("=" * 60)
    
    print("\n🎯 TRADING STRATEGY OVERVIEW:")
    print("   • Multi-timeframe analysis (30m and 1H)")
    print("   • Multi-indicator confirmation system")
    print("   • Risk management with dynamic stop-loss")
    print("   • Volume and trend confirmation")
    print("   • Support/resistance level analysis")
    
    print("\n📊 TECHNICAL INDICATORS:")
    print("   • Trend Indicators:")
    print("     - EMA (9, 21, 50, 200)")
    print("     - MACD with signal line")
    print("     - Ichimoku Cloud")
    print("     - Parabolic SAR")
    print("     - ADX (Average Directional Index)")
    
    print("   • Momentum Indicators:")
    print("     - RSI (Relative Strength Index)")
    print("     - Stochastic Oscillator")
    print("     - Williams %R")
    print("     - CCI (Commodity Channel Index)")
    print("     - Rate of Change")
    
    print("   • Volatility Indicators:")
    print("     - Bollinger Bands")
    print("     - Keltner Channels")
    print("     - ATR (Average True Range)")
    print("     - Donchian Channels")
    
    print("   • Volume Indicators:")
    print("     - VWAP (Volume Weighted Average Price)")
    print("     - OBV (On Balance Volume)")
    print("     - Money Flow Index")
    print("     - Volume Rate of Change")
    
    print("\n⚙️  STRATEGY PARAMETERS:")
    print("   • Entry Threshold: 0.6 (60% signal strength)")
    print("   • Exit Threshold: 0.3 (30% signal strength)")
    print("   • Position Size: 10% of capital per trade")
    print("   • Stop Loss: 2x ATR")
    print("   • Take Profit: 4x ATR (1:2 risk-reward)")
    print("   • Trailing Stop: 1.5%")
    
    print("\n🛡️  RISK MANAGEMENT:")
    print("   • Maximum Open Trades: 3")
    print("   • Maximum Daily Loss: 5%")
    print("   • Maximum Weekly Loss: 15%")
    print("   • Trend confirmation required")
    print("   • Volume confirmation required")
    
    print("\n📈 EXPECTED PERFORMANCE:")
    print("   • Target Win Rate: 65-75%")
    print("   • Risk-Reward Ratio: 1:2")
    print("   • Maximum Drawdown: <20%")
    print("   • Sharpe Ratio: >1.5")

def configuration():
    """Configuration menu"""
    print("\n⚙️  CONFIGURATION:")
    print("=" * 60)
    
    print("1. 📊 View current configuration")
    print("2. 🔑 Set API keys")
    print("3. ⚙️  Modify strategy parameters")
    print("4. 📈 Adjust risk management")
    print("0. 🔙 Back to main menu")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == '1':
        print("\n📊 CURRENT CONFIGURATION:")
        print("-" * 40)
        print(f"Symbols: {', '.join(SYMBOLS)}")
        print(f"Timeframes: {', '.join(TIMEFRAMES)}")
        print(f"Initial Capital: ${config.INITIAL_CAPITAL:,.2f}")
        print(f"Position Size: {config.POSITION_SIZE * 100}%")
        print(f"Stop Loss: {config.STOP_LOSS_PERCENT * 100}%")
        print(f"Take Profit: {config.TAKE_PROFIT_PERCENT * 100}%")
        print(f"Max Open Trades: {config.MAX_OPEN_TRADES}")
        print(f"Max Daily Loss: {config.MAX_DAILY_LOSS * 100}%")
        print(f"Max Weekly Loss: {config.MAX_WEEKLY_LOSS * 100}%")
        
        if config.BINANCE_API_KEY:
            print("API Keys: ✅ Configured")
        else:
            print("API Keys: ❌ Not configured")
    
    elif choice == '2':
        print("\n🔑 API KEY CONFIGURATION:")
        print("-" * 40)
        print("To set API keys, create a .env file in the project directory with:")
        print("BINANCE_API_KEY=your_api_key_here")
        print("BINANCE_SECRET_KEY=your_secret_key_here")
        print("\n⚠️  Note: API keys are optional for data fetching but required for live trading")
    
    elif choice == '3':
        print("\n⚙️  STRATEGY PARAMETERS:")
        print("-" * 40)
        print("Strategy parameters can be modified in config.py")
        print("Current key parameters:")
        print(f"• RSI Period: {config.RSI_PERIOD}")
        print(f"• MACD Fast: {config.MACD_FAST}")
        print(f"• MACD Slow: {config.MACD_SLOW}")
        print(f"• Bollinger Period: {config.BOLLINGER_PERIOD}")
        print(f"• EMA Fast: {config.EMA_FAST}")
        print(f"• EMA Slow: {config.EMA_SLOW}")
    
    elif choice == '4':
        print("\n📈 RISK MANAGEMENT:")
        print("-" * 40)
        print("Risk management parameters can be modified in config.py")
        print("Current settings:")
        print(f"• Position Size: {config.POSITION_SIZE * 100}% of capital")
        print(f"• Stop Loss: {config.STOP_LOSS_PERCENT * 100}%")
        print(f"• Take Profit: {config.TAKE_PROFIT_PERCENT * 100}%")
        print(f"• Max Daily Loss: {config.MAX_DAILY_LOSS * 100}%")
        print(f"• Max Weekly Loss: {config.MAX_WEEKLY_LOSS * 100}%")

def main():
    """Main application loop"""
    print_banner()
    
    while True:
        try:
            print_menu()
            choice = input("Enter your choice (0-7): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using the Cryptocurrency Trading System!")
                print("Good luck with your trading! 🚀")
                break
            
            elif choice == '1':
                analyze_market()
            
            elif choice == '2':
                get_trading_signals()
            
            elif choice == '3':
                run_backtest()
            
            elif choice == '4':
                portfolio_analysis()
            
            elif choice == '5':
                live_monitoring()
            
            elif choice == '6':
                view_strategy_details()
            
            elif choice == '7':
                configuration()
            
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 7.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Cryptocurrency Trading System')
        parser.add_argument('--symbol', choices=SYMBOLS + ['ALL'], default='BTC/USDT',
                          help='Symbol to analyze (default: BTC/USDT)')
        parser.add_argument('--timeframe', choices=TIMEFRAMES + ['ALL'], default='1h',
                          help='Timeframe to analyze (default: 1h)')
        parser.add_argument('--action', choices=['analyze', 'signals', 'backtest'],
                          default='analyze', help='Action to perform (default: analyze)')
        parser.add_argument('--source', choices=['binance', 'yahoo', 'coinbase'],
                          default='binance', help='Data source (default: binance)')
        
        args = parser.parse_args()
        
        # Run command line mode
        print_banner()
        
        if args.action == 'analyze':
            print(f"\n🔍 Analyzing {args.symbol} on {args.timeframe} timeframe...")
            data_fetcher = CryptoDataFetcher()
            strategy = CryptoTradingStrategy()
            
            if args.symbol == 'ALL':
                symbols_to_analyze = SYMBOLS
            else:
                symbols_to_analyze = [args.symbol]
            
            if args.timeframe == 'ALL':
                timeframes_to_analyze = TIMEFRAMES
            else:
                timeframes_to_analyze = [args.timeframe]
            
            for symbol in symbols_to_analyze:
                for timeframe in timeframes_to_analyze:
                    print(f"\n📊 {symbol} - {timeframe}:")
                    df = data_fetcher.get_data(symbol, timeframe, args.source)
                    if not df.empty:
                        analysis = strategy.analyze_market(df)
                        recommendation = strategy.get_trading_recommendation(analysis)
                        print(f"   Action: {recommendation['action']}")
                        print(f"   Confidence: {recommendation['confidence']:.2%}")
                        if recommendation['reason']:
                            print(f"   Reason: {recommendation['reason']}")
        
        elif args.action == 'signals':
            print(f"\n🔍 Getting signals for {args.symbol} on {args.timeframe} timeframe...")
            get_trading_signals()
        
        elif args.action == 'backtest':
            print(f"\n📊 Running backtest for {args.symbol} on {args.timeframe} timeframe...")
            backtester = CryptoBacktester()
            if args.symbol == 'ALL':
                result = backtester.run_portfolio_backtest(SYMBOLS, [args.timeframe] if args.timeframe != 'ALL' else TIMEFRAMES)
            else:
                result = backtester.run_backtest(args.symbol, args.timeframe)
            
            if result:
                print(backtester.generate_report(result))
    
    else:
        # Run interactive mode
        main()