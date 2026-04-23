import unittest

from bot.models import Signal
from bot.paper import PaperBroker


class PaperBrokerTests(unittest.TestCase):
    def test_buy_updates_cash_and_position(self) -> None:
        broker = PaperBroker(starting_cash=1000)
        fill = broker.execute(Signal(instrument='BTC-USD', side='buy', qty=2, reason='test'), price=100)
        self.assertEqual('buy', fill.side)
        self.assertEqual(800, broker.cash)
        self.assertEqual(2, broker.position)

    def test_sell_updates_cash_and_position(self) -> None:
        broker = PaperBroker(starting_cash=1000)
        broker.position = 3
        fill = broker.execute(Signal(instrument='BTC-USD', side='sell', qty=1, reason='test'), price=50)
        self.assertEqual('sell', fill.side)
        self.assertEqual(1050, broker.cash)
        self.assertEqual(2, broker.position)


if __name__ == '__main__':
    unittest.main()
