import yfinance as yf
import pandas as pd


def get_economic_risk_score():
    tickers = ["TSM", "ASML", "NVDA", "SOXX"]
    try:
        data = yf.download(tickers, period="5d", interval="1d", progress=False)
        close_prices = data['Close']
        pct_change = close_prices.pct_change().iloc[-1] * 100
        min_change = pct_change.min()
        commodity_scarcity_index = 0.25
        market_risk = min(max(abs(min_change) / 5.0, 0.0), 1.0) if min_change < 0 else 0.1
        econ_score = (0.6 * market_risk) + (0.4 * commodity_scarcity_index)
        return round(econ_score, 2)
    except Exception as e:
        print(f"❌ Economic Sensor Error: {e}")
        return 0.20


def fetch_market_signals():
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

        shared_econ_score = get_economic_risk_score()
        print(f"\n🧬 NORMALIZED ECON SCORE GENERATED FOR PHASE 5: {shared_econ_score} / 1.0")
        print("=" * 50)

        return [
            {
                "ticker": t,
                "pct_change": round(float(latest_pct_change[t]), 2),
                "status": "critical" if latest_pct_change[t] <= -3 else "warn" if latest_pct_change[t] <= -1 else "ok",
                "commodity_scarcity_index": 0.25,
                "econ_score": shared_econ_score,
                "series": close_prices[t].round(2).tolist(),
            }
            for t in tickers
        ]

    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return []


if __name__ == "__main__":
    fetch_market_signals()