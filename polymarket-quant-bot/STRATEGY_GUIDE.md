# Strategy Guide (Research + Decision Support)

This guide adds practical websites/apps and predefined strategy templates you can use **before** enabling live trading.

> Not financial advice. Use this for research discipline, risk controls, and structured experimentation.

## 1) Useful websites/apps to support strategy

### Market & macro context
- **TradingView**: charting, alerts, multi-timeframe trend/volatility checks.
- **CoinGlass**: derivatives/open interest/funding heatmaps.
- **Coinglass Liquidation Map** (or similar): identify crowded positioning and potential squeeze zones.
- **CoinMarketCap / CoinGecko**: broad market screening, volume and listings.

### News, catalysts, and sentiment
- **X (Twitter) lists + TweetDeck/X Pro**: curated signal feeds for exchanges, token teams, and macro reporters.
- **CryptoPanic**: crypto news aggregation with filtering by coin/topic.
- **The Block / CoinDesk**: sector coverage and event-driven context.

### Prediction-market specific context
- **Polymarket site + market pages**: market structure, depth, and event rules.
- **Kalshi market pages**: event contract definitions and settlement conditions.

### Execution and monitoring support
- **Telegram**: real-time bot alerts and incident notifications.
- **Grafana + Prometheus** (later phase): PnL, latency, fill quality, and uptime dashboards.
- **Sentry** (later phase): runtime error tracking and alerting.

## 2) Predefined strategy templates (for phased rollout)

Use these as templates. Start in `check` mode, then paper/sandbox, then constrained live.

### A) Cross-venue spread watcher (arbitrage candidate detector)
- **Goal**: detect price dislocations between venues.
- **Inputs**: best bid/ask snapshots, fees, withdrawal/deposit frictions, latency.
- **Entry rule**: spread > (all-in fees + slippage buffer + safety margin).
- **Exit rule**: spread closes below minimum profitable threshold.
- **Risk controls**: per-trade notional cap, venue exposure cap, stale quote rejection.

### B) Mean-reversion around event overreaction
- **Goal**: fade short-lived spikes/drops when liquidity is thin.
- **Inputs**: short-term z-score, volume surge factor, spread widening signal.
- **Entry rule**: z-score beyond threshold + no major active catalyst.
- **Exit rule**: reversion to moving average or hard stop.
- **Risk controls**: max concurrent positions, volatility-adjusted size, kill-switch on news shock.

### C) Momentum with volatility filter
- **Goal**: ride directional moves only when trend is strong enough.
- **Inputs**: fast/slow EMA slope, ADX/volatility regime, funding bias.
- **Entry rule**: trend alignment + volatility not extreme.
- **Exit rule**: trailing stop or momentum breakdown.
- **Risk controls**: dynamic position sizing by ATR, daily drawdown halt.

### D) Prediction-market mispricing scanner
- **Goal**: find probability mispricings across related event contracts.
- **Inputs**: implied probabilities, event dependencies, resolution rules.
- **Entry rule**: persistent incoherence in related contract probabilities.
- **Exit rule**: probability normalization or nearing settlement uncertainty window.
- **Risk controls**: strict rule-validation checklist, settlement-risk cap per event.

## 3) Decision framework (simple scorecard)

Use this scorecard before enabling any strategy in live mode.

- **Data quality** (0-5): feed completeness, timestamp quality, missing-data rate.
- **Execution quality** (0-5): slippage, rejection rate, latency consistency.
- **Risk profile** (0-5): max drawdown in backtest/paper, tail-risk exposure.
- **Operational stability** (0-5): restart resilience, alert coverage, incident recovery.
- **Economic viability** (0-5): expected edge after fees and conservative slippage.

Recommended gate:
- Minimum total score: **18/25**
- No category below **3/5**

## 4) How to compare against similar bots (later phase)

When you evaluate competing bots/frameworks, compare on the same rubric:

1. **Strategy breadth**: supported strategy families and parameterization.
2. **Venue support**: exchanges/prediction venues, auth reliability, order types.
3. **Risk engine depth**: drawdown controls, kill-switches, exposure limits.
4. **Observability**: logs, metrics, dashboards, alerting.
5. **Performance realism**: backtest assumptions vs realistic fees/slippage.
6. **Developer ergonomics**: config simplicity, testability, onboarding speed.

### Suggested output format for comparisons
For each bot:
- Strengths (top 3)
- Weaknesses (top 3)
- What to adopt into this repo now
- What to postpone to a later phase

## 5) Immediate next steps for this repo

1. Keep `BOT_MODE=check` and validate all API checks pass.
2. Add one strategy module as "read-only signal generation" (no orders).
3. Emit signals to Telegram for 1-2 weeks.
4. Measure signal quality and false positives.
5. Add paper-trade simulation before any live deployment.
