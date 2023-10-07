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
        es = Flagset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        es.set("col", Color.RED)
        es.set("col", Color.GREEN)
        self.assertEqual(list(es.get("col")), [Color.RED, Color.GREEN])
        self.assertEqual([Color.RED, Color.GREEN], list(es.iterval()))
        self.assertEqual(
            [("col", Color.RED), ("col", Color.GREEN)], list(es.iteritems()))
        self.assertEqual(list(es.get("dw")), [])
        with self.assertRaises(KeyError):
            for _ in es.get("notfound"):
                pass
        es.clear("col")

    def test_baseval(self):
        es = Flagset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        es.setval(Color.RED)
        es.setval(Color.GREEN)
        self.assertEqual(list(es.getval(Color)), [Color.RED, Color.GREEN])
        self.assertEqual([Color.RED, Color.GREEN], list(es.iterval()))
        self.assertEqual(
            [("col", Color.RED), ("col", Color.GREEN)], list(es.iteritems()))
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
        self.assertEqual({Color.GREEN, DayWeek.SUN}, set(es.iterval()))
        es.clearval(DayWeek)
        self.assertEqual([Color.GREEN], list(es.iterval()))

        self.assertTrue(es.issetval(Color.GREEN))
        self.assertFalse(es.issetval(DayWeek.MON))

    def test_dups(self):
        es = Flagset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        with self.assertLogs(level="WARNING"):
            es.define_enum("col2", Color)
        with self.assertRaises(IndexError):
            es.define_enum("dw", Color)

    def test_keyless(self):
        es = Flagset()
        es.define_enum(None, Color)
        es.define_enum(None, DayWeek)
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
        self.assertEqual(list(es.iterval()), [Color.RED, DayWeek.SUN])
