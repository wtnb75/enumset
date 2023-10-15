import unittest
from enumset import Flagset
from enum import Enum, auto
from logging import getLogger

_log = getLogger(__name__)


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3


class DayWeek(Enum):
    MON = auto()
    TUE = auto()
    WED = auto()
    THU = auto()
    FRI = auto()
    SAT = auto()
    SUN = auto()


class Other(Enum):
    A = auto()
    B = auto()


class TestFlagset(unittest.TestCase):
    def test_base(self):
        es = Flagset([("col", Color), ("dw", DayWeek)])
        es.set("col", Color.RED)
        es.set("col", Color.GREEN)
        self.assertEqual(list(es.get("col")), [Color.RED, Color.GREEN])
        self.assertEqual([Color.RED, Color.GREEN], list(es.values()))
        self.assertEqual(
            [("col", Color.RED), ("col", Color.GREEN)], list(es.items()))
        self.assertEqual(list(es.get("dw")), [])
        with self.assertRaises(KeyError):
            for _ in es.get("notfound"):
                pass
        es.clearkey("col")

    def test_keyless2(self):
        es = Flagset([Color, DayWeek])
        es.setval(Color.RED)
        es.setval(Color.GREEN)
        self.assertEqual(list(es.getval(Color)), [Color.RED, Color.GREEN])
        self.assertEqual([Color.RED, Color.GREEN], list(es.values()))
        self.assertEqual(
            [("Color", Color.RED), ("Color", Color.GREEN)], list(es.items()))
        self.assertEqual(list(es.getval(DayWeek)), [])
        with self.assertRaises(KeyError):
            for _ in es.getval(Other):
                pass
        es.setval(Color.GREEN)
        es.clearval1(Color.RED)
        self.assertEqual(list(es.getval(Color)), [Color.GREEN])
        with self.assertRaises(KeyError):
            es.clearval(Other)
        es.setval(DayWeek.SUN)
        self.assertEqual({Color.GREEN, DayWeek.SUN}, set(es.values()))
        es.clearval(DayWeek)
        self.assertEqual([Color.GREEN], list(es.values()))

        self.assertTrue(es.issetval(Color.GREEN))
        self.assertFalse(es.issetval(DayWeek.MON))

    def test_dups(self):
        es = Flagset([("col", Color), ("dw", DayWeek)])
        es.define_key("col2", Color)
        with self.assertRaises(IndexError):
            es.define_key("dw", Color)

    def test_keyless1(self):
        es = Flagset([Color, DayWeek])
        es.setval(Color.RED)
        es.setval(Color.GREEN)  # RED | GREEN
        es.setval(DayWeek.MON)
        self.assertEqual(list(es.getval(Color)), [Color.RED, Color.GREEN])
        self.assertEqual(list(es.getval(DayWeek)), [DayWeek.MON])
        es.clearval(DayWeek)
        self.assertEqual(list(es.getval(DayWeek)), [])
        es.setval(DayWeek.SUN)
        es.clearval1(Color.GREEN)  # RED|GREEN -> RED
        self.assertEqual(list(es.getval(Color)), [Color.RED])
        self.assertEqual(list(es.values()), [Color.RED, DayWeek.SUN])
