# Exchange adapters

This package contains standardized async adapters for adding exchanges quickly.

## Files
- `base.py`: shared abstractions (`ExchangeAdapter`, `OrderResult`, `RateLimiter`, `AdapterManager`).
- `gemini.py`: working Gemini adapter implementation.
- `_template.py`: boilerplate starter for new exchanges.

## Add a new exchange
1. Copy `_template.py` to `<exchange>.py`.
2. Implement `connect`, `fetch_price`, and `place_order`.
3. Add tests similar to `tests/test_gemini_adapter.py`.
4. Export your adapter in `__init__.py`.
