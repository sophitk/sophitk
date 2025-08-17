#!/usr/bin/env python3
"""
Example script demonstrating the Cryptocurrency Trading System
This script shows how to use the system programmatically
"""

from data_fetcher import CryptoDataFetcher
from strategy import CryptoTradingStrategy
from backtester import CryptoBacktester
import config

def example_market_analysis():
    """Example of market analysis"""
    print("🔍 EXAMPLE: Market Analysis")
    print("=" * 50)
    
    # Initialize components
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    # Analyze BTC on 1h timeframe
    symbol = "BTC/USDT"
    timeframe = "1h"
    
    print(f"Analyzing {symbol} on {timeframe} timeframe...")
    
    # Fetch data
    df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=200)
    
    if df.empty:
        print("❌ No data available")
        return
    
    # Clean data
    df = data_fetcher.clean_data(df)
    
    if len(df) < 50:
        print(f"❌ Insufficient data: {len(df)} candles")
        return
    
    # Analyze market
    analysis = strategy.analyze_market(df)
    market_conditions = analysis['market_conditions']
    
    # Display results
    print(f"\n📊 Market Analysis Results:")
    print(f"   Current Price: ${market_conditions['current_price']:.2f}")
    print(f"   Trend: {market_conditions['trend_direction']} ({market_conditions['trend_strength']})")
    print(f"   Volatility: {market_conditions['volatility']}")
    print(f"   Risk Level: {market_conditions['risk_level']}")
    print(f"   Support: ${market_conditions['support_level']:.2f}")
    print(f"   Resistance: ${market_conditions['resistance_level']:.2f}")
    
    # Get trading recommendation
    recommendation = strategy.get_trading_recommendation(analysis)
    print(f"\n🎯 Trading Recommendation:")
    print(f"   Action: {recommendation['action']}")
    print(f"   Confidence: {recommendation['confidence']:.2%}")
    print(f"   Reason: {recommendation['reason']}")
    
    if recommendation['entry_price']:
        print(f"   Entry Price: ${recommendation['entry_price']:.2f}")
        print(f"   Stop Loss: ${recommendation['stop_loss']:.2f}")
        print(f"   Take Profit: ${recommendation['take_profit']:.2f}")
        print(f"   Risk/Reward: {recommendation['risk_reward_ratio']:.2f}")

def example_trading_signals():
    """Example of getting trading signals"""
    print("\n🔍 EXAMPLE: Trading Signals")
    print("=" * 50)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    # Get signals for all symbols and timeframes
    for symbol in config.SYMBOLS:
        print(f"\n📊 {symbol}:")
        
        for timeframe in config.TIMEFRAMES:
            print(f"  ⏰ {timeframe}:")
            
            # Fetch data
            df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
            
            if df.empty:
                print("    ❌ No data")
                continue
            
            df = data_fetcher.clean_data(df)
            
            if len(df) < 50:
                print(f"    ❌ Insufficient data ({len(df)} candles)")
                continue
            
            # Analyze and get signals
            analysis = strategy.analyze_market(df)
            composite_signal = analysis['composite_signal']
            
            if not composite_signal.empty:
                latest_signal = composite_signal.iloc[-1]
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
                
                print(f"    {signal_type} - Strength: {signal_strength:.2%}")

def example_backtest():
    """Example of running a backtest"""
    print("\n📊 EXAMPLE: Backtest")
    print("=" * 50)
    
    # Initialize backtester
    backtester = CryptoBacktester(initial_capital=10000)
    
    # Run backtest for BTC on 1h timeframe
    symbol = "BTC/USDT"
    timeframe = "1h"
    
    print(f"Running backtest for {symbol} on {timeframe} timeframe...")
    print("This may take a few moments...")
    
    # Run backtest
    result = backtester.run_backtest(symbol, timeframe)
    
    if result:
        print("\n📊 Backtest Results:")
        print("=" * 30)
        
        performance = result['performance']
        
        print(f"Total Trades: {performance.get('total_trades', 0)}")
        print(f"Win Rate: {performance.get('win_rate', 0):.2f}%")
        print(f"Total Return: {performance.get('total_return', 0):.2f}%")
        print(f"Total P&L: ${performance.get('total_pnl', 0):.2f}")
        print(f"Maximum Drawdown: {performance.get('max_drawdown', 0):.2f}%")
        print(f"Sharpe Ratio: {performance.get('sharpe_ratio', 0):.2f}")
        print(f"Profit Factor: {performance.get('profit_factor', 0):.2f}")
        
        # Show recent trades
        trades = result['results']['trades']
        if trades:
            print(f"\n📋 Recent Trades:")
            print("-" * 20)
            
            for i, trade in enumerate(trades[-3:], 1):  # Last 3 trades
                print(f"{i}. {trade['direction'].upper()} {trade['symbol']}")
                print(f"   Entry: ${trade['entry_price']:.2f} at {trade['entry_time']}")
                print(f"   Exit: ${trade['exit_price']:.2f} at {trade['exit_time']}")
                print(f"   P&L: ${trade['pnl']:.2f} ({trade['pnl_pct']:.2f}%)")
                print(f"   Reason: {trade['exit_reason']}")
                print()
    else:
        print("❌ Backtest failed or no results")

def example_portfolio_analysis():
    """Example of portfolio analysis"""
    print("\n📈 EXAMPLE: Portfolio Analysis")
    print("=" * 50)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    portfolio_summary = []
    
    # Analyze all symbols and timeframes
    for symbol in config.SYMBOLS:
        print(f"\n📊 {symbol}:")
        
        symbol_summary = {'symbol': symbol, 'timeframes': {}}
        
        for timeframe in config.TIMEFRAMES:
            print(f"  ⏰ {timeframe}:")
            
            # Fetch and analyze data
            df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
            
            if df.empty:
                print("    ❌ No data")
                continue
            
            df = data_fetcher.clean_data(df)
            
            if len(df) < 50:
                print(f"    ❌ Insufficient data")
                continue
            
            # Analyze market
            analysis = strategy.analyze_market(df)
            market_conditions = analysis['market_conditions']
            
            # Calculate scores
            risk_score = 0
            if market_conditions['risk_level'] == 'High':
                risk_score = 3
            elif market_conditions['risk_level'] == 'Medium':
                risk_score = 2
            else:
                risk_score = 1
            
            opportunity_score = 0
            if market_conditions['trend_strength'] == 'Strong':
                opportunity_score += 2
            if market_conditions['volatility'] == 'High':
                opportunity_score += 1
            if market_conditions['volume_condition'] == 'High':
                opportunity_score += 1
            
            overall_score = opportunity_score - risk_score
            
            print(f"    Risk: {risk_score}/3, Opportunity: {opportunity_score}/4, Overall: {overall_score}/4")
            
            # Store summary
            symbol_summary['timeframes'][timeframe] = {
                'risk_score': risk_score,
                'opportunity_score': opportunity_score,
                'overall_score': overall_score
            }
        
        portfolio_summary.append(symbol_summary)
    
    # Portfolio recommendations
    print(f"\n🎯 Portfolio Recommendations:")
    print("=" * 40)
    
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
            print(f"❌ {symbol}: No good opportunities")

def example_live_monitoring():
    """Example of live monitoring (limited to one update)"""
    print("\n🔄 EXAMPLE: Live Monitoring (Single Update)")
    print("=" * 50)
    
    data_fetcher = CryptoDataFetcher()
    strategy = CryptoTradingStrategy()
    
    print("Getting current market data...")
    
    for symbol in config.SYMBOLS:
        print(f"\n📊 {symbol}:")
        
        # Get real-time data
        df = data_fetcher.get_realtime_data(symbol)
        
        if df.empty:
            print("  ❌ No real-time data")
            continue
        
        # Get market info
        market_info = data_fetcher.get_market_info(symbol)
        
        if market_info:
            print(f"  💰 Price: ${market_info.get('last_price', 0):.2f}")
            print(f"  📈 24h Change: {market_info.get('change_24h', 0):.2f}%")
            print(f"  📊 24h Volume: {market_info.get('volume_24h', 0):.0f}")
            print(f"  💸 Spread: ${market_info.get('spread', 0):.4f}")
        
        # Quick analysis for signals
        for timeframe in config.TIMEFRAMES:
            df_tf = data_fetcher.get_data(symbol, timeframe, source='binance', limit=50)
            
            if not df_tf.empty:
                df_tf = data_fetcher.clean_data(df_tf)
                
                if len(df_tf) >= 30:
                    analysis = strategy.analyze_market(df_tf)
                    recommendation = strategy.get_trading_recommendation(analysis)
                    
                    if recommendation['action'] != 'HOLD':
                        print(f"  🎯 {timeframe}: {recommendation['action']} - "
                              f"Confidence: {recommendation['confidence']:.2%}")

def main():
    """Run all examples"""
    print("🚀 CRYPTOCURRENCY TRADING SYSTEM - EXAMPLES")
    print("=" * 60)
    print("This script demonstrates various features of the trading system.")
    print("Note: Examples use real market data and may take time to complete.")
    print()
    
    try:
        # Run examples
        example_market_analysis()
        example_trading_signals()
        example_backtest()
        example_portfolio_analysis()
        example_live_monitoring()
        
        print("\n✅ All examples completed successfully!")
        print("\n💡 To use the system interactively, run: python main.py")
        print("💡 For command line usage, see: python main.py --help")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("This might be due to network issues or API rate limits.")

if __name__ == "__main__":
    main()