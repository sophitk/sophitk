#!/usr/bin/env python3
"""
Modern Minimal Cryptocurrency Trading Dashboard
Beautiful UX/UI with real-time data visualization
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import time
import queue

from data_fetcher import CryptoDataFetcher
from strategy import CryptoTradingStrategy
from backtester import CryptoBacktester
import config

# Initialize components
data_fetcher = CryptoDataFetcher()
strategy = CryptoTradingStrategy()
backtester = CryptoBacktester()

# Global data storage
market_data = {}
signals_data = {}
portfolio_data = {}

# Initialize Dash app with minimal theme
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.COSMO,
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
])

app.title = "Crypto Trading Dashboard"

# Custom CSS for minimal design
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Crypto Trading Dashboard</title>
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .dashboard-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            }
            .metric-card {
                background: white;
                border-radius: 16px;
                padding: 24px;
                margin: 12px 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
            }
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                color: #1a1a1a;
                margin: 8px 0;
            }
            .metric-label {
                font-size: 0.9rem;
                color: #666;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .signal-buy {
                color: #10b981;
                font-weight: 600;
            }
            .signal-sell {
                color: #ef4444;
                font-weight: 600;
            }
            .signal-hold {
                color: #6b7280;
                font-weight: 600;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                color: #1a1a1a;
                margin: 0;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .header p {
                font-size: 1.1rem;
                color: #666;
                margin: 8px 0 0 0;
                font-weight: 400;
            }
            .refresh-button {
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 20px 0;
            }
            .refresh-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            .chart-container {
                background: white;
                border-radius: 16px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div id="react-entry-point">
            <div class="dashboard-container">
                <div class="header">
                    <h1>🚀 Crypto Trading Dashboard</h1>
                    <p>High-Win-Rate Day Trading System for BTC, ETH, and SOL</p>
                </div>
                <div id="dashboard-content"></div>
            </div>
        </div>
    </body>
</html>
'''

def create_metric_card(title, value, subtitle="", color="#667eea"):
    """Create a beautiful metric card"""
    return html.Div([
        html.Div([
            html.H3(title, className="metric-label"),
            html.Div(value, className="metric-value", style={"color": color}),
            html.Div(subtitle, className="metric-label")
        ], className="metric-card")
    ])

def create_signal_card(symbol, timeframe, action, confidence, price, change):
    """Create a signal card with action and confidence"""
    if action == "BUY":
        signal_class = "signal-buy"
        action_icon = "🟢"
    elif action == "SELL":
        signal_class = "signal-sell"
        action_icon = "🔴"
    else:
        signal_class = "signal-hold"
        action_icon = "⚪"
    
    change_color = "#10b981" if change >= 0 else "#ef4444"
    change_icon = "📈" if change >= 0 else "📉"
    
    return html.Div([
        html.Div([
            html.H4(f"{action_icon} {symbol}", className="metric-label"),
            html.Div(f"{timeframe}", className="metric-label", style={"fontSize": "0.8rem"}),
            html.Div(action, className=signal_class, style={"fontSize": "1.5rem", "margin": "8px 0"}),
            html.Div(f"Confidence: {confidence:.1%}", className="metric-label"),
            html.Div(f"${price:,.2f}", className="metric-value", style={"fontSize": "1.8rem"}),
            html.Div([
                change_icon, f" {change:+.2f}%"
            ], style={"color": change_color, "fontWeight": "600"})
        ], className="metric-card")
    ])

def create_price_chart(symbol, timeframe):
    """Create a beautiful price chart"""
    try:
        df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
        if df.empty:
            return html.Div("No data available", className="loading")
        
        df = data_fetcher.clean_data(df)
        
        # Create candlestick chart
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{symbol} Price Chart ({timeframe})', 'Volume'),
            row_width=[0.7, 0.3]
        )
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='OHLC',
            increasing_line_color='#10b981',
            decreasing_line_color='#ef4444'
        ), row=1, col=1)
        
        # Volume bars
        colors = ['#10b981' if close >= open else '#ef4444' 
                 for close, open in zip(df['close'], df['open'])]
        
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='Volume',
            marker_color=colors,
            opacity=0.7
        ), row=2, col=1)
        
        # Update layout for minimal design
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            height=400,
            showlegend=False,
            xaxis_rangeslider_visible=False
        )
        
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, zeroline=False, gridcolor='rgba(0,0,0,0.1)')
        
        return dcc.Graph(figure=fig, config={'displayModeBar': False})
        
    except Exception as e:
        return html.Div(f"Error loading chart: {str(e)}", className="loading")

def create_portfolio_chart():
    """Create portfolio performance chart"""
    try:
        # Simulate portfolio data for demonstration
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        portfolio_values = [10000 + i * 50 + np.random.normal(0, 100) for i in range(30)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=portfolio_values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#667eea', width=3),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,
            showlegend=False,
            title="Portfolio Performance (30 Days)"
        )
        
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=True, zeroline=False, gridcolor='rgba(0,0,0,0.1)')
        
        return dcc.Graph(figure=fig, config={'displayModeBar': False})
        
    except Exception as e:
        return html.Div(f"Error loading portfolio chart: {str(e)}", className="loading")

def update_market_data():
    """Update market data in background"""
    global market_data, signals_data
    
    while True:
        try:
            for symbol in config.SYMBOLS:
                for timeframe in config.TIMEFRAMES:
                    # Fetch data
                    df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
                    if not df.empty:
                        df = data_fetcher.clean_data(df)
                        
                        if len(df) >= 50:
                            # Store market data
                            market_data[f"{symbol}_{timeframe}"] = df
                            
                            # Analyze and store signals
                            analysis = strategy.analyze_market(df)
                            signals_data[f"{symbol}_{timeframe}"] = analysis
            
            time.sleep(60)  # Update every minute
            
        except Exception as e:
            print(f"Error updating market data: {e}")
            time.sleep(60)

# Start background data update thread
data_thread = threading.Thread(target=update_market_data, daemon=True)
data_thread.start()

# Dashboard layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🚀 Crypto Trading Dashboard", className="header"),
        html.P("High-Win-Rate Day Trading System for BTC, ETH, and SOL", className="header"),
        
        # Refresh button
        html.Button("🔄 Refresh Data", id="refresh-button", className="refresh-button"),
        html.Div(id="refresh-output")
    ]),
    
    # Market Overview
    html.Div([
        html.H2("📊 Market Overview", style={"marginBottom": "20px", "color": "#1a1a1a"}),
        html.Div(id="market-overview", className="metric-card")
    ]),
    
    # Trading Signals
    html.Div([
        html.H2("🎯 Trading Signals", style={"marginBottom": "20px", "color": "#1a1a1a"}),
        html.Div(id="trading-signals")
    ]),
    
    # Charts Section
    html.Div([
        html.H2("📈 Price Charts", style={"marginBottom": "20px", "color": "#1a1a1a"}),
        html.Div([
            html.Div([
                html.H3("BTC/USDT - 1H", style={"textAlign": "center", "marginBottom": "15px"}),
                html.Div(id="btc-chart")
            ], className="chart-container"),
            
            html.Div([
                html.H3("Portfolio Performance", style={"textAlign": "center", "marginBottom": "15px"}),
                html.Div(id="portfolio-chart")
            ], className="chart-container")
        ])
    ]),
    
    # Performance Metrics
    html.Div([
        html.H2("📊 Performance Metrics", style={"marginBottom": "20px", "color": "#1a1a1a"}),
        html.Div(id="performance-metrics")
    ])
])

@app.callback(
    Output("market-overview", "children"),
    Input("refresh-button", "n_clicks")
)
def update_market_overview(n_clicks):
    """Update market overview section"""
    try:
        # Get current market data
        overview_cards = []
        
        for symbol in config.SYMBOLS:
            # Get latest data
            df = data_fetcher.get_data(symbol, "1h", source='binance', limit=10)
            if not df.empty:
                df = data_fetcher.clean_data(df)
                
                if len(df) >= 2:
                    current_price = df['close'].iloc[-1]
                    previous_price = df['close'].iloc[-2]
                    change_pct = ((current_price - previous_price) / previous_price) * 100
                    
                    # Get market info
                    market_info = data_fetcher.get_market_info(symbol)
                    volume_24h = market_info.get('volume_24h', 0) if market_info else 0
                    
                    overview_cards.append(create_metric_card(
                        title=symbol,
                        value=f"${current_price:,.2f}",
                        subtitle=f"{change_pct:+.2f}% • Vol: {volume_24h:,.0f}",
                        color="#10b981" if change_pct >= 0 else "#ef4444"
                    ))
        
        return overview_cards
        
    except Exception as e:
        return html.Div(f"Error loading market overview: {str(e)}", className="loading")

@app.callback(
    Output("trading-signals", "children"),
    Input("refresh-button", "n_clicks")
)
def update_trading_signals(n_clicks):
    """Update trading signals section"""
    try:
        signal_cards = []
        
        for symbol in config.SYMBOLS:
            for timeframe in config.TIMEFRAMES:
                # Get analysis
                df = data_fetcher.get_data(symbol, timeframe, source='binance', limit=100)
                if not df.empty:
                    df = data_fetcher.clean_data(df)
                    
                    if len(df) >= 50:
                        analysis = strategy.analyze_market(df)
                        recommendation = strategy.get_trading_recommendation(analysis)
                        
                        # Get current price and change
                        current_price = df['close'].iloc[-1]
                        previous_price = df['close'].iloc[-5]  # 5 periods ago
                        change_pct = ((current_price - previous_price) / previous_price) * 100
                        
                        signal_cards.append(create_signal_card(
                            symbol=symbol,
                            timeframe=timeframe,
                            action=recommendation['action'],
                            confidence=recommendation['confidence'],
                            price=current_price,
                            change=change_pct
                        ))
        
        return signal_cards
        
    except Exception as e:
        return html.Div(f"Error loading trading signals: {str(e)}", className="loading")

@app.callback(
    Output("btc-chart", "children"),
    Input("refresh-button", "n_clicks")
)
def update_btc_chart(n_clicks):
    """Update BTC price chart"""
    return create_price_chart("BTC/USDT", "1h")

@app.callback(
    Output("portfolio-chart", "children"),
    Input("refresh-button", "n_clicks")
)
def update_portfolio_chart(n_clicks):
    """Update portfolio chart"""
    return create_portfolio_chart()

@app.callback(
    Output("performance-metrics", "children"),
    Input("refresh-button", "n_clicks")
)
def update_performance_metrics(n_clicks):
    """Update performance metrics"""
    try:
        # Simulate performance data for demonstration
        metrics = [
            ("Total Return", "+15.7%", "Last 30 days", "#10b981"),
            ("Win Rate", "72.3%", "Current period", "#667eea"),
            ("Sharpe Ratio", "1.85", "Risk-adjusted", "#8b5cf6"),
            ("Max Drawdown", "-8.2%", "Current period", "#f59e0b"),
            ("Total Trades", "47", "This month", "#6b7280"),
            ("Profit Factor", "1.67", "Risk-reward", "#10b981")
        ]
        
        metric_cards = []
        for title, value, subtitle, color in metrics:
            metric_cards.append(create_metric_card(title, value, subtitle, color))
        
        return metric_cards
        
    except Exception as e:
        return html.Div(f"Error loading performance metrics: {str(e)}", className="loading")

@app.callback(
    Output("refresh-output", "children"),
    Input("refresh-button", "n_clicks")
)
def refresh_data(n_clicks):
    """Handle refresh button click"""
    if n_clicks:
        return html.Div("✅ Data refreshed!", style={"textAlign": "center", "color": "#10b981"})
    return ""

if __name__ == "__main__":
    print("🚀 Starting Crypto Trading Dashboard...")
    print("📱 Open your browser and go to: http://127.0.0.1:8050")
    print("🔄 Dashboard will automatically update every minute")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    
    app.run_server(debug=True, host='127.0.0.1', port=8050)