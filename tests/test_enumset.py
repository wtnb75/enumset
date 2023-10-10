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
        es = Enumset([("col", Color), ("dw", DayWeek)])
        es.set("col", Color.RED)
        self.assertEqual(es.get("col"), Color.RED)
        self.assertEqual([Color.RED], list(es.values()))
        self.assertEqual([("col", Color.RED)], list(es.items()))
        self.assertIsNone(es.get("dw"))
        with self.assertRaises(KeyError):
            es.get("notfound")
        with self.assertRaises(KeyError):
            es.set("notfound", Other.A)
        es.clear("col")

    def test_keyless2(self):
        es = Enumset([Color, DayWeek])
        es.setval(Color.RED)
        self.assertEqual(es.getval(Color), Color.RED)
        self.assertEqual([Color.RED], list(es.values()))
        self.assertEqual([("Color", Color.RED)], list(es.items()))
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
        self.assertEqual({Color.GREEN, DayWeek.SUN}, set(es.values()))
        es.clearval(DayWeek)
        self.assertEqual([Color.GREEN], list(es.values()))

    def test_dups(self):
        es = Enumset([("col", Color), ("dw", DayWeek)])
        es.define_key("col2", Color)  # duplicate value: no error
        with self.assertRaises(IndexError):
            es.define_key("dw", Color)  # duplicate key: error

    def test_keyless1(self):
        es = Enumset([Color, DayWeek])
        es.setval(Color.RED)
        es.setval(DayWeek.MON)
        self.assertEqual(es.getval(Color), Color.RED)
        self.assertEqual(es.getval(DayWeek), DayWeek.MON)
        es.clearval(DayWeek)
        self.assertIsNone(es.getval(DayWeek))
        es.setval(Color.GREEN)  # RED -> GREEN
        self.assertEqual([Color.GREEN], list(es.values()))
