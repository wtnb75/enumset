from typing import Optional, Iterable
try:
    from typing import override
except ImportError:
    def override(fn):
        return fn

from enum import Enum, EnumType
from logging import getLogger
from .iface import SetIface

_log = getLogger(__name__)


class Flagset(SetIface):
    def _bits(self, key: str) -> tuple[int, int, EnumType]:
        _log.debug("bits: key %s", key)
        vt, vlen = self.keys[key]
        return vlen-len(vt), len(vt), vt

    def _num(self, key: str, e: Enum) -> int:
        cur_bits, _, _ = self._bits(key)
        pval = 1 << (list(type(e)).index(e))
        return pval << cur_bits

    def _mask(self, key: str) -> Optional[int]:
        cur_bits, bits, _ = self._bits(key)
        return ((1 << bits)-1) << cur_bits

    @override
    def get(self, key: str) -> Iterable[Enum]:
        _log.debug("get %s", key)
        cur_bits, bits, tp = self._bits(key)
        vval = (self.val >> cur_bits) & ((1 << bits)-1)
        for vv in list(tp):
            if (vval & 1) != 0:
                yield vv
            vval >>= 1

    @override
    def items(self) -> Iterable[tuple[str, Enum]]:
        cur_val = self.val
        for k, _, vt in self.iter_key():
            for vv in list(vt):
                if (cur_val & 1) != 0:
                    yield k, vv
                cur_val >>= 1

    @override
    def clear(self, key: str):
        v = self._mask(key)
        self.val &= ~(v)

    @override
    def clear1(self, key: str, e: Enum):
        n = self._num(key, e)
        self.val &= ~(n)

    @override
    def set(self, key: str, e: Enum):
        n = self._num(key, e)
        self.val |= n

    @override
    def isset(self, key: str, e: Enum):
        n = self._num(key, e)
        return (self.val & n) != 0
