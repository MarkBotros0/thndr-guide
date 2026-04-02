import pandas as pd
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
    df["RSI"]    = _rsi(df["Close"], length=14)
    df["SMA50"]  = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    return df


def _rsi(series: pd.Series, length: int = 14) -> pd.Series:
    """Wilder's RSI — identical to pandas-ta output, no extra dependencies."""
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    # Wilder smoothing = EWM with alpha = 1/length
    avg_gain = gain.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))
