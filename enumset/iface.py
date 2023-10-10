from typing import Union, Iterable
from enum import Enum, EnumType
from abc import abstractmethod, ABCMeta
from collections import OrderedDict


class SetIface(metaclass=ABCMeta):
    def __init__(self, kvs: list[Union[EnumType, tuple[EnumType, str]]] = []):
        self.val = 0
        self.keys: OrderedDict[str, tuple[EnumType, int]] = OrderedDict()
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
        if k in self.keys:
            raise IndexError(f"key {k} already exists")
        vlen = len(vt)
        mval = max(self.keys.values(), default=(0, 0), key=lambda f: f[1])
        self.keys[k] = (vt, mval[1] + vlen)

    def get_key(self, k: str) -> int:
        vt, vval = self.keys[k]
        return vval - len(vt)

    def iter_key(self) -> Iterable[tuple[str, int, EnumType]]:
        prev = 0
        for k, v in self.keys.items():
            yield k, prev, v[0]
            prev = v[1]

    @abstractmethod
    def items(self) -> Iterable[tuple[str, Enum]]:
        raise NotImplementedError("items")

    def values(self) -> Iterable[Enum]:
        for _, v in self.items():
            yield v

    def keys(self) -> Iterable[str]:
        return self.keys.keys()

    @abstractmethod
    def get(self, key: str) -> Union[Enum, Iterable[Enum]]:
        raise NotImplementedError("get")

    @abstractmethod
    def clear(self, key: str) -> bool:
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
    def getval(self, et: EnumType) -> Union[Enum, Iterable[Enum]]:
        return self.get(et.__name__)

    def clearval(self, et: EnumType):
        return self.clear(et.__name__)

    def clearval1(self, e: Enum):
        return self.clear1(e.__class__.__name__, e)

    def setval(self, n: Enum):
        return self.set(n.__class__.__name__, n)

    def issetval(self, n: Enum):
        return self.isset(n.__class__.__name__, n)
