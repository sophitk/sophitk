#!/usr/bin/env python3
"""
Demo script to showcase the beautiful UX/UI features
of the Cryptocurrency Trading System
"""

import time
import sys
from terminal_ui import *

def demo_terminal_ui():
    """Demonstrate the beautiful terminal UI"""
    clear_screen()
    print_ascii_art()
    
    print_header("Terminal UI Demo", "Beautiful colors, progress bars, and animations")
    
    # Market overview demo
    print_section("Market Overview")
    print_market_card("BTC/USDT", 43250.50, 2.45, 1234567, "Bullish")
    print_market_card("ETH/USDT", 2650.75, -1.23, 987654, "Bearish")
    print_market_card("SOL/USDT", 98.45, 5.67, 456789, "Bullish")
    
    # Trading signals demo
    print_section("Trading Signals")
    print_signal("BUY", 0.75, 0.85)
    print_signal("SELL", 0.60, 0.70)
    print_signal("HOLD", 0.20, 0.30)
    
    # Performance metrics demo
    print_section("Performance Metrics")
    metrics = {
        "Total Return": "+15.7%",
        "Win Rate": "72.3%",
        "Sharpe Ratio": "1.85",
        "Max Drawdown": "-8.2%",
        "Profit Factor": "1.67",
        "Total Trades": "47"
    }
    print_performance_summary(metrics)
    
    # Progress bar demo
    print_progress_bar(75, 100, title="System Load")
    print_progress_bar(23, 47, title="Completed Trades")
    
    # Table demo
    print_section("Market Data Table")
    headers = ["Symbol", "Price", "Change", "Volume", "Trend"]
    rows = [
        ["BTC/USDT", "$43,250", "+2.45%", "1,234,567", "Bullish"],
        ["ETH/USDT", "$2,650", "-1.23%", "987,654", "Bearish"],
        ["SOL/USDT", "$98.45", "+5.67%", "456,789", "Bullish"]
    ]
    print_table(headers, rows, "Live Market Data")
    
    # Loading animations
    print_section("Loading Animations")
    print_loading_spinner(2, "Fetching market data")
    print_loading_spinner(2, "Analyzing indicators")
    print_loading_spinner(2, "Generating signals")
    
    # Status messages
    print_section("Status Messages")
    print_status("INFO", "System initialized successfully")
    print_status("SUCCESS", "Data updated successfully")
    print_status("WARNING", "High volatility detected")
    print_status("ERROR", "Connection timeout")
    
    # Chart placeholder
    print_section("Chart Placeholders")
    print_chart_placeholder("BTC/USDT Price Chart (1H)")
    print_chart_placeholder("Portfolio Performance")
    
    print_footer()

def demo_web_dashboard():
    """Demonstrate web dashboard features"""
    print_header("Web Dashboard Demo", "Modern web interface features")
    
    print_section("Dashboard Features")
    
    features = [
        "🎨 Beautiful minimal design with gradient backgrounds",
        "📊 Interactive candlestick charts with Plotly",
        "🔄 Real-time data updates every minute",
        "📱 Responsive design for mobile devices",
        "🎯 Live trading signals with confidence levels",
        "📈 Portfolio performance visualization",
        "⚡ Fast and smooth animations",
        "🌙 Dark mode support",
        "♿ Accessibility features",
        "📱 Mobile-optimized interface"
    ]
    
    for feature in features:
        print_colored(f"   {feature}", Colors.SUCCESS)
        time.sleep(0.3)
    
    print()
    print_colored("🚀 To launch the web dashboard:", Colors.PRIMARY, bold=True)
    print_colored("   1. Run: python dashboard.py", Colors.INFO)
    print_colored("   2. Open browser to: http://127.0.0.1:8050", Colors.INFO)
    print_colored("   3. Enjoy the beautiful interface!", Colors.SUCCESS)
    
    print()
    print_colored("💡 The dashboard includes:", Colors.PURPLE)
    print_colored("   • Market overview cards", Colors.INFO)
    print_colored("   • Trading signal displays", Colors.INFO)
    print_colored("   • Interactive price charts", Colors.INFO)
    print_colored("   • Performance metrics", Colors.INFO)
    print_colored("   • Portfolio analysis", Colors.INFO)

def demo_terminal_colors():
    """Demonstrate all available colors"""
    print_header("Color Palette Demo", "All available terminal colors")
    
    colors = [
        ("Primary", Colors.PRIMARY),
        ("Success", Colors.SUCCESS),
        ("Warning", Colors.WARNING),
        ("Error", Colors.ERROR),
        ("Info", Colors.INFO),
        ("Purple", Colors.PURPLE),
        ("Pink", Colors.PINK),
        ("Orange", Colors.ORANGE),
        ("Teal", Colors.TEAL),
        ("Light Gray", Colors.LIGHT_GRAY),
        ("Gray", Colors.GRAY),
        ("Dark Gray", Colors.DARK_GRAY)
    ]
    
    for name, color in colors:
        print_colored(f"   {name}: This is sample text in {name.lower()} color", color)
        time.sleep(0.2)
    
    print()
    print_colored("🎨 All colors support bold, italic, and underline styles", Colors.PURPLE)

def demo_animations():
    """Demonstrate loading animations"""
    print_header("Animation Demo", "Smooth loading animations and effects")
    
    print_section("Loading Spinners")
    print_loading_spinner(3, "Processing data")
    print_loading_spinner(3, "Calculating indicators")
    print_loading_spinner(3, "Generating report")
    
    print_section("Loading Animation")
    print_loading_animation("Analyzing market", 3)
    
    print_section("Progress Bars")
    for i in range(0, 101, 25):
        print_progress_bar(i, 100, title=f"Task {i//25 + 1}")
        time.sleep(0.5)

def main():
    """Run all UI demos"""
    print_ascii_art()
    
    demos = [
        ("Terminal UI", demo_terminal_ui),
        ("Web Dashboard", demo_web_dashboard),
        ("Color Palette", demo_terminal_colors),
        ("Animations", demo_animations)
    ]
    
    while True:
        print_header("UI Demo Menu", "Choose a demo to run")
        
        for i, (name, _) in enumerate(demos, 1):
            print_colored(f"{i}. {name}", Colors.SUCCESS)
        print_colored("0. Exit", Colors.ERROR)
        
        try:
            choice = input(f"\n{Colors.PRIMARY}Enter your choice (0-{len(demos)}): {Colors.RESET}").strip()
            
            if choice == '0':
                print_footer()
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(demos):
                clear_screen()
                demos[choice_num - 1][1]()
                input(f"\n{Colors.INFO}Press Enter to continue...{Colors.RESET}")
                clear_screen()
            else:
                print_colored("❌ Invalid choice. Please enter a number between 0 and 4.", Colors.ERROR)
                
        except ValueError:
            print_colored("❌ Please enter a valid number.", Colors.ERROR)
        except KeyboardInterrupt:
            print_footer()
            break
        except Exception as e:
            print_error(e, "Demo execution")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_footer()
        sys.exit(0)