import pandas as pd
import pandas_ta as ta
import yfinance as yf
import streamlit as st


@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(ticker: str, period: str) -> pd.DataFrame:
    """Download OHLCV history for an EGX ticker (.CA suffix required)."""
    df = yf.Ticker(ticker).history(period=period, auto_adjust=True)
    if df.empty:
        return df
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df = df.ffill()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


@st.cache_data(ttl=300, show_spinner=False)
def fetch_info(ticker: str) -> dict:
    """Return ticker metadata dict; empty dict on any error."""
    try:
        info = yf.Ticker(ticker).info
        return info if isinstance(info, dict) else {}
    except Exception:
        return {}


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Append RSI-14, SMA-50, and SMA-200 columns to a copy of df."""
    df = df.copy()
    df["RSI"]    = ta.rsi(df["Close"], length=14)
    df["SMA50"]  = ta.sma(df["Close"], length=50)
    df["SMA200"] = ta.sma(df["Close"], length=200)
    return df
