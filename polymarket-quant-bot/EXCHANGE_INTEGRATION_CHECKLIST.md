# Exchange Integration Checklist

- [ ] Copy `bot/exchange_adapters/_template.py` to `<exchange>.py`
- [ ] Implement `connect()`
- [ ] Implement `fetch_price()` with rate limiter
- [ ] Implement `place_order()` returning `OrderResult`
- [ ] Add adapter export in `bot/exchange_adapters/__init__.py`
- [ ] Add tests in `tests/test_<exchange>_adapter.py`
- [ ] Add environment variables in `.env.example`
- [ ] Update README usage docs
- [ ] Run staged tests and smoke checks
