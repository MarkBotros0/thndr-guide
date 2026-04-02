import math

import pandas as pd
import yfinance as yf
import streamlit as st


@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(ticker: str, period: str) -> tuple[pd.DataFrame, str | None]:
    """
    Download OHLCV history for an EGX ticker (.CA suffix required).
    Returns: (dataframe, error_message)
    """
    try:
        df = yf.Ticker(ticker).history(period=period, auto_adjust=True)
        if df.empty:
            return df, f"No price data found for {ticker}. The ticker may be delisted or unavailable."
        df = df[["Open", "High", "Low", "Close", "Volume"]]
        df = df.ffill()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df, None
    except Exception as e:
        error_msg = str(e)
        if "delisted" in error_msg.lower() or "not found" in error_msg.lower():
            return pd.DataFrame(), f"{ticker} may be delisted or not found on Yahoo Finance."
        return pd.DataFrame(), f"Error fetching {ticker}: {error_msg}"


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


def fetch_scanner_data(tickers: list, period: str = "1y") -> tuple[list, list]:
    """
    Return one summary dict per ticker for the Market Scanner table.
    Returns: (rows, errors) where errors is a list of error messages
    """
    rows = []
    errors = []
    for ticker in tickers:
        try:
            df_raw, error = fetch_history(ticker, period)
            if error:
                errors.append(error)
                continue
            if df_raw.empty or len(df_raw) < 2:
                errors.append(f"{ticker}: Insufficient data (less than 2 data points)")
                continue
            df = compute_indicators(df_raw)
            latest     = df.iloc[-1]
            prev_close = df["Close"].iloc[-2]
            price      = float(latest["Close"])
            daily_chg  = (price - float(prev_close)) / float(prev_close) * 100
            rsi        = float(latest["RSI"])    if pd.notna(latest["RSI"])    else float("nan")
            sma200     = float(latest["SMA200"]) if pd.notna(latest["SMA200"]) else float("nan")

            if not math.isnan(sma200):
                pct = (price - sma200) / sma200 * 100
                if pct > 5:
                    sma200_pos = f"Above (+{pct:.1f}%)"
                elif pct < -5:
                    sma200_pos = f"Below ({pct:.1f}%)"
                else:
                    sma200_pos = f"Near ({pct:+.1f}%)"
            else:
                sma200_pos = "N/A"

            rows.append({
                "Ticker":       ticker,
                "Price (EGP)":  f"{price:,.2f}",
                "Daily Change": f"{daily_chg:+.2f}%",
                "RSI (14)":     f"{rsi:.1f}" if not math.isnan(rsi) else "N/A",
                "vs SMA 200":   sma200_pos,
                "_rsi_raw":     rsi,
            })
        except Exception as e:
            errors.append(f"{ticker}: {str(e)}")
            continue
    return rows, errors
