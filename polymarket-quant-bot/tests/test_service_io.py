import tempfile
import unittest

from bot.models import Signal
from bot.service_io import BrokerState, SignalQueue


class SignalQueueTests(unittest.TestCase):
    def test_enqueue_and_drain(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            queue = SignalQueue(f'{tempdir}/signals.jsonl')
            queue.enqueue(Signal(instrument='BTC-USD', side='buy', qty=1, reason='x'))
            queue.enqueue(Signal(instrument='BTC-USD', side='sell', qty=2, reason='y'))

            signals = queue.drain()
            self.assertEqual(2, len(signals))
            self.assertEqual('buy', signals[0].side)
            self.assertEqual('sell', signals[1].side)
            self.assertEqual([], queue.drain())


class BrokerStateTests(unittest.TestCase):
    def test_load_defaults_and_save_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            state = BrokerState(f'{tempdir}/broker_state.json', starting_cash=500)
            cash, position = state.load()
            self.assertEqual(500, cash)
            self.assertEqual(0, position)

            state.save(cash=400, position=1.5)
            cash2, position2 = state.load()
            self.assertEqual(400, cash2)
            self.assertEqual(1.5, position2)


if __name__ == '__main__':
    unittest.main()
