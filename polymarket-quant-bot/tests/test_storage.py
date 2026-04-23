import tempfile
import unittest

from bot.models import MarketTick, PaperFill
from bot.storage import Store
from datetime import datetime, timezone


class StoreTests(unittest.TestCase):
    def test_summary_counts_ticks_and_fills(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            store = Store(f'{tempdir}/test.db')
            store.add_tick(MarketTick.now(source='coinbase', instrument='BTC-USD', price=100))
            store.add_fill(
                PaperFill(
                    instrument='BTC-USD',
                    side='buy',
                    qty=1,
                    price=100,
                    ts=datetime.now(timezone.utc),
                )
            )
            summary = store.summary()
            self.assertEqual(1.0, summary['ticks'])
            self.assertEqual(1.0, summary['fills'])


if __name__ == '__main__':
    unittest.main()
