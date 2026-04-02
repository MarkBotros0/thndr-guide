"""
UI components for Thndr Guide.
All functions render a distinct section of the page.
No top-level st.* calls — safe to import before st.set_page_config().
"""

import math

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import YELLOW, GOLD, DARK_BG, CARD_BG, TEXT, DARK_RED, DARK_GREEN


# ─── Sidebar ──────────────────────────────────────────────────────────────────

_EGX_TICKERS = [
    # Banking
    "COMI.CA", "QNBA.CA", "ADIB.CA", "AAIB.CA", "AIBK.CA", "ALEX.CA",
    # Real Estate
    "TMGH.CA", "PHDC.CA", "MNHD.CA", "OCDI.CA", "HELI.CA",
    # Telecom & Tech
    "ETEL.CA", "SWDY.CA",
    # Energy & Utilities
    "AMOC.CA", "EGTS.CA",
    # Food & Consumer
    "JUFO.CA", "DOMN.CA", "CLHO.CA", "EDBE.CA",
    # Industrial & Diversified
    "ACGC.CA", "EKHO.CA", "HRHO.CA", "EFIH.CA", "ORWE.CA",
    "ABUK.CA", "EAST.CA", "SKPC.CA", "MFPC.CA", "IRON.CA",
]

_PERIOD_LABELS = {
    "3mo": "3M", "6mo": "6M", "1y": "1Y", "2y": "2Y", "5y": "5Y",
}


def render_topbar() -> tuple[list, str, bool]:
    """
    Inline control bar at the top of the main page.
    Returns (tickers, period, refresh_clicked).
    """
    # Row 1: brand + refresh button
    c_brand, c_btn = st.columns([4.5, 1.2])
    with c_brand:
        st.markdown(
            f"<div style='padding-top:4px;'>"
            f"<span style='color:{YELLOW}; font-size:1.15rem; font-weight:800; "
            f"letter-spacing:-.02em;'>📊 Thndr Guide</span>"
            f"<span style='color:#999; font-size:0.7rem; margin-left:10px;'>"
            f"EGX Investment Companion</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c_btn:
        refresh = st.button("🔄 Refresh Data", type="secondary", use_container_width=True)

    # Row 2: ticker selector (full width)
    tickers = st.multiselect(
        "Tickers",
        options=_EGX_TICKERS,
        default=["COMI.CA"],
        placeholder="Select EGX tickers…",
        label_visibility="collapsed",
        help="First selected ticker drives the Stock Analysis tab. "
             "All selected tickers appear in the Market Scanner.",
    )

    # Row 3: period dropdown
    period = st.selectbox(
        "Period",
        options=list(_PERIOD_LABELS.keys()),
        index=2,
        format_func=lambda x: _PERIOD_LABELS[x],
        label_visibility="collapsed",
    )

    st.markdown(
        "<hr style='margin:8px 0 16px 0; border-color:#23262f; opacity:1;'>",
        unsafe_allow_html=True,
    )
    return tickers, period, refresh


# ─── Page Header ──────────────────────────────────────────────────────────────

def render_header(ticker: str, company_name: str, num_tickers: int = 1) -> None:
    analyzing_note = ""
    if num_tickers > 1:
        analyzing_note = (
            f"<span style='background:#23262f; color:{YELLOW}; font-size:0.75rem; "
            f"font-weight:700; padding:3px 10px; border-radius:20px; "
            f"border:1px solid #2a2d35; margin-left:10px;'>"
            f"Analyzing: {ticker}</span>"
        )

    st.markdown(
        f"<div style='margin-bottom:20px;'>"
        f"<div style='display:flex; align-items:center; gap:10px; flex-wrap:wrap;'>"
        f"<h2 style='margin:0; font-size:1.6rem;'>{company_name}</h2>"
        f"<span style='background:{YELLOW}; color:{DARK_BG}; font-size:0.75rem; "
        f"font-weight:800; padding:3px 10px; border-radius:20px;'>{ticker}</span>"
        f"<span style='background:#1e2128; color:#888; font-size:0.72rem; "
        f"padding:3px 10px; border-radius:20px; border:1px solid #2a2d35;'>EGX · EGP</span>"
        f"{analyzing_note}"
        f"</div></div>",
        unsafe_allow_html=True,
    )


# ─── KPI Cards ────────────────────────────────────────────────────────────────

def render_metrics(price: float, daily_change: float, rsi: float,
                   sma50: float, mkt_cap) -> None:
    """Four custom KPI cards: Price | RSI | SMA-50 | Market Cap."""
    delta_cls   = "delta-up" if daily_change >= 0 else "delta-down"
    delta_arrow = "▲" if daily_change >= 0 else "▼"

    # RSI card accent + tag
    if not np.isnan(rsi):
        if rsi < 35:
            rsi_card_cls  = "rsi-oversold"
            rsi_color     = DARK_GREEN
            rsi_tag       = f"<span class='kpi-tag tag-oversold'>Oversold</span>"
        elif rsi > 70:
            rsi_card_cls  = "rsi-overbought"
            rsi_color     = DARK_RED
            rsi_tag       = f"<span class='kpi-tag tag-overbought'>Overbought</span>"
        else:
            rsi_card_cls  = ""
            rsi_color     = YELLOW
            rsi_tag       = f"<span class='kpi-tag tag-neutral'>Neutral</span>"
        rsi_val = f"{rsi:.1f}"
    else:
        rsi_card_cls, rsi_color, rsi_tag, rsi_val = "", TEXT, "", "N/A"

    sma50_val = f"{sma50:,.2f} EGP" if not np.isnan(sma50) else "N/A"
    cap_val   = _format_market_cap(mkt_cap)

    st.markdown(
        f"""
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Current Price</div>
            <div class="kpi-value">{price:,.2f} <span style="font-size:.9rem;font-weight:500;color:#888;">EGP</span></div>
            <div class="kpi-delta {delta_cls}">{delta_arrow} {abs(daily_change):.2f}% today</div>
          </div>
          <div class="kpi-card {rsi_card_cls}">
            <div class="kpi-label">RSI (14-day)</div>
            <div class="kpi-value" style="color:{rsi_color};">{rsi_val}</div>
            {rsi_tag}
          </div>
          <div class="kpi-card">
            <div class="kpi-label">SMA 50</div>
            <div class="kpi-value" style="font-size:1.25rem;">{sma50_val}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Market Cap</div>
            <div class="kpi-value" style="font-size:1.25rem;">{cap_val}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _format_market_cap(mkt_cap) -> str:
    if not mkt_cap:
        return "N/A"
    if mkt_cap >= 1_000_000_000:
        return f"{mkt_cap / 1_000_000_000:.2f}B EGP"
    return f"{mkt_cap / 1_000_000:.1f}M EGP"


# ─── 52-Week Range Track ──────────────────────────────────────────────────────

def render_52week_range(price: float, week52_low: float, week52_high: float) -> None:
    span     = week52_high - week52_low
    position = (price - week52_low) / span if span > 0 else 0.5
    pct      = float(np.clip(position, 0.0, 1.0)) * 100

    pct_above_low  = (price - week52_low)  / week52_low  * 100 if week52_low  > 0 else 0
    pct_below_high = (week52_high - price) / week52_high * 100 if week52_high > 0 else 0

    st.markdown(
        f"""
        <div class="range-wrap">
          <div class="range-header">
            <span class="range-section-label">52-Week Range</span>
            <span class="range-current">Current: {price:,.2f} EGP</span>
          </div>
          <div class="range-track">
            <div class="range-fill" style="width:{pct:.1f}%;"></div>
            <div class="range-dot"  style="left:{pct:.1f}%;"></div>
          </div>
          <div class="range-footer">
            <span style="color:{DARK_RED};">{week52_low:,.2f} EGP</span>
            <span style="color:{DARK_GREEN};">{week52_high:,.2f} EGP</span>
          </div>
          <div class="range-sub">
            +{pct_above_low:.1f}% above 52-wk low &nbsp;·&nbsp; {pct_below_high:.1f}% below 52-wk high
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── Analysis Summary Block ───────────────────────────────────────────────────

def render_analysis_box(price: float, rsi: float, sma50: float, sma200: float,
                        signal_label: str, signal_emoji: str,
                        signal_color: str, explanation: str, recommendation: str) -> None:

    rsi_str    = f"{rsi:.1f}"         if not np.isnan(rsi)    else "N/A"
    sma50_str  = f"{sma50:,.2f} EGP"  if not np.isnan(sma50)  else "N/A"
    sma200_str = f"{sma200:,.2f} EGP" if not np.isnan(sma200) else "N/A"

    # RSI context label
    if not np.isnan(rsi):
        if rsi < 35:
            rsi_color, rsi_context = DARK_GREEN, "Oversold zone"
        elif rsi > 70:
            rsi_color, rsi_context = DARK_RED,   "Overbought zone"
        else:
            rsi_color, rsi_context = YELLOW,      "Neutral zone"
    else:
        rsi_color, rsi_context = TEXT, ""

    # SMA position labels
    sma50_context  = _sma_context(price, sma50)
    sma200_context = _sma_context(price, sma200)

    # Badge background from signal color
    badge_bg     = _hex_to_rgba(signal_color, 0.10)
    badge_border = _hex_to_rgba(signal_color, 0.30)

    # Recommendation styling
    if recommendation == "BUY":
        rec_color = DARK_GREEN
        rec_emoji = "✅"
    elif recommendation == "NOT BUY":
        rec_color = DARK_RED
        rec_emoji = "🚫"
    else:  # WAIT
        rec_color = YELLOW
        rec_emoji = "⏳"

    st.markdown(
        f"""
        <div class="signal-block">
          <div class="signal-badge"
               style="background:{badge_bg}; border:1px solid {badge_border};">
            <span style="font-size:2.2rem; line-height:1;">{signal_emoji}</span>
            <div>
              <div class="signal-title" style="color:{signal_color};">{signal_label}</div>
              <div class="signal-sub">RSI + Moving Average analysis</div>
            </div>
          </div>

          <div style="text-align:center; margin:1rem 0; padding:0.8rem; background:{_hex_to_rgba(rec_color, 0.15)}; border-radius:8px; border:1px solid {_hex_to_rgba(rec_color, 0.3)};">
            <span style="font-size:1.1rem;">{rec_emoji}</span>
            <span style="font-size:1.3rem; font-weight:600; color:{rec_color}; margin-left:0.5rem;">
              {recommendation}
            </span>
          </div>

          <div class="indicator-row">
            <div class="indicator-pill">
              <div class="ind-label">RSI (14)</div>
              <div class="ind-value" style="color:{rsi_color};">{rsi_str}</div>
              <div class="ind-sub">{rsi_context}</div>
            </div>
            <div class="indicator-pill">
              <div class="ind-label">SMA 50</div>
              <div class="ind-value" style="color:{YELLOW};">{sma50_str}</div>
              <div class="ind-sub">{sma50_context}</div>
            </div>
            <div class="indicator-pill">
              <div class="ind-label">SMA 200</div>
              <div class="ind-value" style="color:{GOLD};">{sma200_str}</div>
              <div class="ind-sub">{sma200_context}</div>
            </div>
          </div>

          <div class="signal-why">
            <b style="color:{YELLOW};">Why?</b>&nbsp; {explanation}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _sma_context(price: float, sma: float) -> str:
    if np.isnan(sma):
        return "Insufficient data"
    diff_pct = (price - sma) / sma * 100
    if diff_pct > 0:
        return f"Price +{diff_pct:.1f}% above"
    return f"Price {diff_pct:.1f}% below"


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ─── Plotly Price Chart ───────────────────────────────────────────────────────

def render_chart(df, ticker: str) -> None:
    st.plotly_chart(
        _build_figure(df, ticker),
        width='stretch',
        config={'displayModeBar': False, 'displaylogo': False},
    )


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
                line=dict(color=YELLOW, width=1.5), opacity=0.85,
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
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG,
        plot_bgcolor="#13161e",
        legend=dict(
            orientation="h", yanchor="top", y=1.0, xanchor="left", x=0,
            font=dict(color=TEXT, size=12), bgcolor="rgba(0,0,0,0)",
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=36, b=10),
    )
    fig.update_yaxes(
        title=dict(font=dict(color="#888")), tickfont=dict(color="#888"),
        gridcolor="#1e2128", zeroline=False,
    )
    fig.update_xaxes(tickfont=dict(color="#888"), gridcolor="#1e2128")
    fig.update_yaxes(title_text="Price (EGP)", row=1, col=1)
    fig.update_yaxes(title_text="Volume",      row=2, col=1)


# ─── Company Info Expander ────────────────────────────────────────────────────

def render_company_info(info: dict) -> None:
    fields = {
        "Full Name":      info.get("longName",       "N/A"),
        "Sector":         info.get("sector",          "N/A"),
        "Industry":       info.get("industry",        "N/A"),
        "Exchange":       info.get("exchange",        "EGX"),
        "Currency":       info.get("currency",        "EGP"),
        "P/E Ratio":      info.get("trailingPE",      "N/A"),
        "EPS (EGP)":      info.get("trailingEps",     "N/A"),
        "Dividend Yield": _format_dividend(info.get("dividendYield")),
        "Beta":           info.get("beta",             "N/A"),
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
                f"<p style='margin:6px 0; font-size:0.88rem;'>"
                f"<span style='color:#aaa; font-size:0.72rem; text-transform:uppercase; "
                f"letter-spacing:.06em; font-weight:700;'>{label}</span><br>"
                f"<span style='color:{TEXT}; font-weight:600;'>{value}</span></p>",
                unsafe_allow_html=True,
            )


def _format_dividend(value) -> str:
    return f"{value * 100:.2f}%" if value else "N/A"


def _format_avg_volume(value) -> str:
    return f"{value:,}" if value else "N/A"


# ─── Market Scanner ──────────────────────────────────────────────────────────

def render_market_scanner(rows: list) -> None:
    """Comparison table. Yellow-highlighted rows = RSI < 35 (oversold)."""
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown(
            f"<p style='color:#888; font-size:0.82rem; margin:0;'>"
            f"Comparing {len(rows)} ticker(s) &nbsp;·&nbsp; "
            f"<span style='background:rgba(255,215,0,.15); color:{YELLOW}; "
            f"padding:2px 8px; border-radius:8px; font-weight:700;'>Yellow</span>"
            f" = RSI &lt; 35 (potential oversold opportunity)</p>",
            unsafe_allow_html=True,
        )

    if not rows:
        st.info("Select at least one ticker in the sidebar.")
        return

    df        = pd.DataFrame(rows)
    rsi_vals  = df["_rsi_raw"].values
    df_display = df.drop(columns=["_rsi_raw"]).reset_index(drop=True)

    def _highlight(row):
        rsi = rsi_vals[row.name]
        if not pd.isna(rsi) and rsi < 35:
            return [f"background-color:{YELLOW}; color:{DARK_BG}; font-weight:700;"] * len(row)
        return [""] * len(row)

    styled = df_display.style.apply(_highlight, axis=1)
    st.dataframe(styled, width='stretch', hide_index=True)


# ─── Footer Disclaimer ────────────────────────────────────────────────────────

def render_disclaimer() -> None:
    st.markdown(
        "<p class='footer-note'>⚠️ Thndr Guide is for informational purposes only and does "
        "not constitute financial advice. Always do your own research before investing. "
        "Data sourced from Yahoo Finance and may be delayed.</p>",
        unsafe_allow_html=True,
    )
