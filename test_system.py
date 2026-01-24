#!/usr/bin/env python3
"""
Test script to verify the Cryptocurrency Trading System components
"""

import sys
import traceback

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        import config
        print("✅ config.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config.py: {e}")
        return False
    
    try:
        from indicators import CryptoIndicators
        print("✅ indicators.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import indicators.py: {e}")
        return False
    
    try:
        from strategy import CryptoTradingStrategy
        print("✅ strategy.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import strategy.py: {e}")
        return False
    
    try:
        from data_fetcher import CryptoDataFetcher
        print("✅ data_fetcher.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import data_fetcher.py: {e}")
        return False
    
    try:
        from backtester import CryptoBacktester
        print("✅ backtester.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import backtester.py: {e}")
        return False
    
    return True

def test_config():
    """Test configuration values"""
    print("\n⚙️  Testing configuration...")
    
    try:
        import config
        
        # Check required config values
        required_configs = [
            'SYMBOLS', 'TIMEFRAMES', 'INITIAL_CAPITAL', 'POSITION_SIZE',
            'STOP_LOSS_PERCENT', 'TAKE_PROFIT_PERCENT', 'MAX_OPEN_TRADES'
        ]
        
        for config_name in required_configs:
            if hasattr(config, config_name):
                value = getattr(config, config_name)
                print(f"✅ {config_name}: {value}")
            else:
                print(f"❌ Missing config: {config_name}")
                return False
        
        print(f"✅ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_indicators():
    """Test indicators module"""
    print("\n📊 Testing indicators module...")
    
    try:
        import pandas as pd
        import numpy as np
        from indicators import CryptoIndicators
        
        # Create sample data
        dates = pd.date_range('2024-01-01', periods=100, freq='1h')
        sample_data = pd.DataFrame({
            'open': np.random.uniform(40000, 50000, 100),
            'high': np.random.uniform(40000, 50000, 100),
            'low': np.random.uniform(40000, 50000, 100),
            'close': np.random.uniform(40000, 50000, 100),
            'volume': np.random.uniform(1000, 5000, 100)
        }, index=dates)
        
        # Ensure high >= low and high >= close >= low
        sample_data['high'] = sample_data[['open', 'close', 'high']].max(axis=1)
        sample_data['low'] = sample_data[['open', 'close', 'low']].min(axis=1)
        
        # Test indicators
        indicators = CryptoIndicators()
        df_with_indicators = indicators.calculate_all_indicators(sample_data)
        
        # Check if indicators were added
        expected_indicators = ['rsi', 'macd', 'ema_9', 'bb_upper', 'atr', 'vwap']
        for indicator in expected_indicators:
            if indicator in df_with_indicators.columns:
                print(f"✅ {indicator} calculated successfully")
            else:
                print(f"❌ {indicator} not found")
                return False
        
        # Test signal generation
        signals = indicators.generate_signals(df_with_indicators)
        composite_signal = indicators.get_composite_signal(signals)
        
        if not composite_signal.empty:
            print("✅ Signal generation successful")
        else:
            print("❌ Signal generation failed")
            return False
        
        print(f"✅ Indicators test passed")
        return True
        
    except Exception as e:
        print(f"❌ Indicators test failed: {e}")
        traceback.print_exc()
        return False

def test_strategy():
    """Test strategy module"""
    print("\n🎯 Testing strategy module...")
    
    try:
        import pandas as pd
        import numpy as np
        from strategy import CryptoTradingStrategy
        
        # Create sample data
        dates = pd.date_range('2024-01-01', periods=100, freq='1h')
        sample_data = pd.DataFrame({
            'open': np.random.uniform(40000, 50000, 100),
            'high': np.random.uniform(40000, 50000, 100),
            'low': np.random.uniform(40000, 50000, 100),
            'close': np.random.uniform(40000, 50000, 100),
            'volume': np.random.uniform(1000, 5000, 100)
        }, index=dates)
        
        # Ensure high >= low and high >= close >= low
        sample_data['high'] = sample_data[['open', 'close', 'high']].max(axis=1)
        sample_data['low'] = sample_data[['open', 'close', 'low']].min(axis=1)
        
        # Test strategy
        strategy = CryptoTradingStrategy()
        analysis = strategy.analyze_market(sample_data)
        
        # Check analysis components
        required_components = ['data', 'signals', 'composite_signal', 'entry_signals', 'exit_signals', 'market_conditions']
        for component in required_components:
            if component in analysis:
                print(f"✅ {component} generated successfully")
            else:
                print(f"❌ Missing component: {component}")
                return False
        
        # Test trading recommendation
        recommendation = strategy.get_trading_recommendation(analysis)
        if 'action' in recommendation:
            print(f"✅ Trading recommendation generated: {recommendation['action']}")
        else:
            print("❌ Trading recommendation failed")
            return False
        
        print(f"✅ Strategy test passed")
        return True
        
    except Exception as e:
        print(f"❌ Strategy test failed: {e}")
        traceback.print_exc()
        return False

def test_data_fetcher():
    """Test data fetcher module"""
    print("\n📡 Testing data fetcher module...")
    
    try:
        from data_fetcher import CryptoDataFetcher
        
        # Test initialization
        data_fetcher = CryptoDataFetcher()
        print("✅ Data fetcher initialized successfully")
        
        # Test data validation
        import pandas as pd
        import numpy as np
        
        # Valid data
        valid_data = pd.DataFrame({
            'open': [40000, 41000, 42000],
            'high': [41000, 42000, 43000],
            'low': [39000, 40000, 41000],
            'close': [41000, 42000, 43000],
            'volume': [1000, 1100, 1200]
        })
        
        if data_fetcher.validate_data(valid_data):
            print("✅ Data validation passed")
        else:
            print("❌ Data validation failed")
            return False
        
        # Test data cleaning
        cleaned_data = data_fetcher.clean_data(valid_data)
        if not cleaned_data.empty:
            print("✅ Data cleaning successful")
        else:
            print("❌ Data cleaning failed")
            return False
        
        print(f"✅ Data fetcher test passed")
        return True
        
    except Exception as e:
        print(f"❌ Data fetcher test failed: {e}")
        traceback.print_exc()
        return False

def test_backtester():
    """Test backtester module"""
    print("\n📊 Testing backtester module...")
    
    try:
        from backtester import CryptoBacktester
        
        # Test initialization
        backtester = CryptoBacktester(initial_capital=10000)
        print("✅ Backtester initialized successfully")
        
        # Test reset
        backtester.reset()
        print("✅ Backtester reset successful")
        
        print(f"✅ Backtester test passed")
        return True
        
    except Exception as e:
        print(f"❌ Backtester test failed: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'yfinance', 
        'ta', 'sklearn', 'plotly', 'dash', 'ccxt', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install missing packages with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def main():
    """Run all tests"""
    print("🧪 CRYPTOCURRENCY TRADING SYSTEM - SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        test_dependencies,
        test_imports,
        test_config,
        test_indicators,
        test_strategy,
        test_data_fetcher,
        test_backtester
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test failed: {test.__name__}")
        except Exception as e:
            print(f"❌ Test crashed: {test.__name__} - {e}")
            traceback.print_exc()
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n💡 To run the system:")
        print("   Interactive mode: python main.py")
        print("   Examples: python example.py")
        print("   Command line: python main.py --help")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)