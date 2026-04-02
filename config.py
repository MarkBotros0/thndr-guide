# ─── Thndr Theme Colors ───────────────────────────────────────────────────────
YELLOW    = "#FFD700"
GOLD      = "#FFA500"
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
/* Global background */
.stApp {{ background-color: {DARK_BG}; }}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {CARD_BG};
    border-right: 2px solid {YELLOW};
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {{ color: {YELLOW} !important; }}

/* Headers */
h1, h2, h3 {{ color: {YELLOW} !important; }}

/* Metric labels */
[data-testid="stMetricLabel"] p {{ color: {YELLOW} !important; font-weight: 600; }}
[data-testid="stMetricValue"]   {{ color: {TEXT} !important; }}

/* Buttons */
.stButton > button {{
    background-color: {YELLOW};
    color: {DARK_BG};
    font-weight: 700;
    border: none;
    border-radius: 6px;
}}
.stButton > button:hover {{ background-color: #e6c200; color: {DARK_BG}; }}

/* Analysis box */
.analysis-box {{
    border: 2px solid {YELLOW};
    border-radius: 10px;
    padding: 18px 22px;
    background-color: {CARD_BG};
    margin-top: 12px;
}}

/* Progress bar */
div[data-testid="stProgress"] > div > div > div {{
    background-color: {YELLOW} !important;
}}

/* Dividers */
hr {{ border-color: {YELLOW}; opacity: 0.3; }}

/* Disclaimer footer */
.footer-note {{ color: #666; font-size: 0.78rem; margin-top: 24px; }}
</style>
"""
