# ─── Thndr Theme Colors ───────────────────────────────────────────────────────
YELLOW    = "#F59E0B"
GOLD      = "#F97316"
DARK_BG   = "#0E1117"
CARD_BG   = "#1A1D24"
TEXT      = "#FAFAFA"
DARK_RED  = "#FF4B4B"
DARK_GREEN = "#00C48C"

# ─── Signal Thresholds ────────────────────────────────────────────────────────
RSI_OVERSOLD   = 35
RSI_OVERBOUGHT = 70
NEAR_SMA200_PCT = 0.05   # price within ±5% of SMA-200 counts as "near"

# ─── CSS (injected once in main.py) ──────────────────────────────────────────
THEME_CSS = f"""
<style>
/* ── Global ── */
.stApp {{ background-color: {DARK_BG}; overflow-x: hidden; }}
body, p, span, li {{ color: {TEXT}; }}
h1, h2, h3, h4 {{ color: {YELLOW} !important; }}
.block-container {{ overflow-x: hidden !important; max-width: 100% !important; padding-bottom: 1rem !important; }}
[data-testid="stAppViewContainer"] {{ overflow-x: hidden; }}

/* ── Sidebar (hidden) ── */
section[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"]  {{ display: none !important; }}

/* ── Topbar container ── */
.topbar-wrap {{
    background: {CARD_BG};
    border-radius: 14px;
    border: 1px solid #23262f;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}}

/* ── Streamlit columns: prevent overflow ── */
[data-testid="stHorizontalBlock"] {{
    flex-wrap: wrap;
    min-width: 0;
}}
[data-testid="stColumn"] {{
    min-width: 0;
    overflow: hidden;
}}

/* ── Buttons ── */
.stButton > button {{
    background-color: {YELLOW};
    color: {DARK_BG};
    font-weight: 700;
    border: none;
    border-radius: 8px;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.stButton > button:hover {{ background-color: #e6c200; }}

/* ── Period selectbox ── */
div[data-testid="stSelectbox"] > div > div {{
    background: #23262f !important;
    border: 1px solid #3a3d47 !important;
    border-radius: 8px !important;
    color: #ccc !important;
}}

/* ── Multiselect tags ── */
span[data-baseweb="tag"] {{
    background-color: #2a2d38 !important;
    border: 1px solid #3a3d47 !important;
    border-radius: 6px !important;
}}
span[data-baseweb="tag"] span {{
    color: #ccc !important;
    font-weight: 600;
}}
span[data-baseweb="tag"] span[role="presentation"] {{
    color: #888 !important;
}}

/* ── Tabs ── */
button[data-baseweb="tab"] {{
    color: #888 !important;
    font-weight: 600;
    font-size: 0.9rem;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {YELLOW} !important;
    border-bottom: 2px solid {YELLOW} !important;
}}

/* ── KPI Cards ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 4px 0 20px 0;
    min-width: 0;
}}
.kpi-card {{
    background: {CARD_BG};
    border-radius: 12px;
    border-left: 3px solid {YELLOW};
    padding: 18px 20px;
}}
.kpi-card.rsi-oversold  {{ border-left-color: {DARK_GREEN}; }}
.kpi-card.rsi-overbought {{ border-left-color: {DARK_RED}; }}
.kpi-label {{
    color: #aaa;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1;
    color: {TEXT};
    margin-bottom: 6px;
}}
.kpi-delta {{
    font-size: 0.8rem;
    font-weight: 600;
}}
.delta-up   {{ color: {DARK_GREEN}; }}
.delta-down {{ color: {DARK_RED}; }}
.kpi-tag {{
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    margin-top: 2px;
}}
.tag-oversold   {{ background: rgba(0,196,140,.15); color: {DARK_GREEN}; }}
.tag-overbought {{ background: rgba(255,75,75,.15);  color: {DARK_RED}; }}
.tag-neutral    {{ background: rgba(255,215,0,.1);   color: {YELLOW}; }}

/* ── 52-Week Range Track ── */
.range-wrap {{
    background: {CARD_BG};
    border-radius: 12px;
    padding: 20px 24px;
    margin: 4px 0 20px 0;
}}
.range-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}}
.range-section-label {{
    color: #aaa;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
}}
.range-current {{
    color: {YELLOW};
    font-size: 0.9rem;
    font-weight: 700;
}}
.range-track {{
    position: relative;
    height: 6px;
    background: #2a2d35;
    border-radius: 3px;
    margin-bottom: 12px;
}}
.range-fill {{
    position: absolute;
    left: 0;
    height: 100%;
    background: linear-gradient(90deg, {DARK_RED}, {YELLOW});
    border-radius: 3px;
}}
.range-dot {{
    position: absolute;
    top: -5px;
    width: 16px;
    height: 16px;
    background: {YELLOW};
    border-radius: 50%;
    border: 2px solid {DARK_BG};
    transform: translateX(-50%);
    box-shadow: 0 0 6px rgba(255,215,0,.5);
}}
.range-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 600;
}}
.range-sub {{
    color: #999;
    font-size: 0.72rem;
    text-align: center;
    margin-top: 8px;
}}

/* ── Signal / Analysis Block ── */
.signal-block {{
    background: {CARD_BG};
    border-radius: 12px;
    padding: 24px;
    margin: 4px 0 20px 0;
}}
.signal-badge {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}}
.signal-title {{
    font-size: 1.2rem;
    font-weight: 700;
    line-height: 1.2;
}}
.signal-sub {{
    color: #bbb;
    font-size: 0.8rem;
    margin-top: 3px;
}}
.indicator-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}}
.indicator-pill {{
    background: #23262f;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}}
.ind-label {{
    color: #aaa;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 6px;
}}
.ind-value {{
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 4px;
}}
.ind-sub {{
    color: #999;
    font-size: 0.7rem;
}}
.signal-why {{
    color: {TEXT};
    line-height: 1.7;
    border-top: 1px solid #2a2d35;
    padding-top: 16px;
    font-size: 0.9rem;
}}

/* ── Dividers ── */
hr {{ border-color: {YELLOW}; opacity: 0.15; }}

/* ── Disclaimer footer ── */
.footer-note {{
    color: #777;
    font-size: 0.75rem;
    margin-top: 12px;
    margin-bottom: 0;
    padding-top: 12px;
    border-top: 1px solid #1e2128;
}}

/* ── Expander ── */
details summary {{ color: {YELLOW} !important; font-weight: 600; }}

/* ── Responsive ── */
@media (max-width: 900px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
@media (max-width: 640px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
    .kpi-card {{ padding: 12px 14px; }}
    .kpi-value {{ font-size: 1.1rem; }}
    .indicator-row {{ grid-template-columns: repeat(3, 1fr); gap: 8px; }}
    .indicator-pill {{ padding: 10px 8px; }}
    .ind-value {{ font-size: 0.95rem; }}
    .ind-label {{ font-size: 0.65rem; }}
    .signal-badge {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
    .range-wrap {{ padding: 14px 12px; }}
    .signal-block {{ padding: 14px; }}
    .signal-why {{ font-size: 0.82rem; }}
    h2 {{ font-size: 1.15rem !important; }}

}}
</style>
"""
