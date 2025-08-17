import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from strategy import CryptoTradingStrategy
from data_fetcher import CryptoDataFetcher
import config

class CryptoBacktester:
    """Backtesting engine for cryptocurrency trading strategies"""
    
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.strategy = CryptoTradingStrategy()
        self.data_fetcher = CryptoDataFetcher()
        self.reset()
    
    def reset(self):
        """Reset backtester state"""
        self.capital = self.initial_capital
        self.positions = []
        self.trades = []
        self.equity_curve = []
        self.current_positions = {}
    
    def run_backtest(self, symbol: str, timeframe: str, start_date: str = None, 
                    end_date: str = None, source: str = 'binance') -> Dict:
        """Run backtest for a single symbol and timeframe"""
        print(f"Running backtest for {symbol} on {timeframe} timeframe...")
        
        # Fetch data
        df = self.data_fetcher.get_data(symbol, timeframe, source, limit=1000)
        
        if df.empty:
            print(f"No data available for {symbol}")
            return {}
        
        # Filter by date range if specified
        if start_date:
            df = df[df.index >= start_date]
        if end_date:
            df = df[df.index <= end_date]
        
        # Clean data
        df = self.data_fetcher.clean_data(df)
        
        if len(df) < 100:
            print(f"Insufficient data for {symbol}: {len(df)} candles")
            return {}
        
        # Run strategy analysis
        analysis = self.strategy.analyze_market(df)
        
        # Execute backtest
        results = self._execute_backtest(analysis, symbol, timeframe)
        
        # Calculate performance metrics
        performance = self._calculate_performance_metrics(results)
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'results': results,
            'performance': performance,
            'data': analysis['data']
        }
    
    def run_multi_timeframe_backtest(self, symbol: str, timeframes: List[str], 
                                   source: str = 'binance') -> Dict:
        """Run backtest for multiple timeframes"""
        print(f"Running multi-timeframe backtest for {symbol}...")
        
        results = {}
        
        for tf in timeframes:
            print(f"\n--- Testing {tf} timeframe ---")
            result = self.run_backtest(symbol, tf, source=source)
            if result:
                results[tf] = result
                self.reset()  # Reset for next timeframe
        
        return results
    
    def run_portfolio_backtest(self, symbols: List[str], timeframes: List[str], 
                             source: str = 'binance') -> Dict:
        """Run backtest for multiple symbols and timeframes"""
        print(f"Running portfolio backtest for {len(symbols)} symbols...")
        
        portfolio_results = {}
        
        for symbol in symbols:
            print(f"\n=== Testing {symbol} ===")
            symbol_results = self.run_multi_timeframe_backtest(symbol, timeframes, source)
            if symbol_results:
                portfolio_results[symbol] = symbol_results
                self.reset()  # Reset for next symbol
        
        # Calculate portfolio performance
        portfolio_performance = self._calculate_portfolio_performance(portfolio_results)
        
        return {
            'symbols': symbols,
            'timeframes': timeframes,
            'results': portfolio_results,
            'portfolio_performance': portfolio_performance
        }
    
    def _execute_backtest(self, analysis: Dict, symbol: str, timeframe: str) -> Dict:
        """Execute the backtest based on strategy analysis"""
        df = analysis['data']
        entry_signals = analysis['entry_signals']
        exit_signals = analysis['exit_signals']
        
        results = {
            'trades': [],
            'equity_curve': [],
            'positions': [],
            'metrics': {}
        }
        
        capital = self.initial_capital
        current_position = None
        
        for i in range(1, len(df)):
            current_bar = df.iloc[i]
            previous_bar = df.iloc[i-1]
            
            # Check for exit signals if we have a position
            if current_position:
                exit_signal = exit_signals.iloc[i]
                
                if exit_signal != 0 or self._check_stop_loss(current_position, current_bar):
                    # Close position
                    trade_result = self._close_position(current_position, current_bar, i)
                    results['trades'].append(trade_result)
                    
                    # Update capital
                    if trade_result['pnl'] > 0:
                        capital += trade_result['pnl']
                    else:
                        capital -= abs(trade_result['pnl'])
                    
                    current_position = None
            
            # Check for entry signals if we don't have a position
            if not current_position:
                entry_signal = entry_signals.iloc[i]
                
                if entry_signal != 0:
                    # Open new position
                    current_position = self._open_position(
                        entry_signal, current_bar, i, capital, symbol, timeframe
                    )
                    results['positions'].append(current_position)
            
            # Update equity curve
            if current_position:
                unrealized_pnl = self._calculate_unrealized_pnl(current_position, current_bar)
                current_equity = capital + unrealized_pnl
            else:
                current_equity = capital
            
            results['equity_curve'].append({
                'timestamp': current_bar.name,
                'equity': current_equity,
                'capital': capital,
                'unrealized_pnl': unrealized_pnl if current_position else 0
            })
        
        # Close any remaining position at the end
        if current_position:
            last_bar = df.iloc[-1]
            trade_result = self._close_position(current_position, last_bar, len(df) - 1)
            results['trades'].append(trade_result)
        
        return results
    
    def _open_position(self, signal: int, bar: pd.Series, index: int, 
                      capital: float, symbol: str, timeframe: str) -> Dict:
        """Open a new trading position"""
        direction = 'long' if signal == 1 else 'short'
        entry_price = bar['close']
        
        # Calculate position size (10% of capital)
        position_value = capital * 0.1
        quantity = position_value / entry_price
        
        # Calculate stop loss and take profit
        atr = bar['atr'] if not pd.isna(bar['atr']) else entry_price * 0.02
        
        if direction == 'long':
            stop_loss = entry_price - (atr * 2)
            take_profit = entry_price + (atr * 4)  # 1:2 risk-reward
        else:
            stop_loss = entry_price + (atr * 2)
            take_profit = entry_price - (atr * 4)
        
        position = {
            'id': len(self.positions) + 1,
            'symbol': symbol,
            'timeframe': timeframe,
            'direction': direction,
            'entry_time': bar.name,
            'entry_price': entry_price,
            'quantity': quantity,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_index': index,
            'status': 'open'
        }
        
        return position
    
    def _close_position(self, position: Dict, bar: pd.Series, index: int) -> Dict:
        """Close a trading position"""
        exit_price = bar['close']
        exit_time = bar.name
        
        # Calculate P&L
        if position['direction'] == 'long':
            pnl = (exit_price - position['entry_price']) * position['quantity']
        else:
            pnl = (position['entry_price'] - exit_price) * position['quantity']
        
        # Calculate trade metrics
        entry_value = position['entry_price'] * position['quantity']
        exit_value = exit_price * position['quantity']
        
        # Determine exit reason
        if exit_price <= position['stop_loss'] and position['direction'] == 'long':
            exit_reason = 'stop_loss'
        elif exit_price >= position['stop_loss'] and position['direction'] == 'short':
            exit_reason = 'stop_loss'
        elif exit_price >= position['take_profit'] and position['direction'] == 'long':
            exit_reason = 'take_profit'
        elif exit_price <= position['take_profit'] and position['direction'] == 'short':
            exit_reason = 'take_profit'
        else:
            exit_reason = 'signal'
        
        trade_result = {
            'position_id': position['id'],
            'symbol': position['symbol'],
            'timeframe': position['timeframe'],
            'direction': position['direction'],
            'entry_time': position['entry_time'],
            'exit_time': exit_time,
            'entry_price': position['entry_price'],
            'exit_price': exit_price,
            'quantity': position['quantity'],
            'entry_value': entry_value,
            'exit_value': exit_value,
            'pnl': pnl,
            'pnl_pct': (pnl / entry_value) * 100,
            'exit_reason': exit_reason,
            'duration': (exit_time - position['entry_time']).total_seconds() / 3600,  # hours
            'stop_loss': position['stop_loss'],
            'take_profit': position['take_profit']
        }
        
        return trade_result
    
    def _check_stop_loss(self, position: Dict, bar: pd.Series) -> bool:
        """Check if stop loss has been hit"""
        if position['direction'] == 'long':
            return bar['low'] <= position['stop_loss']
        else:
            return bar['high'] >= position['stop_loss']
    
    def _calculate_unrealized_pnl(self, position: Dict, bar: pd.Series) -> float:
        """Calculate unrealized P&L for open position"""
        current_price = bar['close']
        
        if position['direction'] == 'long':
            return (current_price - position['entry_price']) * position['quantity']
        else:
            return (position['entry_price'] - current_price) * position['quantity']
    
    def _calculate_performance_metrics(self, results: Dict) -> Dict:
        """Calculate comprehensive performance metrics"""
        if not results['trades']:
            return {}
        
        trades_df = pd.DataFrame(results['trades'])
        equity_df = pd.DataFrame(results['equity_curve'])
        
        # Basic metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = trades_df['pnl'].sum()
        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Average metrics
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        # Risk metrics
        max_drawdown = self._calculate_max_drawdown(equity_df['equity'])
        sharpe_ratio = self._calculate_sharpe_ratio(equity_df['equity'])
        
        # Return metrics
        initial_equity = self.initial_capital
        final_equity = equity_df['equity'].iloc[-1] if not equity_df.empty else initial_equity
        total_return = ((final_equity - initial_equity) / initial_equity) * 100
        
        # Time-based metrics
        if not equity_df.empty:
            start_time = equity_df['timestamp'].iloc[0]
            end_time = equity_df['timestamp'].iloc[-1]
            duration_hours = (end_time - start_time).total_seconds() / 3600
            hourly_return = total_return / duration_hours if duration_hours > 0 else 0
        else:
            duration_hours = 0
            hourly_return = 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'total_return': total_return,
            'duration_hours': duration_hours,
            'hourly_return': hourly_return,
            'initial_capital': initial_equity,
            'final_capital': final_equity
        }
    
    def _calculate_max_drawdown(self, equity_series: pd.Series) -> float:
        """Calculate maximum drawdown"""
        if equity_series.empty:
            return 0
        
        peak = equity_series.expanding().max()
        drawdown = (equity_series - peak) / peak * 100
        return abs(drawdown.min())
    
    def _calculate_sharpe_ratio(self, equity_series: pd.Series) -> float:
        """Calculate Sharpe ratio"""
        if equity_series.empty or len(equity_series) < 2:
            return 0
        
        returns = equity_series.pct_change().dropna()
        if returns.std() == 0:
            return 0
        
        return (returns.mean() / returns.std()) * np.sqrt(252 * 24)  # Annualized
    
    def _calculate_portfolio_performance(self, portfolio_results: Dict) -> Dict:
        """Calculate overall portfolio performance"""
        all_trades = []
        total_initial_capital = 0
        total_final_capital = 0
        
        for symbol, symbol_results in portfolio_results.items():
            for timeframe, timeframe_results in symbol_results.items():
                if 'results' in timeframe_results and 'trades' in timeframe_results['results']:
                    trades = timeframe_results['results']['trades']
                    for trade in trades:
                        trade['portfolio_symbol'] = symbol
                        trade['portfolio_timeframe'] = timeframe
                        all_trades.append(trade)
                
                if 'performance' in timeframe_results:
                    perf = timeframe_results['performance']
                    total_initial_capital += perf.get('initial_capital', 0)
                    total_final_capital += perf.get('final_capital', 0)
        
        if not all_trades:
            return {}
        
        # Calculate portfolio metrics
        portfolio_trades_df = pd.DataFrame(all_trades)
        
        total_trades = len(portfolio_trades_df)
        winning_trades = len(portfolio_trades_df[portfolio_trades_df['pnl'] > 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_pnl = portfolio_trades_df['pnl'].sum()
        total_return = ((total_final_capital - total_initial_capital) / total_initial_capital) * 100 if total_initial_capital > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'initial_capital': total_initial_capital,
            'final_capital': total_final_capital
        }
    
    def plot_results(self, results: Dict, save_path: str = None):
        """Plot backtest results"""
        if not results or 'data' not in results:
            print("No results to plot")
            return
        
        df = results['data']
        trades = results.get('trades', [])
        equity_curve = results.get('equity_curve', [])
        
        # Create subplots
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle(f'Backtest Results - {results.get("symbol", "Unknown")} ({results.get("timeframe", "Unknown")})')
        
        # Price chart with indicators
        ax1 = axes[0]
        ax1.plot(df.index, df['close'], label='Close Price', color='black', linewidth=1)
        
        # Plot EMAs
        if 'ema_9' in df.columns:
            ax1.plot(df.index, df['ema_9'], label='EMA 9', color='blue', alpha=0.7)
        if 'ema_21' in df.columns:
            ax1.plot(df.index, df['ema_21'], label='EMA 21', color='orange', alpha=0.7)
        if 'ema_50' in df.columns:
            ax1.plot(df.index, df['ema_50'], label='EMA 50', color='red', alpha=0.7)
        
        # Plot Bollinger Bands
        if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
            ax1.plot(df.index, df['bb_upper'], label='BB Upper', color='gray', alpha=0.5, linestyle='--')
            ax1.plot(df.index, df['bb_lower'], label='BB Lower', color='gray', alpha=0.5, linestyle='--')
        
        # Plot trades
        if trades:
            for trade in trades:
                if trade['direction'] == 'long':
                    ax1.scatter(trade['entry_time'], trade['entry_price'], 
                               color='green', marker='^', s=100, alpha=0.7)
                    ax1.scatter(trade['exit_time'], trade['exit_price'], 
                               color='red', marker='v', s=100, alpha=0.7)
                else:
                    ax1.scatter(trade['entry_time'], trade['entry_price'], 
                               color='red', marker='v', s=100, alpha=0.7)
                    ax1.scatter(trade['exit_time'], trade['exit_price'], 
                               color='green', marker='^', s=100, alpha=0.7)
        
        ax1.set_title('Price Chart with Indicators and Trades')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Volume chart
        ax2 = axes[1]
        ax2.bar(df.index, df['volume'], alpha=0.6, color='blue')
        if 'vwap' in df.columns:
            ax2.plot(df.index, df['vwap'], color='red', alpha=0.7, label='VWAP')
        ax2.set_title('Volume')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Equity curve
        ax3 = axes[2]
        if equity_curve:
            equity_df = pd.DataFrame(equity_curve)
            ax3.plot(equity_df['timestamp'], equity_df['equity'], label='Portfolio Value', color='green')
            ax3.axhline(y=self.initial_capital, color='red', linestyle='--', alpha=0.7, label='Initial Capital')
            ax3.set_title('Equity Curve')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def generate_report(self, results: Dict) -> str:
        """Generate a comprehensive backtest report"""
        if not results:
            return "No results to report"
        
        performance = results.get('performance', {})
        trades = results.get('trades', [])
        
        report = f"""
=== CRYPTOCURRENCY TRADING STRATEGY BACKTEST REPORT ===

Symbol: {results.get('symbol', 'Unknown')}
Timeframe: {results.get('timeframe', 'Unknown')}
Period: {results.get('data', pd.DataFrame()).index[0] if results.get('data') is not None and not results.get('data').empty else 'Unknown'} to {results.get('data', pd.DataFrame()).index[-1] if results.get('data') is not None and not results.get('data').empty else 'Unknown'}

=== PERFORMANCE SUMMARY ===
Total Return: {performance.get('total_return', 0):.2f}%
Total P&L: ${performance.get('total_pnl', 0):.2f}
Initial Capital: ${performance.get('initial_capital', 0):.2f}
Final Capital: ${performance.get('final_capital', 0):.2f}

=== TRADING STATISTICS ===
Total Trades: {performance.get('total_trades', 0)}
Winning Trades: {performance.get('winning_trades', 0)}
Losing Trades: {performance.get('losing_trades', 0)}
Win Rate: {performance.get('win_rate', 0):.2f}%

=== RISK METRICS ===
Maximum Drawdown: {performance.get('max_drawdown', 0):.2f}%
Sharpe Ratio: {performance.get('sharpe_ratio', 0):.2f}
Profit Factor: {performance.get('profit_factor', 0):.2f}

=== TRADE ANALYSIS ===
Average Win: ${performance.get('avg_win', 0):.2f}
Average Loss: ${performance.get('avg_loss', 0):.2f}
Duration: {performance.get('duration_hours', 0):.1f} hours
Hourly Return: {performance.get('hourly_return', 0):.4f}%

=== RECENT TRADES ===
"""
        
        if trades:
            recent_trades = trades[-5:]  # Last 5 trades
            for trade in recent_trades:
                report += f"""
Trade {trade.get('position_id', 'N/A')}:
  {trade.get('direction', 'N/A').upper()} {trade.get('symbol', 'N/A')}
  Entry: ${trade.get('entry_price', 0):.2f} at {trade.get('entry_time', 'N/A')}
  Exit: ${trade.get('exit_price', 0):.2f} at {trade.get('exit_time', 'N/A')}
  P&L: ${trade.get('pnl', 0):.2f} ({trade.get('pnl_pct', 0):.2f}%)
  Reason: {trade.get('exit_reason', 'N/A')}
"""
        
        return report