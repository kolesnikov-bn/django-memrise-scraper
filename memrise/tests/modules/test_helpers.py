from django.test import TestCase

from memrise.core.modules.dashboard_counter import DashboardCounter, START_OFFSET, STEP


class TestDashboardCounter(TestCase):
    def test_next(self):
        dc = DashboardCounter()
        self.assertEqual(dc.offset, START_OFFSET)
        repeated = 5
        [dc.next() for x in range(repeated)]
        # Умножаем количество повторений -1 один холостой, так как отчет начинается с 0, на шаг смещения.
        expected = (repeated-1) * STEP
        self.assertEqual(dc.offset, expected)
