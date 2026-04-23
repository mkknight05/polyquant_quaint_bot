import unittest

from bot.strategy import SpreadStrategy


class SpreadStrategyTests(unittest.TestCase):
    def test_generate_buy_signal_when_spread_above_threshold(self) -> None:
        strategy = SpreadStrategy(threshold=0.01, qty=2)
        signal = strategy.generate('BTC-USD', price_a=100, price_b=101.5)
        self.assertIsNotNone(signal)
        assert signal is not None
        self.assertEqual('buy', signal.side)

    def test_generate_sell_signal_when_spread_below_negative_threshold(self) -> None:
        strategy = SpreadStrategy(threshold=0.01, qty=2)
        signal = strategy.generate('BTC-USD', price_a=100, price_b=98.5)
        self.assertIsNotNone(signal)
        assert signal is not None
        self.assertEqual('sell', signal.side)

    def test_generate_none_when_inside_threshold(self) -> None:
        strategy = SpreadStrategy(threshold=0.01, qty=2)
        signal = strategy.generate('BTC-USD', price_a=100, price_b=100.5)
        self.assertIsNone(signal)


if __name__ == '__main__':
    unittest.main()
