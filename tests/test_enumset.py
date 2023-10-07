import unittest
from enumset import Enumset
from enum import Enum, auto


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


class TestEnumset(unittest.TestCase):
    def test_base(self):
        es = Enumset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        es.set("col", Color.RED)
        self.assertEqual(es.get("col"), Color.RED)
        self.assertEqual([Color.RED], list(es.iterval()))
        self.assertEqual([("col", Color.RED)], list(es.iteritems()))
        self.assertIsNone(es.get("dw"))
        with self.assertRaises(KeyError):
            es.get("notfound")
        with self.assertRaises(KeyError):
            es.set("notfound", Other.A)
        es.clear("col")

    def test_baseval(self):
        es = Enumset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        es.setval(Color.RED)
        self.assertEqual(es.getval(Color), Color.RED)
        self.assertEqual([Color.RED], list(es.iterval()))
        self.assertEqual([("col", Color.RED)], list(es.iteritems()))
        self.assertIsNone(es.getval(DayWeek))
        with self.assertRaises(KeyError):
            es.getval(Other)
        with self.assertRaises(KeyError):
            es.setval(Other.A)
        es.setval(Color.GREEN)
        self.assertEqual(es.getval(Color), Color.GREEN)
        with self.assertRaises(KeyError):
            es.clearval(Other)
        es.setval(DayWeek.SUN)
        self.assertEqual({Color.GREEN, DayWeek.SUN}, set(es.iterval()))
        es.clearval(DayWeek)
        self.assertEqual([Color.GREEN], list(es.iterval()))

    def test_dups(self):
        es = Enumset()
        es.define_enum("col", Color)
        es.define_enum("dw", DayWeek)
        with self.assertLogs(level="WARNING"):
            es.define_enum("col2", Color)
        with self.assertRaises(IndexError):
            es.define_enum("dw", Color)

    def test_keyless(self):
        es = Enumset()
        es.define_enum(None, Color)
        es.define_enum(None, DayWeek)
        es.setval(Color.RED)
        es.setval(DayWeek.MON)
        self.assertEqual(es.getval(Color), Color.RED)
        self.assertEqual(es.getval(DayWeek), DayWeek.MON)
        es.clearval(DayWeek)
        self.assertIsNone(es.getval(DayWeek))
        es.setval(Color.GREEN)  # RED -> GREEN
        self.assertEqual([Color.GREEN], list(es.iterval()))
