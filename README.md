# enumset

collection of Enum classes.

## Install

- pip install enumset

## Enumset

Enumset stores multiple Enum-class value, each value in Enum-class should be unique.

```python
from enum import Enum, auto
from enumset import Enumset

class A(Enum):
    A1 = auto();A2 = auto();A3 = auto()

class B(Enum):
    B1 = auto();B2 = auto()

es = Enumset([A, B])
es.setval(A.A1)
es.setval(B.B2)
assert list(es.values()) == [A.A1, B.B2]
assert es.getval(A) == A.A1

es.setval(A.A2)   # replace A1 -> A2
assert list(es.values()) == [A.A2, B.B2]
assert es.getval(A) == A.A2
```

## Flagset

Flagset stores multiple Enum-class value, like `set[Enum]`.

```python
from enum import Enum, auto
from enumset import Flagset

class A(Enum):
    A1 = auto();A2 = auto();A3 = auto()

class B(Enum):
    B1 = auto();B2 = auto()

fs = Flagset([A, B])
fs.setval(A.A1)
fs.setval(B.B2)
assert list(fs.values()) == [A.A1, B.B2]
assert list(fs.getval(A)) == [A.A1]

fs.setval(A.A2)   # A1+A2
assert list(fs.values()) == [A.A1, A.A2, B.B2]
assert list(fs.getval(A)) == [A.A1, A.A2]

fs.setval(A.A2)   # A2 already exists
assert list(fs.values()) == [A.A1, A.A2, B.B2]
```
