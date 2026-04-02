"""
Thndr Guide — Egyptian Exchange Investment Companion
Entry point: wires together data, signals, and UI components.
"""

import time
import pandas as pd
import streamlit as st

from config import THEME_CSS
from data import fetch_history, fetch_info, compute_indicators, fetch_scanner_data
from signals import get_signal
from components import (
    render_topbar,
    render_header,
    render_metrics,
    render_52week_range,
    render_analysis_box,
    render_chart,
    render_company_info,
    render_market_scanner,
    render_disclaimer,
)

# ── Must be the first Streamlit call ─────────────────────────────────────────
st.set_page_config(
    page_title="Thndr Guide",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ── Auto-refresh every 60 seconds ────────────────────────────────────────────
AUTO_REFRESH_INTERVAL = 60  # 60 seconds

# Initialize last refresh time in session state
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# Check if it's time to refresh
current_time = time.time()
time_since_refresh = current_time - st.session_state.last_refresh

if time_since_refresh >= AUTO_REFRESH_INTERVAL:
    st.session_state.last_refresh = current_time
    st.cache_data.clear()
    st.rerun()

# Calculate time until next refresh
time_until_refresh = AUTO_REFRESH_INTERVAL - time_since_refresh
seconds_until = int(time_until_refresh)

# ── Topbar controls ───────────────────────────────────────────────────────────
tickers, period = render_topbar()

ticker = tickers[0] if tickers else "COMI.CA"

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_analysis, tab_scanner = st.tabs(["📈  Stock Analysis", "🔍  Market Scanner"])

# ══════════════════════════════════════════════════════════════════════════════
# Tab 1 — Stock Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tab_analysis:
    if len(tickers) > 1:
        st.info(
            f"📊 Showing detailed analysis for **{ticker}** (first selected ticker). "
            f"Switch to the **Market Scanner** tab to compare all {len(tickers)} selected stocks."
        )
    
    df_raw, error = fetch_history(ticker, period)
    info   = fetch_info(ticker)

    if error:
        st.error(
            f"**{error}**\n\n"
            "EGX tickers require the `.CA` suffix (e.g. `COMI.CA`). "
            "If the ticker is correct, the stock may be delisted or Yahoo Finance may be temporarily unavailable."
        )
        st.stop()

    if df_raw.empty:
        st.error(
            f"**No data found for `{ticker}`.**\n\n"
            "EGX tickers require the `.CA` suffix (e.g. `COMI.CA`). "
            "If the ticker is correct, Yahoo Finance may be temporarily unavailable — try refreshing."
        )
        st.stop()

    df = compute_indicators(df_raw)

    latest     = df.iloc[-1]
    prev_close = df["Close"].iloc[-2] if len(df) > 1 else latest["Close"]

    price        = float(latest["Close"])
    rsi          = float(latest["RSI"])    if pd.notna(latest["RSI"])    else float("nan")
    sma50        = float(latest["SMA50"])  if pd.notna(latest["SMA50"])  else float("nan")
    sma200       = float(latest["SMA200"]) if pd.notna(latest["SMA200"]) else float("nan")
    daily_change = (price - float(prev_close)) / float(prev_close) * 100

    week52_low  = info.get("fiftyTwoWeekLow",  float(df["Low"].min()))
    week52_high = info.get("fiftyTwoWeekHigh", float(df["High"].max()))
    mkt_cap     = info.get("marketCap")
    company_name = info.get("longName", ticker)

    render_header(ticker, company_name, num_tickers=len(tickers))
    render_metrics(price, daily_change, rsi, sma50, mkt_cap)
    render_52week_range(price, week52_low, week52_high)

    signal_label, signal_emoji, signal_color, explanation, recommendation = get_signal(price, rsi, sma50, sma200)
    render_analysis_box(price, rsi, sma50, sma200, signal_label, signal_emoji, signal_color, explanation, recommendation)

    render_chart(df, ticker)
    render_company_info(info)
    render_disclaimer()

# ══════════════════════════════════════════════════════════════════════════════
# Tab 2 — Market Scanner
# ══════════════════════════════════════════════════════════════════════════════
with tab_scanner:
    if not tickers:
        st.info("📌 Select multiple tickers in the bar above to compare stocks side-by-side.")
    else:
        scanner_rows, errors = fetch_scanner_data(tickers, period)
        
        if errors:
            with st.expander(f"⚠️ {len(errors)} ticker(s) failed to load - Click to see details", expanded=False):
                for error in errors:
                    st.warning(error)
        
        if scanner_rows:
            render_market_scanner(scanner_rows)
        elif not errors:
            st.info("Loading data...")
        else:
            st.error("No tickers could be loaded. Please check the ticker symbols and try again.")
        
        render_disclaimer()
