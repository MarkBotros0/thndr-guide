import numpy as np
from config import YELLOW, DARK_GREEN, DARK_RED, RSI_OVERSOLD, RSI_OVERBOUGHT, NEAR_SMA200_PCT

# Each signal is: (label, emoji, hex_color, explanation_template_fn)
# explanation_template_fn receives (price, rsi, sma50, sma200) and returns a string.


def _explain_strong_buy(price, rsi, sma50, sma200) -> str:
    return (
        f"RSI is **{rsi:.1f}**, well below the {RSI_OVERSOLD} oversold threshold — the stock is "
        f"statistically cheap relative to recent momentum. The current price "
        f"(**{price:,.2f} EGP**) is within 5% of the 200-day SMA "
        f"(**{sma200:,.2f} EGP**), a key long-term support level. "
        "Together these signals suggest a potential bounce-back opportunity."
    )


def _explain_caution(price, rsi, sma50, sma200) -> str:
    return (
        f"RSI is **{rsi:.1f}**, above the {RSI_OVERBOUGHT} overbought threshold — the stock has "
        "rallied strongly and may be due for a pullback or consolidation phase. "
        "Consider waiting for a cooler entry point before adding to your position."
    )


def _explain_hold(price, rsi, sma50, sma200) -> str:
    return (
        f"The price (**{price:,.2f} EGP**) is trading above its 50-day SMA "
        f"(**{sma50:,.2f} EGP**), indicating a healthy short-term uptrend. "
        f"RSI is **{rsi:.1f}** — neutral territory. "
        "The trend is your friend here; hold existing positions and monitor closely."
    )


def _explain_neutral(price, rsi, sma50, sma200) -> str:
    return (
        f"RSI is **{rsi:.1f}** (neutral range) and the price (**{price:,.2f} EGP**) "
        f"is below the 50-day SMA (**{sma50:,.2f} EGP**). "
        "No strong directional signal at this time. Monitor for a breakout above "
        "the SMA-50 before committing capital."
    )


def get_signal(price: float, rsi: float, sma50: float, sma200: float) -> tuple:
    """
    Evaluate technical conditions and return a (label, emoji, color, explanation) tuple.

    Rules (evaluated in priority order):
      1. STRONG BUY  — RSI < 35  AND  price within ±5% of SMA-200
      2. CAUTION     — RSI > 70
      3. HOLD        — price > SMA-50  (neutral RSI)
      4. NEUTRAL     — none of the above
    """
    if any(np.isnan(v) for v in [rsi, sma50, sma200]):
        return (
            "INSUFFICIENT DATA", "⚪", "#888888",
            "Not enough historical data to generate a reliable signal. "
            "Try selecting a longer time period.",
        )

    near_sma200 = abs(price - sma200) / sma200 <= NEAR_SMA200_PCT

    if rsi < RSI_OVERSOLD and near_sma200:
        return ("STRONG BUY",    "🟢", DARK_GREEN, _explain_strong_buy(price, rsi, sma50, sma200))
    if rsi > RSI_OVERBOUGHT:
        return ("CAUTION",       "🔴", DARK_RED,   _explain_caution(price, rsi, sma50, sma200))
    if price > sma50:
        return ("HOLD",          "🟡", YELLOW,     _explain_hold(price, rsi, sma50, sma200))
    return     ("NEUTRAL / WATCH","⚪", "#AAAAAA",  _explain_neutral(price, rsi, sma50, sma200))
