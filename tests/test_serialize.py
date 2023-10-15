import unittest
from enumset import Enumset, Flagset
from enum import Flag, Enum
import pickle
try:
    import yaml
    have_yaml = True
except ImportError:
    have_yaml = False


A = Enum("A", "A1 A2 A3")
B = Enum("B", "B1 B2")
C = Flag("C", "C1 C2 C3 C4")


class TestSerialize(unittest.TestCase):
    def enumdata(self):
        es = Enumset([A, B, C])
        es.update([A.A1, C.C3])
        return es

    def flagdata(self):
        fs = Flagset([A, B, C])
        fs.update([A.A1, C.C3, C.C4])
        return fs

    def test_str_enum(self):
        data = self.enumdata()
        strdata = str(data)
        self.assertIn("Enumset", strdata)
        self.assertIn("A1", strdata)
        self.assertIn("C3", strdata)

    def test_str_flag(self):
        data = self.flagdata()
        strdata = str(data)
        self.assertIn("Flagset", strdata)
        self.assertIn("A1", strdata)
        self.assertIn("C3", strdata)
        self.assertIn("C4", strdata)

    def test_repr_enum(self):
        data = self.enumdata()
        strdata = repr(data)
        self.assertIn("Enumset", strdata)
        self.assertIn("A1", strdata)
        self.assertIn("C3", strdata)

    def test_repr_flag(self):
        data = self.flagdata()
        strdata = repr(data)
        self.assertIn("Flagset", strdata)
        self.assertIn("A1", strdata)
        self.assertIn("C3", strdata)
        self.assertIn("C4", strdata)

    def test_pickle_enum(self):
        data = self.enumdata()
        pickled = pickle.dumps(data)
        unpickled = pickle.loads(pickled)
        self.assertEqual(data, unpickled)
        self.assertEqual(pickle.dumps(self.enumdata()), pickled)

    def test_pickle_flag(self):
        data = self.flagdata()
        pickled = pickle.dumps(data)
        unpickled = pickle.loads(pickled)
        self.assertEqual(data, unpickled)
        self.assertEqual(pickle.dumps(self.flagdata()), pickled)

    @unittest.skipUnless(have_yaml, "PyYAML not installed")
    def test_yaml_enum(self):
        data = self.enumdata()
        pickled = yaml.dump(data)
        unpickled = yaml.unsafe_load(pickled)
        self.assertEqual(data, unpickled)
        self.assertEqual(yaml.dump(self.enumdata()), pickled)

    @unittest.skipUnless(have_yaml, "PyYAML not installed")
    def test_yaml_flag(self):
        data = self.flagdata()
        pickled = yaml.dump(data)
        unpickled = yaml.unsafe_load(pickled)
        self.assertEqual(data, unpickled)
        self.assertEqual(yaml.dump(self.flagdata()), pickled)
