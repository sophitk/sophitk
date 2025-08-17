import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from indicators import CryptoIndicators
import config

class CryptoTradingStrategy:
    """High-win-rate cryptocurrency trading strategy for day trading"""
    
    def __init__(self):
        self.indicators = CryptoIndicators()
        self.entry_threshold = 0.6  # Minimum signal strength for entry
        self.exit_threshold = 0.3   # Signal strength for exit
        self.trailing_stop = True
        self.trailing_stop_distance = 0.015  # 1.5% trailing stop
        
    def analyze_market(self, df: pd.DataFrame) -> Dict:
        """Analyze market conditions and generate trading signals"""
        # Calculate all indicators
        df_with_indicators = self.indicators.calculate_all_indicators(df)
        
        # Generate individual signals
        signals = self.indicators.generate_signals(df_with_indicators)
        
        # Get composite signal
        composite_signal = self.indicators.get_composite_signal(signals)
        
        # Add signals to dataframe
        df_with_indicators['composite_signal'] = composite_signal
        
        # Generate entry/exit signals
        entry_signals = self._generate_entry_signals(df_with_indicators, signals)
        exit_signals = self._generate_exit_signals(df_with_indicators, signals)
        
        # Market condition analysis
        market_conditions = self._analyze_market_conditions(df_with_indicators)
        
        return {
            'data': df_with_indicators,
            'signals': signals,
            'composite_signal': composite_signal,
            'entry_signals': entry_signals,
            'exit_signals': exit_signals,
            'market_conditions': market_conditions
        }
    
    def _generate_entry_signals(self, df: pd.DataFrame, signals: Dict) -> pd.Series:
        """Generate entry signals based on multiple confirmation factors"""
        entry_signal = pd.Series(0, index=df.index)
        
        # Strong bullish entry conditions
        strong_bullish = (
            (df['composite_signal'] > self.entry_threshold) &
            (df['close'] > df['ema_9']) &
            (df['ema_9'] > df['ema_21']) &
            (df['volume'] > df['volume'].rolling(20).mean() * 1.2) &
            (df['rsi'] > 40) & (df['rsi'] < 70) &
            (df['close'] > df['bb_middle']) &
            (df['macd'] > df['macd_signal']) &
            (df['close'] > df['vwap'])
        )
        
        # Strong bearish entry conditions
        strong_bearish = (
            (df['composite_signal'] < -self.entry_threshold) &
            (df['close'] < df['ema_9']) &
            (df['ema_9'] < df['ema_21']) &
            (df['volume'] > df['volume'].rolling(20).mean() * 1.2) &
            (df['rsi'] < 60) & (df['rsi'] > 30) &
            (df['close'] < df['bb_middle']) &
            (df['macd'] < df['macd_signal']) &
            (df['close'] < df['vwap'])
        )
        
        # Breakout entry conditions
        breakout_bullish = (
            (df['close'] > df['bb_upper']) &
            (df['volume'] > df['volume'].rolling(20).mean() * 1.5) &
            (df['rsi'] < 70) &
            (df['close'] > df['close'].shift(1)) &
            (df['close'].shift(1) > df['close'].shift(2))
        )
        
        breakout_bearish = (
            (df['close'] < df['bb_lower']) &
            (df['volume'] > df['volume'].rolling(20).mean() * 1.5) &
            (df['rsi'] > 30) &
            (df['close'] < df['close'].shift(1)) &
            (df['close'].shift(1) < df['close'].shift(2))
        )
        
        # Support/Resistance bounce entries
        support_bounce = (
            (df['close'] <= df['support_1'] * 1.005) &
            (df['rsi'] < 40) &
            (df['stoch_k'] < 30) &
            (df['volume'] > df['volume'].rolling(20).mean())
        )
        
        resistance_rejection = (
            (df['close'] >= df['resistance_1'] * 0.995) &
            (df['rsi'] > 60) &
            (df['stoch_k'] > 70) &
            (df['volume'] > df['volume'].rolling(20).mean())
        )
        
        # Combine all entry conditions
        bullish_entries = strong_bullish | breakout_bullish | support_bounce
        bearish_entries = strong_bearish | breakout_bearish | resistance_rejection
        
        # Add trend confirmation
        trend_confirmed_bullish = (
            bullish_entries &
            (df['ema_50'] > df['ema_200']) &
            (df['adx'] > 25)
        )
        
        trend_confirmed_bearish = (
            bearish_entries &
            (df['ema_50'] < df['ema_200']) &
            (df['adx'] > 25)
        )
        
        # Final entry signals
        entry_signal[trend_confirmed_bullish] = 1
        entry_signal[trend_confirmed_bearish] = -1
        
        return entry_signal
    
    def _generate_exit_signals(self, df: pd.DataFrame, signals: Dict) -> pd.Series:
        """Generate exit signals for position management"""
        exit_signal = pd.Series(0, index=df.index)
        
        # Take profit signals
        take_profit_bullish = (
            (df['rsi'] > 80) |
            (df['close'] > df['bb_upper'] * 1.02) |
            (df['stoch_k'] > 90) |
            (df['mfi'] > 85)
        )
        
        take_profit_bearish = (
            (df['rsi'] < 20) |
            (df['close'] < df['bb_lower'] * 0.98) |
            (df['stoch_k'] < 10) |
            (df['mfi'] < 15)
        )
        
        # Stop loss signals
        stop_loss_bullish = (
            (df['close'] < df['ema_21']) &
            (df['macd'] < df['macd_signal']) &
            (df['rsi'] < 35)
        )
        
        stop_loss_bearish = (
            (df['close'] > df['ema_21']) &
            (df['macd'] > df['macd_signal']) &
            (df['rsi'] > 65)
        )
        
        # Trend reversal signals
        trend_reversal_bullish = (
            (df['ema_9'] < df['ema_21']) &
            (df['close'] < df['ema_9']) &
            (df['macd'] < 0)
        )
        
        trend_reversal_bearish = (
            (df['ema_9'] > df['ema_21']) &
            (df['close'] > df['ema_9']) &
            (df['macd'] > 0)
        )
        
        # Combine exit conditions
        exit_bullish = take_profit_bullish | stop_loss_bullish | trend_reversal_bullish
        exit_bearish = take_profit_bearish | stop_loss_bearish | trend_reversal_bearish
        
        exit_signal[exit_bullish] = 1
        exit_signal[exit_bearish] = -1
        
        return exit_signal
    
    def _analyze_market_conditions(self, df: pd.DataFrame) -> Dict:
        """Analyze overall market conditions"""
        latest = df.iloc[-1]
        
        # Trend strength
        trend_strength = 'Strong' if latest['adx'] > 25 else 'Weak'
        trend_direction = 'Bullish' if latest['ema_50'] > latest['ema_200'] else 'Bearish'
        
        # Volatility
        volatility = 'High' if latest['bb_width'] > df['bb_width'].rolling(20).mean().iloc[-1] else 'Low'
        
        # Volume
        volume_condition = 'High' if latest['volume'] > df['volume'].rolling(20).mean().iloc[-1] * 1.5 else 'Normal'
        
        # Market phase
        if latest['rsi'] > 70 and latest['stoch_k'] > 80:
            market_phase = 'Overbought'
        elif latest['rsi'] < 30 and latest['stoch_k'] < 20:
            market_phase = 'Oversold'
        else:
            market_phase = 'Neutral'
        
        # Risk level
        if latest['rsi'] > 80 or latest['rsi'] < 20:
            risk_level = 'High'
        elif latest['rsi'] > 70 or latest['rsi'] < 30:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'trend_strength': trend_strength,
            'trend_direction': trend_direction,
            'volatility': volatility,
            'volume_condition': volume_condition,
            'market_phase': market_phase,
            'risk_level': risk_level,
            'current_price': latest['close'],
            'support_level': latest['support_1'],
            'resistance_level': latest['resistance_1']
        }
    
    def get_position_size(self, capital: float, risk_per_trade: float, 
                         stop_loss_pct: float) -> float:
        """Calculate position size based on risk management"""
        risk_amount = capital * risk_per_trade
        position_size = risk_amount / stop_loss_pct
        return position_size
    
    def calculate_stop_loss(self, entry_price: float, direction: str, 
                           atr: float) -> float:
        """Calculate dynamic stop loss based on ATR"""
        if direction == 'long':
            stop_loss = entry_price - (atr * 2)  # 2x ATR below entry
        else:
            stop_loss = entry_price + (atr * 2)  # 2x ATR above entry
        
        return stop_loss
    
    def calculate_take_profit(self, entry_price: float, direction: str, 
                             stop_loss: float) -> float:
        """Calculate take profit based on risk-reward ratio"""
        risk = abs(entry_price - stop_loss)
        reward = risk * 2  # 1:2 risk-reward ratio
        
        if direction == 'long':
            take_profit = entry_price + reward
        else:
            take_profit = entry_price - reward
        
        return take_profit
    
    def should_trade(self, market_conditions: Dict) -> bool:
        """Determine if current market conditions are suitable for trading"""
        # Avoid trading in extreme conditions
        if market_conditions['risk_level'] == 'High':
            return False
        
        # Avoid trading in very low volatility
        if market_conditions['volatility'] == 'Low':
            return False
        
        # Avoid trading in very weak trends
        if market_conditions['trend_strength'] == 'Weak':
            return False
        
        return True
    
    def get_trading_recommendation(self, analysis: Dict) -> Dict:
        """Generate trading recommendation based on analysis"""
        df = analysis['data']
        entry_signals = analysis['entry_signals']
        exit_signals = analysis['exit_signals']
        market_conditions = analysis['market_conditions']
        
        latest = df.iloc[-1]
        
        recommendation = {
            'action': 'HOLD',
            'confidence': 0.0,
            'reason': '',
            'entry_price': None,
            'stop_loss': None,
            'take_profit': None,
            'risk_reward_ratio': 0.0
        }
        
        # Check if we should trade
        if not self.should_trade(market_conditions):
            recommendation['reason'] = f"Market conditions not suitable: {market_conditions['risk_level']} risk, {market_conditions['volatility']} volatility"
            return recommendation
        
        # Check for entry signals
        if entry_signals.iloc[-1] == 1:  # Bullish entry
            entry_price = latest['close']
            stop_loss = self.calculate_stop_loss(entry_price, 'long', latest['atr'])
            take_profit = self.calculate_take_profit(entry_price, 'long', stop_loss)
            
            recommendation.update({
                'action': 'BUY',
                'confidence': min(abs(analysis['composite_signal'].iloc[-1]), 1.0),
                'reason': f"Strong bullish signal with {market_conditions['trend_direction']} trend",
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_reward_ratio': abs(take_profit - entry_price) / abs(entry_price - stop_loss)
            })
            
        elif entry_signals.iloc[-1] == -1:  # Bearish entry
            entry_price = latest['close']
            stop_loss = self.calculate_stop_loss(entry_price, 'short', latest['atr'])
            take_profit = self.calculate_take_profit(entry_price, 'short', stop_loss)
            
            recommendation.update({
                'action': 'SELL',
                'confidence': min(abs(analysis['composite_signal'].iloc[-1]), 1.0),
                'reason': f"Strong bearish signal with {market_conditions['trend_direction']} trend",
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_reward_ratio': abs(take_profit - entry_price) / abs(entry_price - stop_loss)
            })
        
        return recommendation