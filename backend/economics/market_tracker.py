import yfinance as yf
import pandas as pd


def get_economic_risk_score():
    """
    Fetches market volatility and calculates a Raw Material & Market Volatility Score (0.0 to 1.0).
    THIS IS WHAT PHASE 5 CONSUMES.
    """
    tickers = ["TSM", "ASML", "NVDA", "SOXX"]
    try:
        data = yf.download(tickers, period="5d", interval="1d", progress=False)
        close_prices = data['Close']
        pct_change = close_prices.pct_change().iloc[-1] * 100

        # Calculate max market drop across semiconductor entities
        min_change = pct_change.min()

        # Simulated Commodity Scarcity Index (Neon Gas / Silicon price volatility)
        # 0.0 = Abundant, 1.0 = Extreme Shortage
        commodity_scarcity_index = 0.25

        # If market drops significantly (< -2%), economic volatility risk increases
        market_risk = min(max(abs(min_change) / 5.0, 0.0), 1.0) if min_change < 0 else 0.1

        # Weighted Economic Signal
        econ_score = (0.6 * market_risk) + (0.4 * commodity_scarcity_index)
        return round(econ_score, 2)
    except Exception as e:
        print(f"❌ Economic Sensor Error: {e}")
        return 0.20  # Fallback default


def fetch_market_signals():
    """Keeps your beautiful wall of green terminal output for testing!"""
    print("📈 Fetching Live Macro-Economic Signals...")
    tickers = ["TSM", "ASML", "NVDA", "SOXX"]
    try:
        data = yf.download(tickers, period="5d", interval="1d", progress=False)
        close_prices = data['Close']
        latest_pct_change = close_prices.pct_change().iloc[-1] * 100

        print("\n🔥 DAILY MARKET VOLATILITY:")
        print("=" * 50)
        for ticker in tickers:
            change = latest_pct_change[ticker]
            alert_status = "🚨 VOLATILE (Supply Shock Risk)" if change <= -2.0 else "✅ STABLE"
            print(f"[{ticker.ljust(4)}] Daily Change: {change:+5.2f}%  | {alert_status}")
        print("=" * 50)

        # Run the Phase 5 logic to prove it works
        normalized_score = get_economic_risk_score()
        print(f"\n🧬 NORMALIZED ECON SCORE GENERATED FOR PHASE 5: {normalized_score} / 1.0")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error fetching market data: {e}")


if __name__ == "__main__":
    fetch_market_signals()