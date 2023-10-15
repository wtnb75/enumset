import unittest
from enumset import Enumset, Flagset, SetIface
from enum import Enum, Flag

A = Enum("A", "A1 A2 A3")
B = Enum("B", "B1 B2")
C = Flag("C", "C1 C2 C3 C4")


class TestSetCompat(unittest.TestCase):
    def sub1_0(self, a: SetIface, b: SetIface):
        seta = set(a)
        setb = set(b)
        self.assertEqual(a | b, seta | setb)
        self.assertEqual(a & b, seta & setb)
        self.assertEqual(a ^ b, seta ^ setb)
        self.assertEqual(a - b, seta - setb)
        self.assertEqual(a > b, seta > setb)
        self.assertEqual(a >= b, seta >= setb)
        self.assertEqual(a == b, seta == setb)
        self.assertEqual(a <= b, seta <= setb)
        self.assertEqual(a < b, seta < setb)
        self.assertEqual(a.issubset(b), seta.issubset(setb))
        self.assertEqual(a.issuperset(b), seta.issuperset(setb))
        self.assertEqual(a.isdisjoint(b), seta.isdisjoint(setb))
        self.assertEqual(list(a.copy()), list(a))
        self.assertEqual(list(b.copy()), list(b))

    def sub1_1(self, a: SetIface, b: SetIface):
        aset = set(a)
        bset = set(b)

        acopy = a.copy()
        acopy -= b
        self.assertEqual(set(acopy), aset - bset)

        acopy = a.copy()
        acopy &= b
        self.assertEqual(set(acopy), aset & bset)

        acopy = a.copy()
        acopy |= b
        self.assertEqual(set(acopy), aset | bset)

        acopy = a.copy()
        acopy ^= b
        self.assertEqual(set(acopy), aset ^ bset)

    def sub2(self, a: SetIface, n_in_a: Enum, n_notin_a: Enum):
        self.assertTrue(n_in_a in a)
        self.assertFalse(n_notin_a in a)
        oldlen = len(a)
        with self.assertRaises(KeyError):
            a.remove(n_notin_a)
        a.discard(n_notin_a)
        self.assertEqual(oldlen, len(a))
        a.remove(n_in_a)
        self.assertFalse(n_in_a in a)
        self.assertEqual(oldlen-1, len(a))
        a.add(n_in_a)
        a.discard(n_in_a)
        self.assertEqual(oldlen-1, len(a))

    def sub1_2(self, a: SetIface):
        self.assertNotEqual(0, len(a))
        a.clear()
        self.assertEqual(0, len(a))

    def test_enumenum(self):
        a = Enumset([A, B, C])
        b = Enumset([A, B, C])
        a.update([A.A1, B.B2, C.C3])
        b.update([C.C4, B.B2])
        with self.subTest("sub1_0"):
            self.sub1_0(a, b)
        # update Enumset -> replace(C.C3 -> C.C4)
        # with self.subTest("sub1_1"):
        #     self.sub1_1(a, b)
        with self.subTest("sub1_2(A)"):
            self.sub1_2(a)
        with self.subTest("sub1_2(B)"):
            self.sub1_2(b)

    def test_flagflag(self):
        a = Flagset([A, B, C])
        b = Flagset([A, B, C])
        a.update([A.A1, B.B2, C.C3, C.C4])
        b.update([C.C4, B.B2, B.B1])
        with self.subTest("sub1_0"):
            self.sub1_0(a, b)
        with self.subTest("sub1_1"):
            self.sub1_1(a, b)
        with self.subTest("sub1_2(A)"):
            self.sub1_2(a)
        with self.subTest("sub1_2(B)"):
            self.sub1_2(b)

    def test_enumflag(self):
        a = Enumset([A, B, C])
        b = Flagset([A, B, C])
        a.update([A.A1, B.B2, C.C3])
        b.update([C.C4, B.B2, B.B1])
        with self.subTest("sub1_0"):
            self.sub1_0(a, b)
        # update Enumset -> replace(C.C3 -> C.C4)
        # with self.subTest("sub1_1"):
        #     self.sub1_1(a, b)
        with self.subTest("sub1_2(A)"):
            self.sub1_2(a)
        with self.subTest("sub1_2(B)"):
            self.sub1_2(b)

    def test_flagenum(self):
        a = Flagset([A, B, C])
        b = Enumset([A, B, C])
        a.update([A.A1, B.B2, C.C3, C.C4])
        b.update([C.C4, B.B2, A.A1])
        with self.subTest("sub1_0"):
            self.sub1_0(a, b)
        with self.subTest("sub1_1"):
            self.sub1_1(a, b)
        with self.subTest("sub1_2(A)"):
            self.sub1_2(a)
        with self.subTest("sub1_2(B)"):
            self.sub1_2(b)

    def test_enum1(self):
        a = Enumset([A, B, C])
        a.update([A.A1, C.C3])
        abak = a.copy()
        with self.subTest("remove1"):
            self.sub2(a, A.A1, B.B2)
        a = abak
        with self.subTest("remove2"):
            self.sub2(a, C.C3, C.C2)

    def test_enum_pop(self):
        a = Enumset([A, B, C])
        a.update([A.A1, C.C3])
        self.assertIn(a.pop(), [A.A1, C.C3])
        self.assertIn(a.pop(), [A.A1, C.C3])
        with self.assertRaises(KeyError):
            a.pop()
        self.assertEqual(0, len(a))

    def test_flage_pop(self):
        a = Flagset([A, B, C])
        a.update([A.A1, B.B2, C.C3, C.C4])
        self.assertIn(a.pop(), [A.A1, B.B2, C.C3, C.C4])
        self.assertIn(a.pop(), [A.A1, B.B2, C.C3, C.C4])
        self.assertIn(a.pop(), [A.A1, B.B2, C.C3, C.C4])
        self.assertIn(a.pop(), [A.A1, B.B2, C.C3, C.C4])
        with self.assertRaises(KeyError):
            a.pop()
        self.assertEqual(0, len(a))
