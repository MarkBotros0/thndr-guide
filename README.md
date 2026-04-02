# Thndr Guide 📈

> Your EGX (Egyptian Exchange) Investment Companion — built with Streamlit, yfinance, and Plotly.

---

## Features

- **Live EGX data** via Yahoo Finance (`.CA` suffix tickers, e.g. `COMI.CA`, `HRHO.CA`)
- **Thndr-themed UI** — dark background, Thndr Yellow (`#FFD700`) accents
- **Technical signals** — RSI (14), SMA-50, SMA-200 with plain-language explanations
- **Guide Engine** — STRONG BUY / HOLD / CAUTION signals with educational context
- **52-Week Range** visualizer with yellow progress bar
- **Interactive Plotly chart** — candlestick + colored volume bars + MA overlays
- All prices explicitly labelled in **EGP**

---

## Local Development

### 1. Prerequisites

- Python 3.10 or higher
- `pip` (or a virtual environment manager like `venv` / `conda`)

### 2. Clone and install

```bash
git clone https://github.com/<your-username>/thndr-guide.git
cd thndr-guide

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run locally

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploying to Streamlit Cloud (Private Repo)

### Step 1 — Push to a Private GitHub Repository

```bash
# Inside your project folder
git init
git add .
git commit -m "Initial commit — Thndr Guide"

# Create a new private repo on GitHub (via GitHub website or gh CLI)
gh repo create thndr-guide --private --source=. --push
```

Or manually:

1. Go to [github.com/new](https://github.com/new)
2. Name it `thndr-guide`, set visibility to **Private**, click **Create repository**
3. Follow the "push an existing repository" instructions shown on the page

### Step 2 — Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account
2. Click **"New app"**
3. Select:
   - **Repository:** `<your-username>/thndr-guide`
   - **Branch:** `main`
   - **Main file path:** `main.py`
4. Click **"Deploy!"**

Streamlit Cloud will automatically install `requirements.txt` and launch the app.
The `.streamlit/config.toml` file is picked up automatically — no extra configuration needed.

> **Note:** For a private repo, Streamlit Cloud requires you to grant it access during the OAuth flow. Click **"Grant access"** when prompted.

### Step 3 — Whitelist Specific User Emails (Share Button)

Once deployed, control who can access your private app:

1. Open your app on Streamlit Cloud
2. Click the **"Share"** button (top-right corner of the app management page)
3. Under **"Invite viewers"**, enter the email addresses you want to grant access to
4. Click **"Invite"** — they will receive an email with a link to view the app

> Invited users must have (or create) a free Streamlit Cloud account using that email address to authenticate.

**To revoke access:** Return to the Share dialog, find the user, and click the trash icon next to their name.

---

## Supported EGX Tickers (Examples)

| Company                        | Ticker     |
|-------------------------------|------------|
| Commercial International Bank | `COMI.CA`  |
| Eastern Company               | `EAST.CA`  |
| Heliopolis Housing            | `HELI.CA`  |
| Hassan Allam Holding          | `HELI.CA`  |
| Madinet Nasr Housing          | `MNHD.CA`  |
| Orascom Construction          | `ORAS.CA`  |
| Palm Hills                    | `PHDC.CA`  |
| Talaat Mostafa Group          | `TMGH.CA`  |
| Edita Food Industries         | `EFID.CA`  |
| Juhayna Food Industries       | `JUFO.CA`  |

> Full EGX ticker list: search Yahoo Finance with the `.CA` suffix.

---

## Tech Stack

| Layer        | Library          | Version   |
|-------------|-----------------|-----------|
| UI Framework | Streamlit        | ≥ 1.32    |
| Data Source  | yfinance         | ≥ 0.2.38  |
| Data Wrangling | pandas / numpy | ≥ 2.1 / 1.26 |
| Indicators   | pandas-ta        | ≥ 0.3.14b |
| Charts       | Plotly           | ≥ 5.20    |

---

## Disclaimer

Thndr Guide is for **informational and educational purposes only**. It does not constitute financial advice. Always conduct your own research and consult a qualified financial adviser before making investment decisions.
