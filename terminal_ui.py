#!/usr/bin/env python3
"""
Beautiful Terminal UI Enhancement Module
Modern colors, progress bars, and formatting for the crypto trading system
"""

import time
import sys
import os
from datetime import datetime

# Color codes for beautiful terminal output
class Colors:
    # Primary colors
    PRIMARY = "\033[38;2;102;126;234m"      # Blue
    SUCCESS = "\033[38;2;16;185;129m"       # Green
    WARNING = "\033[38;2;245;158;11m"       # Yellow
    ERROR = "\033[38;2;239;68;68m"          # Red
    INFO = "\033[38;2;59;130;246m"          # Blue
    
    # Secondary colors
    PURPLE = "\033[38;2;139;92;246m"        # Purple
    PINK = "\033[38;2;236;72;153m"          # Pink
    ORANGE = "\033[38;2;249;115;22m"        # Orange
    TEAL = "\033[38;2;20;184;166m"          # Teal
    
    # Grays
    LIGHT_GRAY = "\033[38;2;156;163;175m"   # Light gray
    GRAY = "\033[38;2;107;114;128m"         # Gray
    DARK_GRAY = "\033[38;2;75;85;99m"       # Dark gray
    
    # Reset
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

def print_colored(text, color=Colors.PRIMARY, bold=False, end="\n"):
    """Print colored text"""
    style = Colors.BOLD if bold else ""
    print(f"{style}{color}{text}{Colors.RESET}", end=end)

def print_header(title, subtitle=""):
    """Print a beautiful header"""
    width = 80
    print()
    print_colored("╔" + "═" * (width - 2) + "╗", Colors.PRIMARY)
    print_colored("║" + title.center(width - 2) + "║", Colors.PRIMARY, bold=True)
    if subtitle:
        print_colored("║" + subtitle.center(width - 2) + "║", Colors.PRIMARY)
    print_colored("╚" + "═" * (width - 2) + "╝", Colors.PRIMARY)
    print()

def print_section(title, color=Colors.SUCCESS):
    """Print a section header"""
    print()
    print_colored(f"📊 {title}", color, bold=True)
    print_colored("─" * (len(title) + 4), color)
    print()

def print_subsection(title, color=Colors.INFO):
    """Print a subsection header"""
    print_colored(f"  ⏰ {title}", color)
    print_colored("    " + "─" * len(title), color)

def print_metric(label, value, color=Colors.PRIMARY, unit=""):
    """Print a metric with beautiful formatting"""
    if isinstance(value, float):
        if abs(value) >= 1:
            formatted_value = f"{value:,.2f}"
        else:
            formatted_value = f"{value:.4f}"
    else:
        formatted_value = str(value)
    
    print_colored(f"   {label}: {formatted_value}{unit}", color)

def print_signal(signal_type, strength, confidence):
    """Print a trading signal with beautiful formatting"""
    if signal_type == "BUY":
        color = Colors.SUCCESS
        icon = "🟢"
        action = "BUY"
    elif signal_type == "SELL":
        color = Colors.ERROR
        icon = "🔴"
        action = "SELL"
    else:
        color = Colors.GRAY
        icon = "⚪"
        action = "HOLD"
    
    print_colored(f"   {icon} {action}", color, bold=True)
    print_colored(f"   📊 Signal Strength: {strength:.1%}", Colors.INFO)
    print_colored(f"   🎯 Confidence: {confidence:.1%}", Colors.PURPLE)

def print_progress_bar(current, total, width=50, title="Progress"):
    """Print a beautiful progress bar"""
    percentage = current / total if total > 0 else 0
    filled_width = int(width * percentage)
    bar = "█" * filled_width + "░" * (width - filled_width)
    
    print_colored(f"\n{title}:", Colors.INFO)
    print(f"   [{bar}] {percentage:.1%} ({current}/{total})")
    print()

def print_loading_spinner(duration=3, message="Loading"):
    """Print a loading spinner"""
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    print_colored(f"\n{message}...", Colors.INFO, end="")
    
    for i in range(duration * 10):
        print(f"\r{message}... {spinner[i % len(spinner)]}", end="")
        time.sleep(0.1)
        sys.stdout.flush()
    
    print(f"\r{message}... ✅", end="")
    print()

def print_table(headers, rows, title=""):
    """Print a beautiful table"""
    if title:
        print_colored(f"\n{title}", Colors.INFO, bold=True)
    
    if not rows:
        print_colored("   No data available", Colors.GRAY)
        return
    
    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)
    
    # Print header
    header_line = "   "
    separator_line = "   "
    for i, header in enumerate(headers):
        header_line += f"{header:<{col_widths[i]}}"
        separator_line += "─" * col_widths[i]
        if i < len(headers) - 1:
            header_line += "│"
            separator_line += "┼"
    
    print_colored(header_line, Colors.PRIMARY, bold=True)
    print_colored(separator_line, Colors.PRIMARY)
    
    # Print rows
    for row in rows:
        row_line = "   "
        for i, cell in enumerate(row):
            if i < len(row):
                row_line += f"{str(cell):<{col_widths[i]}}"
            if i < len(row) - 1:
                row_line += "│"
        print(row_line)
    
    print()

def print_status(status, message, color=Colors.SUCCESS):
    """Print a status message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print_colored(f"[{timestamp}] {status}: {message}", color)

def print_error(error, context=""):
    """Print an error message beautifully"""
    print_colored(f"\n❌ ERROR{': ' + context if context else ''}", Colors.ERROR, bold=True)
    print_colored(f"   {str(error)}", Colors.ERROR)
    print()

def print_success(message):
    """Print a success message"""
    print_colored(f"\n✅ {message}", Colors.SUCCESS, bold=True)

def print_warning(message):
    """Print a warning message"""
    print_colored(f"\n⚠️  {message}", Colors.WARNING, bold=True)

def print_info(message):
    """Print an info message"""
    print_colored(f"\nℹ️  {message}", Colors.INFO)

def print_divider(char="─", length=60, color=Colors.GRAY):
    """Print a divider line"""
    print_colored(char * length, color)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    """Print ASCII art logo"""
    logo = """
\033[38;2;102;126;234m
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                    🚀 CRYPTOCURRENCY TRADING SYSTEM 🚀                     ║
    ║                                                                              ║
    ║  High-Win-Rate Day Trading Strategy for BTC, ETH, and SOL                  ║
    ║  Timeframes: 30m and 1H                                                    ║
    ║  Features: Multi-indicator analysis, backtesting, and live signals         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m
    """
    print(logo)

def print_menu_options(options, title="Menu"):
    """Print menu options beautifully"""
    print_colored(f"\n{title}", Colors.PRIMARY, bold=True)
    print_colored("=" * len(title), Colors.PRIMARY)
    
    for i, option in enumerate(options):
        if i == 0:  # Exit option
            color = Colors.ERROR
        elif "Dashboard" in option:  # Special features
            color = Colors.PURPLE
        else:  # Regular options
            color = Colors.SUCCESS
        
        print_colored(f"{i}. {option}", color)
    
    print_colored("-" * len(title), Colors.PRIMARY)

def print_market_card(symbol, price, change, volume, trend):
    """Print a market data card"""
    change_color = Colors.SUCCESS if change >= 0 else Colors.ERROR
    change_icon = "📈" if change >= 0 else "📉"
    
    print_colored(f"\n📊 {symbol}", Colors.INFO, bold=True)
    print_colored("   " + "─" * (len(symbol) + 4), Colors.INFO)
    print_colored(f"   💰 Price: ${price:,.2f}", Colors.PRIMARY)
    print_colored(f"   {change_icon} Change: {change:+.2f}%", change_color)
    print_colored(f"   📊 Volume: {volume:,.0f}", Colors.TEAL)
    print_colored(f"   📈 Trend: {trend}", Colors.PURPLE)

def print_performance_summary(metrics):
    """Print performance metrics summary"""
    print_section("Performance Summary", Colors.PURPLE)
    
    for metric, value in metrics.items():
        if "Return" in metric or "Win Rate" in metric:
            color = Colors.SUCCESS if value > 0 else Colors.ERROR
        elif "Drawdown" in metric:
            color = Colors.ERROR
        else:
            color = Colors.INFO
        
        print_metric(metric, value, color)

def print_trade_summary(trade):
    """Print a trade summary beautifully"""
    print_colored(f"\n📋 Trade {trade.get('position_id', 'N/A')}", Colors.INFO, bold=True)
    print_colored("   " + "─" * 20, Colors.INFO)
    
    direction_color = Colors.SUCCESS if trade.get('direction') == 'long' else Colors.ERROR
    print_colored(f"   {trade.get('direction', 'N/A').upper()}", direction_color, bold=True)
    
    print_metric("Entry Price", f"${trade.get('entry_price', 0):.2f}", Colors.PRIMARY)
    print_metric("Exit Price", f"${trade.get('exit_price', 0):.2f}", Colors.PRIMARY)
    print_metric("P&L", f"${trade.get('pnl', 0):.2f}", 
                Colors.SUCCESS if trade.get('pnl', 0) > 0 else Colors.ERROR)
    print_metric("P&L %", f"{trade.get('pnl_pct', 0):.2f}%",
                Colors.SUCCESS if trade.get('pnl_pct', 0) > 0 else Colors.ERROR)
    print_metric("Duration", f"{trade.get('duration', 0):.1f} hours", Colors.TEAL)
    print_metric("Exit Reason", trade.get('exit_reason', 'N/A'), Colors.PURPLE)

def print_loading_animation(message="Processing", duration=2):
    """Print a loading animation"""
    frames = [
        "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    ]
    
    print_colored(f"\n{message}", Colors.INFO, end="")
    
    for frame in frames:
        for char in frame:
            print(f"\r{message} {char}", end="")
            time.sleep(duration / len(frames))
            sys.stdout.flush()
    
    print(f"\r{message} ✅", end="")
    print()

def print_chart_placeholder(title, width=60):
    """Print a chart placeholder"""
    print_colored(f"\n📈 {title}", Colors.INFO, bold=True)
    print_colored("   " + "─" * width, Colors.INFO)
    print_colored("   📊 Chart would be displayed here", Colors.GRAY)
    print_colored("   🔄 Use the web dashboard for interactive charts", Colors.PURPLE)
    print_colored("   " + "─" * width, Colors.INFO)

def print_footer():
    """Print a beautiful footer"""
    print()
    print_colored("╔" + "═" * 78 + "╗", Colors.PRIMARY)
    print_colored("║" + "Thank you for using the Cryptocurrency Trading System!".center(78) + "║", Colors.PRIMARY)
    print_colored("║" + "Good luck with your trading! 🚀".center(78) + "║", Colors.PRIMARY)
    print_colored("╚" + "═" * 78 + "╝", Colors.PRIMARY)
    print()

# Example usage
if __name__ == "__main__":
    print_ascii_art()
    
    # Demo of various UI elements
    print_header("Terminal UI Demo", "Beautiful formatting and colors")
    
    print_section("Market Overview")
    print_market_card("BTC/USDT", 43250.50, 2.45, 1234567, "Bullish")
    print_market_card("ETH/USDT", 2650.75, -1.23, 987654, "Bearish")
    
    print_section("Trading Signals")
    print_signal("BUY", 0.75, 0.85)
    print_signal("SELL", 0.60, 0.70)
    
    print_section("Performance Metrics")
    metrics = {
        "Total Return": "+15.7%",
        "Win Rate": "72.3%",
        "Sharpe Ratio": "1.85",
        "Max Drawdown": "-8.2%"
    }
    print_performance_summary(metrics)
    
    print_progress_bar(75, 100, title="System Load")
    
    print_section("Sample Table")
    headers = ["Symbol", "Price", "Change", "Volume"]
    rows = [
        ["BTC/USDT", "$43,250", "+2.45%", "1,234,567"],
        ["ETH/USDT", "$2,650", "-1.23%", "987,654"],
        ["SOL/USDT", "$98.45", "+5.67%", "456,789"]
    ]
    print_table(headers, rows, "Market Data")
    
    print_footer()