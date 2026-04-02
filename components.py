"""
UI components for Thndr Guide.
All functions render a distinct section of the page.
No top-level st.* calls — safe to import before st.set_page_config().
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import YELLOW, GOLD, DARK_BG, TEXT, DARK_RED, DARK_GREEN


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar() -> tuple[str, str, bool]:
    """
    Render the sidebar controls.
    Returns (ticker, period, refresh_clicked).
    """
    with st.sidebar:
        st.markdown(
            f"<h2 style='color:{YELLOW}; margin-bottom:4px;'>📊 Thndr Guide</h2>"
            "<p style='color:#888; font-size:0.85rem;'>EGX Investment Companion</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        ticker = st.text_input(
            "EGX Ticker Symbol",
            value="COMI.CA",
            help="Yahoo Finance format — e.g. COMI.CA, HRHO.CA, MNHD.CA",
        ).strip().upper()

        period = st.selectbox(
            "Historical Period",
            options=["3mo", "6mo", "1y", "2y", "5y"],
            index=2,
            format_func=lambda x: {
                "3mo": "3 Months", "6mo": "6 Months",
                "1y": "1 Year",   "2y": "2 Years", "5y": "5 Years",
            }[x],
        )

        st.markdown("---")
        st.markdown(
            f"<p style='color:#888; font-size:0.78rem;'>"
            f"Data via Yahoo Finance. Not financial advice.<br>"
            f"Prices in <b style='color:{YELLOW};'>Egyptian Pounds (EGP)</b>.</p>",
            unsafe_allow_html=True,
        )
        refresh = st.button("🔄  Refresh Data")

    return ticker, period, refresh


# ─── Page Header ──────────────────────────────────────────────────────────────

def render_header(ticker: str) -> None:
    st.markdown(
        f"<h1 style='margin-bottom:0;'>📈 Thndr Guide</h1>"
        f"<p style='color:#888; margin-top:4px;'>Your EGX Investment Companion — "
        f"<span style='color:{YELLOW};'>{ticker}</span></p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


# ─── Metric Row ───────────────────────────────────────────────────────────────

def render_metrics(price: float, daily_change: float, rsi: float,
                   sma50: float, mkt_cap) -> None:
    """Four-column metric strip: Price | RSI | SMA-50 | Market Cap."""
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

    with col1:
        st.metric(
            label="Current Price",
            value=f"{price:,.2f} EGP",
            delta=f"{daily_change:+.2f}% today",
        )
    with col2:
        st.metric(
            label="RSI (14-day)",
            value=f"{rsi:.1f}" if not np.isnan(rsi) else "N/A",
        )
    with col3:
        st.metric(
            label="SMA 50",
            value=f"{sma50:,.2f} EGP" if not np.isnan(sma50) else "N/A",
        )
    with col4:
        st.metric(label="Market Cap", value=_format_market_cap(mkt_cap))


def _format_market_cap(mkt_cap) -> str:
    if not mkt_cap:
        return "N/A"
    if mkt_cap >= 1_000_000_000:
        return f"{mkt_cap / 1_000_000_000:.2f}B EGP"
    return f"{mkt_cap / 1_000_000:.1f}M EGP"


# ─── 52-Week Range Visualizer ─────────────────────────────────────────────────

def render_52week_range(price: float, week52_low: float, week52_high: float) -> None:
    st.markdown("### 52-Week Range")

    range_span = week52_high - week52_low
    position   = (price - week52_low) / range_span if range_span > 0 else 0.5

    left, mid, right = st.columns([1.2, 4, 1.2])

    with left:
        st.markdown(
            f"<p style='color:{TEXT}; text-align:right; margin-top:10px;'>"
            f"Low<br><b style='color:{DARK_RED};'>{week52_low:,.2f} EGP</b></p>",
            unsafe_allow_html=True,
        )
    with mid:
        st.progress(float(np.clip(position, 0.0, 1.0)))
        pct_above_low  = (price - week52_low)  / week52_low  * 100 if week52_low  > 0 else 0
        pct_below_high = (week52_high - price) / week52_high * 100 if week52_high > 0 else 0
        st.markdown(
            f"<p style='color:#888; font-size:0.78rem; text-align:center;'>"
            f"+{pct_above_low:.1f}% above 52-wk low &nbsp;|&nbsp; "
            f"{pct_below_high:.1f}% below 52-wk high</p>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"<p style='color:{TEXT}; margin-top:10px;'>"
            f"High<br><b style='color:{DARK_GREEN};'>{week52_high:,.2f} EGP</b></p>",
            unsafe_allow_html=True,
        )


# ─── Analysis Summary Box ─────────────────────────────────────────────────────

def render_analysis_box(price: float, rsi: float, sma50: float, sma200: float,
                        signal_label: str, signal_emoji: str,
                        signal_color: str, explanation: str) -> None:
    st.markdown("### The Guide — Analysis Summary")

    rsi_str   = f"{rsi:.1f}"          if not np.isnan(rsi)   else "N/A"
    sma50_str = f"{sma50:,.2f} EGP"   if not np.isnan(sma50) else "N/A"
    sma200_str= f"{sma200:,.2f} EGP"  if not np.isnan(sma200)else "N/A"

    st.markdown(
        f"""
        <div class="analysis-box">
            <h3 style="color:{signal_color}; margin-bottom:8px;">
                {signal_emoji} &nbsp; {signal_label}
            </h3>
            <table style="width:100%; margin-bottom:14px; border-collapse:collapse;">
                <tr>
                    <td style="color:#888; padding:4px 12px 4px 0; width:130px;">RSI (14)</td>
                    <td style="color:{TEXT}; font-weight:600;">{rsi_str}</td>
                    <td style="color:#888; padding:4px 12px 4px 24px; width:130px;">SMA 50</td>
                    <td style="color:{YELLOW}; font-weight:600;">{sma50_str}</td>
                </tr>
                <tr>
                    <td style="color:#888; padding:4px 12px 4px 0;">Current Price</td>
                    <td style="color:{TEXT}; font-weight:600;">{price:,.2f} EGP</td>
                    <td style="color:#888; padding:4px 12px 4px 24px;">SMA 200</td>
                    <td style="color:{GOLD}; font-weight:600;">{sma200_str}</td>
                </tr>
            </table>
            <p style="color:{TEXT}; margin:0; line-height:1.6;">
                <b style="color:{YELLOW};">Why?</b>&nbsp; {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Plotly Price Chart ───────────────────────────────────────────────────────

def render_chart(df, ticker: str) -> None:
    st.markdown("### Price Chart")
    st.plotly_chart(_build_figure(df, ticker), use_container_width=True)


def _build_figure(df, ticker: str) -> go.Figure:
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.70, 0.30],
    )

    _add_candlestick(fig, df)
    _add_moving_averages(fig, df)
    _add_volume_bars(fig, df)
    _apply_dark_layout(fig, ticker)
    return fig


def _add_candlestick(fig: go.Figure, df) -> None:
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"], high=df["High"],
            low=df["Low"],   close=df["Close"],
            name="Price",
            increasing_line_color=DARK_GREEN, increasing_fillcolor=DARK_GREEN,
            decreasing_line_color=DARK_RED,   decreasing_fillcolor=DARK_RED,
        ),
        row=1, col=1,
    )


def _add_moving_averages(fig: go.Figure, df) -> None:
    if df["SMA50"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df["SMA50"], name="SMA 50",
                line=dict(color=YELLOW, width=1.5, dash="solid"), opacity=0.85,
            ),
            row=1, col=1,
        )
    if df["SMA200"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df["SMA200"], name="SMA 200",
                line=dict(color=GOLD, width=2, dash="dot"), opacity=0.85,
            ),
            row=1, col=1,
        )


def _add_volume_bars(fig: go.Figure, df) -> None:
    bar_colors = [
        DARK_GREEN if close >= open_ else DARK_RED
        for close, open_ in zip(df["Close"], df["Open"])
    ]
    fig.add_trace(
        go.Bar(
            x=df.index, y=df["Volume"],
            name="Volume", marker_color=bar_colors, opacity=0.65,
        ),
        row=2, col=1,
    )


def _apply_dark_layout(fig: go.Figure, ticker: str) -> None:
    axis_style = dict(titlefont=dict(color=YELLOW), tickfont=dict(color=TEXT), gridcolor="#2a2d35")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        title=dict(text=f"{ticker} — Price & Volume", font=dict(color=YELLOW, size=18)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color=TEXT)),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=60, b=10),
        yaxis =dict(title="Price (EGP)", **axis_style),
        yaxis2=dict(title="Volume",      **axis_style),
        xaxis2=dict(tickfont=dict(color=TEXT), gridcolor="#2a2d35"),
    )


# ─── Company Info Expander ────────────────────────────────────────────────────

def render_company_info(info: dict) -> None:
    fields = {
        "Full Name":      info.get("longName",       "N/A"),
        "Sector":         info.get("sector",          "N/A"),
        "Industry":       info.get("industry",        "N/A"),
        "Exchange":       info.get("exchange",        "EGX"),
        "Currency":       info.get("currency",        "EGP"),
        "P/E Ratio":      info.get("trailingPE",     "N/A"),
        "EPS (EGP)":      info.get("trailingEps",    "N/A"),
        "Dividend Yield": _format_dividend(info.get("dividendYield")),
        "Beta":           info.get("beta",            "N/A"),
        "Avg Volume":     _format_avg_volume(info.get("averageVolume")),
    }

    with st.expander("📋  Company Information", expanded=False):
        col1, col2 = st.columns(2)
        items = list(fields.items())
        half  = (len(items) + 1) // 2
        _render_info_column(col1, items[:half])
        _render_info_column(col2, items[half:])


def _render_info_column(col, items: list) -> None:
    with col:
        for label, value in items:
            st.markdown(
                f"<p style='margin:4px 0;'>"
                f"<span style='color:{YELLOW}; font-weight:600;'>{label}:</span> "
                f"<span style='color:{TEXT};'>{value}</span></p>",
                unsafe_allow_html=True,
            )


def _format_dividend(value) -> str:
    return f"{value * 100:.2f}%" if value else "N/A"


def _format_avg_volume(value) -> str:
    return f"{value:,}" if value else "N/A"


# ─── Footer Disclaimer ────────────────────────────────────────────────────────

def render_disclaimer() -> None:
    st.markdown(
        "<p class='footer-note'>⚠️ Thndr Guide is for informational purposes only and does "
        "not constitute financial advice. Always do your own research before investing. "
        "Data sourced from Yahoo Finance and may be delayed.</p>",
        unsafe_allow_html=True,
    )
