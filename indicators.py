import pandas as pd
import numpy as np
import ta
from typing import Tuple, Dict, List

class CryptoIndicators:
    """High-accuracy technical indicators for cryptocurrency trading"""
    
    def __init__(self):
        self.indicators_data = {}
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators for the dataframe"""
        df = df.copy()
        
        # Volume indicators
        df = self.add_volume_indicators(df)
        
        # Trend indicators
        df = self.add_trend_indicators(df)
        
        # Momentum indicators
        df = self.add_momentum_indicators(df)
        
        # Volatility indicators
        df = self.add_volatility_indicators(df)
        
        # Support/Resistance levels
        df = self.add_support_resistance(df)
        
        return df
    
    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based indicators"""
        # Volume Weighted Average Price (VWAP)
        df['vwap'] = ta.volume.volume_weighted_average_price(
            high=df['high'], low=df['low'], close=df['close'], volume=df['volume']
        )
        
        # On Balance Volume (OBV)
        df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
        
        # Volume Rate of Change
        df['volume_roc'] = ta.volume.volume_rate_of_change(df['volume'])
        
        # Money Flow Index
        df['mfi'] = ta.volume.money_flow_index(
            high=df['high'], low=df['low'], close=df['close'], volume=df['volume']
        )
        
        return df
    
    def add_trend_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add trend-following indicators"""
        # Exponential Moving Averages
        df['ema_9'] = ta.trend.ema_indicator(df['close'], window=9)
        df['ema_21'] = ta.trend.ema_indicator(df['close'], window=21)
        df['ema_50'] = ta.trend.ema_indicator(df['close'], window=50)
        df['ema_200'] = ta.trend.ema_indicator(df['close'], window=200)
        
        # MACD
        df['macd'] = ta.trend.macd(df['close'])
        df['macd_signal'] = ta.trend.macd_signal(df['close'])
        df['macd_histogram'] = ta.trend.macd_diff(df['close'])
        
        # Parabolic SAR
        df['psar'] = ta.trend.psar_down(df['high'], df['low'], df['close'])
        
        # ADX (Average Directional Index)
        df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'])
        
        # Ichimoku Cloud
        df['ichimoku_a'] = ta.trend.ichimoku_a(df['high'], df['low'])
        df['ichimoku_b'] = ta.trend.ichimoku_b(df['high'], df['low'])
        df['ichimoku_base'] = ta.trend.ichimoku_base_line(df['high'], df['low'])
        df['ichimoku_conversion'] = ta.trend.ichimoku_conversion_line(df['high'], df['low'])
        
        return df
    
    def add_momentum_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add momentum indicators"""
        # RSI
        df['rsi'] = ta.momentum.rsi(df['close'])
        
        # Stochastic Oscillator
        df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'])
        df['stoch_d'] = ta.momentum.stoch_signal(df['high'], df['low'], df['close'])
        
        # Williams %R
        df['williams_r'] = ta.momentum.williams_r(df['high'], df['low'], df['close'])
        
        # Commodity Channel Index
        df['cci'] = ta.trend.cci(df['high'], df['low'], df['close'])
        
        # Rate of Change
        df['roc'] = ta.momentum.roc(df['close'])
        
        # Relative Vigor Index
        df['rvi'] = ta.momentum.relative_vigor_index(df['open'], df['high'], df['low'], df['close'])
        
        return df
    
    def add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volatility indicators"""
        # Bollinger Bands
        df['bb_upper'] = ta.volatility.bollinger_hband(df['close'])
        df['bb_middle'] = ta.volatility.bollinger_mavg(df['close'])
        df['bb_lower'] = ta.volatility.bollinger_lband(df['close'])
        df['bb_width'] = ta.volatility.bollinger_wband(df['close'])
        df['bb_percent'] = ta.volatility.bollinger_pband(df['close'])
        
        # Average True Range
        df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
        
        # Keltner Channel
        df['keltner_upper'] = ta.volatility.keltner_channel_hband(df['high'], df['low'], df['close'])
        df['keltner_middle'] = ta.volatility.keltner_channel_mband(df['high'], df['low'], df['close'])
        df['keltner_lower'] = ta.volatility.keltner_channel_lband(df['high'], df['low'], df['close'])
        
        # Donchian Channel
        df['donchian_upper'] = ta.volatility.donchian_channel_hband(df['high'], df['low'])
        df['donchian_middle'] = ta.volatility.donchian_channel_mband(df['high'], df['low'])
        df['donchian_lower'] = ta.volatility.donchian_channel_lband(df['high'], df['low'])
        
        return df
    
    def add_support_resistance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add support and resistance levels"""
        # Pivot Points
        df['pivot'] = ta.trend.pivot_points(df['high'], df['low'], df['close'])
        df['support_1'] = ta.trend.pivot_points(df['high'], df['low'], df['close'], mode='support')
        df['resistance_1'] = ta.trend.pivot_points(df['high'], df['low'], df['close'], mode='resistance')
        
        # Fibonacci Retracement levels (simplified)
        df['fib_236'] = df['high'].rolling(20).max() * 0.236
        df['fib_382'] = df['high'].rolling(20).max() * 0.382
        df['fib_500'] = df['high'].rolling(20).max() * 0.500
        df['fib_618'] = df['high'].rolling(20).max() * 0.618
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Generate trading signals based on multiple indicators"""
        signals = {}
        
        # Trend signals
        signals['ema_trend'] = self._ema_trend_signal(df)
        signals['macd_signal'] = self._macd_signal(df)
        signals['ichimoku_signal'] = self._ichimoku_signal(df)
        
        # Momentum signals
        signals['rsi_signal'] = self._rsi_signal(df)
        signals['stochastic_signal'] = self._stochastic_signal(df)
        signals['cci_signal'] = self._cci_signal(df)
        
        # Volatility signals
        signals['bollinger_signal'] = self._bollinger_signal(df)
        signals['keltner_signal'] = self._keltner_signal(df)
        
        # Volume signals
        signals['volume_signal'] = self._volume_signal(df)
        signals['mfi_signal'] = self._mfi_signal(df)
        
        # Support/Resistance signals
        signals['support_resistance_signal'] = self._support_resistance_signal(df)
        
        return signals
    
    def _ema_trend_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate EMA trend signals"""
        signal = pd.Series(0, index=df.index)
        
        # Bullish: price above all EMAs and EMAs aligned upward
        bullish = (df['close'] > df['ema_9']) & (df['ema_9'] > df['ema_21']) & \
                  (df['ema_21'] > df['ema_50']) & (df['ema_50'] > df['ema_200'])
        
        # Bearish: price below all EMAs and EMAs aligned downward
        bearish = (df['close'] < df['ema_9']) & (df['ema_9'] < df['ema_21']) & \
                  (df['ema_21'] < df['ema_50']) & (df['ema_50'] < df['ema_200'])
        
        signal[bullish] = 1
        signal[bearish] = -1
        
        return signal
    
    def _macd_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate MACD signals"""
        signal = pd.Series(0, index=df.index)
        
        # Bullish: MACD crosses above signal line
        bullish = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
        
        # Bearish: MACD crosses below signal line
        bearish = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))
        
        signal[bullish] = 1
        signal[bearish] = -1
        
        return signal
    
    def _ichimoku_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate Ichimoku signals"""
        signal = pd.Series(0, index=df.index)
        
        # Bullish: price above cloud and conversion line above base line
        bullish = (df['close'] > df['ichimoku_a']) & (df['close'] > df['ichimoku_b']) & \
                  (df['ichimoku_conversion'] > df['ichimoku_base'])
        
        # Bearish: price below cloud and conversion line below base line
        bearish = (df['close'] < df['ichimoku_a']) & (df['close'] < df['ichimoku_b']) & \
                  (df['ichimoku_conversion'] < df['ichimoku_base'])
        
        signal[bullish] = 1
        signal[bearish] = -1
        
        return signal
    
    def _rsi_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate RSI signals"""
        signal = pd.Series(0, index=df.index)
        
        # Oversold bounce
        oversold_bounce = (df['rsi'] < 30) & (df['rsi'].shift(1) >= 30)
        
        # Overbought reversal
        overbought_reversal = (df['rsi'] > 70) & (df['rsi'].shift(1) <= 70)
        
        # RSI divergence (simplified)
        price_higher = df['close'] > df['close'].shift(5)
        rsi_lower = df['rsi'] < df['rsi'].shift(5)
        bearish_divergence = price_higher & rsi_lower & (df['rsi'] > 70)
        
        price_lower = df['close'] < df['close'].shift(5)
        rsi_higher = df['rsi'] > df['rsi'].shift(5)
        bullish_divergence = price_lower & rsi_higher & (df['rsi'] < 30)
        
        signal[oversold_bounce | bullish_divergence] = 1
        signal[overbought_reversal | bearish_divergence] = -1
        
        return signal
    
    def _stochastic_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate Stochastic signals"""
        signal = pd.Series(0, index=df.index)
        
        # Oversold bounce
        oversold_bounce = (df['stoch_k'] < 20) & (df['stoch_k'].shift(1) >= 20)
        
        # Overbought reversal
        overbought_reversal = (df['stoch_k'] > 80) & (df['stoch_k'].shift(1) <= 80)
        
        # Bullish crossover
        bullish_cross = (df['stoch_k'] > df['stoch_d']) & (df['stoch_k'].shift(1) <= df['stoch_d'].shift(1))
        
        # Bearish crossover
        bearish_cross = (df['stoch_k'] < df['stoch_d']) & (df['stoch_k'].shift(1) >= df['stoch_d'].shift(1))
        
        signal[oversold_bounce | bullish_cross] = 1
        signal[overbought_reversal | bearish_cross] = -1
        
        return signal
    
    def _cci_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate CCI signals"""
        signal = pd.Series(0, index=df.index)
        
        # Oversold bounce
        oversold_bounce = (df['cci'] < -100) & (df['cci'].shift(1) >= -100)
        
        # Overbought reversal
        overbought_reversal = (df['cci'] > 100) & (df['cci'].shift(1) <= 100)
        
        signal[oversold_bounce] = 1
        signal[overbought_reversal] = -1
        
        return signal
    
    def _bollinger_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate Bollinger Bands signals"""
        signal = pd.Series(0, index=df.index)
        
        # Price touches lower band (potential bounce)
        lower_touch = df['close'] <= df['bb_lower'] * 1.001
        
        # Price touches upper band (potential reversal)
        upper_touch = df['close'] >= df['bb_upper'] * 0.999
        
        # Squeeze (low volatility)
        squeeze = df['bb_width'] < df['bb_width'].rolling(20).mean() * 0.5
        
        signal[lower_touch] = 1
        signal[upper_touch] = -1
        
        return signal
    
    def _keltner_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate Keltner Channel signals"""
        signal = pd.Series(0, index=df.index)
        
        # Price touches lower channel
        lower_touch = df['close'] <= df['keltner_lower'] * 1.001
        
        # Price touches upper channel
        upper_touch = df['close'] >= df['keltner_upper'] * 0.999
        
        signal[lower_touch] = 1
        signal[upper_touch] = -1
        
        return signal
    
    def _volume_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate volume-based signals"""
        signal = pd.Series(0, index=df.index)
        
        # High volume breakout
        volume_breakout = (df['volume'] > df['volume'].rolling(20).mean() * 1.5) & \
                         (df['close'] > df['close'].shift(1))
        
        # High volume breakdown
        volume_breakdown = (df['volume'] > df['volume'].rolling(20).mean() * 1.5) & \
                          (df['close'] < df['close'].shift(1))
        
        signal[volume_breakout] = 1
        signal[volume_breakdown] = -1
        
        return signal
    
    def _mfi_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate MFI signals"""
        signal = pd.Series(0, index=df.index)
        
        # Oversold bounce
        oversold_bounce = (df['mfi'] < 20) & (df['mfi'].shift(1) >= 20)
        
        # Overbought reversal
        overbought_reversal = (df['mfi'] > 80) & (df['mfi'].shift(1) <= 80)
        
        signal[oversold_bounce] = 1
        signal[overbought_reversal] = -1
        
        return signal
    
    def _support_resistance_signal(self, df: pd.DataFrame) -> pd.Series:
        """Generate support/resistance signals"""
        signal = pd.Series(0, index=df.index)
        
        # Price near support (within 0.5%)
        near_support = (df['close'] <= df['support_1'] * 1.005) & \
                      (df['close'] >= df['support_1'] * 0.995)
        
        # Price near resistance (within 0.5%)
        near_resistance = (df['close'] >= df['resistance_1'] * 0.995) & \
                         (df['close'] <= df['resistance_1'] * 1.005)
        
        signal[near_support] = 1
        signal[near_resistance] = -1
        
        return signal
    
    def get_composite_signal(self, signals: Dict[str, pd.Series]) -> pd.Series:
        """Combine all signals into a composite signal"""
        composite = pd.Series(0, index=signals[list(signals.keys())[0]].index)
        
        # Weight different signal types
        trend_weight = 0.3
        momentum_weight = 0.25
        volatility_weight = 0.2
        volume_weight = 0.15
        support_resistance_weight = 0.1
        
        # Trend signals
        trend_signals = ['ema_trend', 'macd_signal', 'ichimoku_signal']
        for signal_name in trend_signals:
            if signal_name in signals:
                composite += signals[signal_name] * trend_weight / len(trend_signals)
        
        # Momentum signals
        momentum_signals = ['rsi_signal', 'stochastic_signal', 'cci_signal']
        for signal_name in momentum_signals:
            if signal_name in signals:
                composite += signals[signal_name] * momentum_weight / len(momentum_signals)
        
        # Volatility signals
        volatility_signals = ['bollinger_signal', 'keltner_signal']
        for signal_name in volatility_signals:
            if signal_name in signals:
                composite += signals[signal_name] * volatility_weight / len(volatility_signals)
        
        # Volume signals
        volume_signals = ['volume_signal', 'mfi_signal']
        for signal_name in volume_signals:
            if signal_name in signals:
                composite += signals[signal_name] * volume_weight / len(volume_signals)
        
        # Support/Resistance signals
        if 'support_resistance_signal' in signals:
            composite += signals['support_resistance_signal'] * support_resistance_weight
        
        # Normalize to -1 to 1 range
        composite = np.clip(composite, -1, 1)
        
        return composite