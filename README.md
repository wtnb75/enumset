# enumset

collection of Enum classes.

## Install

- pip install enumset

## Enumset

Enumset stores multiple Enum-class value, each value in Enum-class should be unique.

```python
from enum import Enum, Flag
from enumset import Enumset

A = Enum("A", "A1 A2 A3")
B = Enum("B", "B1 B2")
C = Flag("C", "C1 C2 C3 C4")

es = Enumset([A, B, C])
es.setval(A.A1)
es.setval(B.B2)
es.setval(C.C3)
assert list(es.values()) == [A.A1, B.B2, C.C3]
assert es.getval(A) == A.A1

es.setval(A.A2)   # replace A1 -> A2
es.setval(C.C4)   # replace C3 -> C4
assert list(es.values()) == [A.A2, B.B2, C.C4]
assert es.getval(A) == A.A2
```

## Flagset

Flagset stores multiple Enum-class value, like `set[Enum]`.

```python
from enum import Enum, Flag
from enumset import Flagset

A = Enum("A", "A1 A2 A3")
B = Enum("B", "B1 B2")
C = Flag("C", "C1 C2 C3 C4")

fs = Flagset([A, B, C])
fs.setval(A.A1)
fs.setval(B.B2)
fs.setval(C.C3)
assert list(fs.values()) == [A.A1, B.B2, C.C3]
assert list(fs.getval(A)) == [A.A1]

fs.setval(A.A2)   # A1+A2
fs.setval(C.C4)   # C3+C4
assert list(fs.values()) == [A.A1, A.A2, B.B2, C.C3, C.C4]
assert list(fs.getval(A)) == [A.A1, A.A2]
assert list(fs.getval(C)) == [C.C3, C.C4]

fs.setval(A.A2)   # A2 already exists
assert list(fs.values()) == [A.A1, A.A2, B.B2, C.C3, C.C4]
```
