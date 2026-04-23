# Exchange Integration Guide

This document standardizes how to add new exchange connectors in this MVP.

## Goals
- Deterministic adapter behavior.
- Consistent error handling and fallback patterns.
- Minimal integration time for new exchanges.

## Adapter contract
All exchange connectors should subclass `ExchangeAdapter` from `bot/exchange_adapters/base.py` and implement:
- `connect()`
- `fetch_price(symbol)`
- `place_order(symbol, side, qty, order_type='market')`

## Recommended implementation pattern
1. Start from `bot/exchange_adapters/_template.py`.
2. Use `RateLimiter.acquire()` before network actions.
3. Return normalized `OrderResult` from `place_order`.
4. Add at least one unit test for fetch and order paths.

## Fallback pattern
Use `AdapterManager([primary, secondary, ...])` and call:

```python
price, source = await manager.fetch_price_with_fallback('BTC/USD')
```

## Security checklist
- Keep API keys in `.env` only.
- Do not commit secrets.
- Use paper mode by default for new adapters.

## Validation
- `python -m unittest discover -s tests -v`
- `python -m compileall bot run.py services`
- optional smoke using the service flow in README
