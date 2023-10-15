from typing import Union, Iterable
from collections.abc import Collection
from enum import Enum, EnumType
from abc import abstractmethod, ABCMeta
from collections import OrderedDict


class SetIface(metaclass=ABCMeta):
    def __init__(self, kvs: list[Union[EnumType, tuple[str, EnumType]]] = []):
        self._val: int = 0
        self._keys: OrderedDict[str, tuple[EnumType, int]] = OrderedDict()
        for kv in kvs:
            if isinstance(kv, (list, tuple)) and len(kv) == 2:
                k, vt = kv
            elif isinstance(kv, EnumType):
                k = kv.__name__
                vt = kv
            else:
                raise TypeError(f"invalid type: {kv}")
            self.define_key(k, vt)

    def define_key(self, k: str, vt: EnumType) -> None:
        if k in self._keys:
            raise IndexError(f"key {k} already exists")
        vlen = len(vt)
        mval = max(self._keys.values(), default=(0, 0), key=lambda f: f[1])
        self._keys[k] = (vt, mval[1] + vlen)

    def get_key(self, k: str) -> int:
        vt, vval = self._keys[k]
        return vval - len(vt)

    def iter_key(self) -> Iterable[tuple[str, int, EnumType]]:
        prev = 0
        for k, v in self._keys.items():
            yield k, prev, v[0]
            prev = v[1]

    @abstractmethod
    def items(self) -> Iterable[tuple[str, Enum]]:
        raise NotImplementedError("items")

    def values(self) -> Iterable[Enum]:
        for _, v in self.items():
            yield v

    def keys(self) -> Iterable[str]:
        return self._keys.keys()

    @abstractmethod
    def get(self, key: str) -> Union[None, Enum, Iterable[Enum]]:
        raise NotImplementedError("get")

    @abstractmethod
    def clearkey(self, key: str) -> bool:
        raise NotImplementedError("clear")

    @abstractmethod
    def clear1(self, key: str, e: Enum) -> bool:
        raise NotImplementedError("clear1")

    @abstractmethod
    def set(self, key: str, e: Enum) -> bool:
        raise NotImplementedError("clear")

    @abstractmethod
    def isset(self, key: str, e: Enum) -> bool:
        raise NotImplementedError("clear")

    # value-only ops
    def getval(self, et: EnumType) -> Union[None, Enum, Iterable[Enum]]:
        return self.get(et.__name__)

    def clearval(self, et: EnumType):
        return self.clearkey(et.__name__)

    def clearval1(self, e: Enum):
        return self.clear1(e.__class__.__name__, e)

    def setval(self, n: Enum):
        return self.set(n.__class__.__name__, n)

    def issetval(self, n: Enum):
        return self.isset(n.__class__.__name__, n)

    # set() interface
    def __len__(self) -> int:
        return len(list(self.items()))

    def __contains__(self, n: Enum) -> bool:
        return self.issetval(n)

    def copy(self):
        res = self.__class__()
        res._keys = self._keys.copy()
        res._val = self._val
        return res

    def clear(self):
        self._val = 0

    def __iter__(self):
        return self.values()

    add = setval

    def remove(self, n: Enum):
        if not self.clearval1(n):
            raise KeyError(f"key {n} not found")

    discard = clearval1

    def pop(self):
        try:
            res = next(self.values())
            self.clearval1(res)
            return res
        except StopIteration:
            raise KeyError("empty set")

    def update(self, other: Iterable[Enum]):
        for i in other:
            self.setval(i)
        return self

    __ior__ = update

    def intersection_update(self, other: Iterable[Enum]):
        for i in self:
            if i not in other:
                self.clearval1(i)
        return self

    __iand__ = intersection_update

    def difference_update(self, other: Iterable[Enum]):
        for i in other:
            self.clearval1(i)
        return self

    __isub__ = difference_update

    def symmetric_difference_update(self, other: Iterable[Enum]):
        for i in other:
            if i in self:
                self.clearval1(i)
            else:
                self.setval(i)
        return self

    __ixor__ = symmetric_difference_update

    def isdisjoint(self, other: Iterable[Enum]) -> bool:
        for i in other:
            if i in self:
                return False
        return True

    def issubset(self, other: Iterable[Enum]) -> bool:
        for i in self:
            if i not in other:
                return False
        return True

    __le__ = issubset

    def issuperset(self, other) -> bool:
        for i in other:
            if i not in self:
                return False
        return True

    __ge__ = issuperset

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Collection):
            raise NotImplementedError()
        if len(other) != len(self):
            return False
        for i in other:
            if i not in self:
                return False
        return True

    # fallback to set
    def __lt__(self, other) -> bool:
        return {x for x in self.values()} < {x for x in other.values()}

    def __gt__(self, other) -> bool:
        return {x for x in self.values()} > {x for x in other.values()}

    def union(self, other):
        return {x for x in self.values()} | {x for x in other.values()}

    __or__ = union

    def intersection(self, other):
        return {x for x in self.values()} & {x for x in other.values()}

    __and__ = intersection

    def difference(self, other):
        return {x for x in self.values()} - {x for x in other.values()}

    __sub__ = difference

    def symmetric_difference(self, other):
        return {x for x in self.values()} ^ {x for x in other.values()}

    __xor__ = symmetric_difference

    # repr/str
    def __str__(self):
        return "{}({})".format(self.__class__.__name__, set(self))

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, list(self._keys.keys()), set(self))

    # pickle/yaml
    def __getstate__(self):
        return {
            "keys": [(x[0], x[1][0]) for x in self._keys.items()],
            "val": self._val,
        }

    def __setstate__(self, d):
        self._keys = OrderedDict()
        for k, vt in d["keys"]:
            self.define_key(k, vt)
        self._val = d["val"]
