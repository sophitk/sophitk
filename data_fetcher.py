import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import config

class CryptoDataFetcher:
    """Fetch cryptocurrency data from multiple sources"""
    
    def __init__(self):
        self.binance = None
        self.setup_binance()
        
    def setup_binance(self):
        """Setup Binance API connection"""
        try:
            if config.BINANCE_API_KEY and config.BINANCE_SECRET_KEY:
                self.binance = ccxt.binance({
                    'apiKey': config.BINANCE_API_KEY,
                    'secret': config.BINANCE_SECRET_KEY,
                    'sandbox': False,
                    'enableRateLimit': True
                })
            else:
                # Use public API without authentication
                self.binance = ccxt.binance({
                    'enableRateLimit': True
                })
        except Exception as e:
            print(f"Error setting up Binance: {e}")
            self.binance = None
    
    def get_binance_data(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        """Fetch data from Binance"""
        try:
            if not self.binance:
                return pd.DataFrame()
            
            # Convert symbol format (BTC/USDT -> BTCUSDT)
            binance_symbol = symbol.replace('/', '')
            
            # Fetch OHLCV data
            ohlcv = self.binance.fetch_ohlcv(binance_symbol, timeframe, limit=limit)
            
            if not ohlcv:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching Binance data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_yahoo_data(self, symbol: str, period: str = "30d", interval: str = "1h") -> pd.DataFrame:
        """Fetch data from Yahoo Finance"""
        try:
            # Convert symbol format (BTC/USDT -> BTC-USD)
            yahoo_symbol = symbol.replace('/', '-')
            
            # Get ticker data
            ticker = yf.Ticker(yahoo_symbol)
            
            # Fetch historical data
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return pd.DataFrame()
            
            # Rename columns to match standard format
            df.columns = [col.lower() for col in df.columns]
            
            return df
            
        except Exception as e:
            print(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_coinbase_data(self, symbol: str, timeframe: str, limit: int = 300) -> pd.DataFrame:
        """Fetch data from Coinbase Pro API"""
        try:
            # Convert symbol format (BTC/USDT -> BTC-USD)
            coinbase_symbol = symbol.replace('USDT', 'USD')
            
            # Coinbase Pro API endpoint
            base_url = "https://api.pro.coinbase.com"
            endpoint = f"/products/{coinbase_symbol}/candles"
            
            # Convert timeframe to granularity
            granularity_map = {
                '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
                '1h': 3600, '4h': 14400, '1d': 86400
            }
            
            granularity = granularity_map.get(timeframe, 3600)
            
            # Calculate start time
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=limit * granularity / 3600)
            
            params = {
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'granularity': granularity
            }
            
            response = requests.get(f"{base_url}{endpoint}", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            
            # Convert to float
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            return df
            
        except Exception as e:
            print(f"Error fetching Coinbase data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_data(self, symbol: str, timeframe: str, source: str = 'binance', limit: int = 500) -> pd.DataFrame:
        """Get data from specified source"""
        if source.lower() == 'binance':
            return self.get_binance_data(symbol, timeframe, limit)
        elif source.lower() == 'yahoo':
            return self.get_yahoo_data(symbol, period="30d", interval=timeframe)
        elif source.lower() == 'coinbase':
            return self.get_coinbase_data(symbol, timeframe, limit)
        else:
            print(f"Unknown data source: {source}")
            return pd.DataFrame()
    
    def get_multiple_timeframes(self, symbol: str, timeframes: List[str], 
                               source: str = 'binance', limit: int = 500) -> Dict[str, pd.DataFrame]:
        """Get data for multiple timeframes"""
        data = {}
        
        for tf in timeframes:
            print(f"Fetching {symbol} data for {tf} timeframe...")
            df = self.get_data(symbol, tf, source, limit)
            
            if not df.empty:
                data[tf] = df
                print(f"Successfully fetched {len(df)} candles for {tf}")
            else:
                print(f"Failed to fetch data for {tf}")
            
            # Rate limiting
            time.sleep(0.1)
        
        return data
    
    def get_realtime_data(self, symbol: str, timeframe: str = '1m') -> pd.DataFrame:
        """Get real-time data for live trading"""
        try:
            if not self.binance:
                return pd.DataFrame()
            
            # Convert symbol format
            binance_symbol = symbol.replace('/', '')
            
            # Get latest ticker
            ticker = self.binance.fetch_ticker(binance_symbol)
            
            # Get recent OHLCV
            ohlcv = self.binance.fetch_ohlcv(binance_symbol, timeframe, limit=1)
            
            if not ohlcv:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return pd.DataFrame()
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality"""
        if df.empty:
            return False
        
        # Check for required columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            return False
        
        # Check for missing values
        if df.isnull().any().any():
            return False
        
        # Check for zero or negative prices
        if (df[['open', 'high', 'low', 'close']] <= 0).any().any():
            return False
        
        # Check for logical price relationships
        if not ((df['low'] <= df['open']) & (df['low'] <= df['close']) & 
                (df['high'] >= df['open']) & (df['high'] >= df['close'])).all():
            return False
        
        return True
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data for analysis"""
        if df.empty:
            return df
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Sort by timestamp
        df = df.sort_index()
        
        # Forward fill missing values (if any)
        df = df.fillna(method='ffill')
        
        # Remove rows with still missing values
        df = df.dropna()
        
        # Ensure volume is positive
        df['volume'] = df['volume'].abs()
        
        return df
    
    def resample_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Resample data to different timeframe"""
        if df.empty:
            return df
        
        # Convert timeframe to pandas offset
        timeframe_map = {
            '1m': '1T', '5m': '5T', '15m': '15T', '30m': '30T',
            '1h': '1H', '4h': '4H', '1d': 'D'
        }
        
        pandas_timeframe = timeframe_map.get(timeframe, '1H')
        
        # Resample
        resampled = df.resample(pandas_timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        return resampled.dropna()
    
    def get_market_info(self, symbol: str) -> Dict:
        """Get market information for a symbol"""
        try:
            if not self.binance:
                return {}
            
            binance_symbol = symbol.replace('/', '')
            
            # Get ticker
            ticker = self.binance.fetch_ticker(binance_symbol)
            
            # Get order book
            order_book = self.binance.fetch_order_book(binance_symbol, limit=10)
            
            market_info = {
                'symbol': symbol,
                'last_price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low'],
                'volume_24h': ticker['baseVolume'],
                'change_24h': ticker['percentage'],
                'bid_depth': sum([bid[1] for bid in order_book['bids'][:5]]),
                'ask_depth': sum([ask[1] for ask in order_book['asks'][:5]]),
                'spread': ticker['ask'] - ticker['bid'] if ticker['ask'] and ticker['bid'] else 0
            }
            
            return market_info
            
        except Exception as e:
            print(f"Error fetching market info: {e}")
            return {}