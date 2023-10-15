from typing import Iterable, Optional
try:
    from typing import override
except ImportError:
    # Python <3.12
    def override(fn):
        return fn
from enum import Enum
from logging import getLogger
from .iface import SetIface

_log = getLogger(__name__)


class Enumset(SetIface):
    def _num(self, key: str, e: Enum) -> int:
        pval = list(type(e)).index(e) + 1
        for k, _, vt in self.iter_key():
            vlen = len(vt) + 1
            if k == key:
                _log.debug("num %s/%s -> %s", key, e, pval)
                return pval
            pval *= vlen
        raise KeyError(f"key {key} not found")

    @override
    def get(self, key: str) -> Optional[Enum]:
        cur_val = self._val
        for k, _, vt in self.iter_key():
            _log.debug("get iter_key: %s/%s/len=%s", k, vt, len(vt))
            vlen = len(vt) + 1
            if k == key:
                vv = cur_val % vlen
                if vv == 0:
                    _log.debug("not set: key=%s", key)
                    return None
                _log.debug("set: key=%s, nth=%s", key, vv)
                return list(vt)[vv-1]
            cur_val //= vlen
        raise KeyError(f"key {key} not found")

    @override
    def items(self) -> Iterable[tuple[str, Enum]]:
        cur_val = self._val
        for k, _, vt in self.iter_key():
            _log.debug("items iter_key: %s/%s/len=%s/val=%s",
                       k, vt, len(vt), cur_val)
            vlen = len(vt) + 1
            vv = cur_val % vlen
            if vv != 0:
                yield k, list(vt)[vv-1]
            cur_val //= vlen

    @override
    def clearkey(self, key: str) -> bool:
        _log.debug("clearkey %s", key)
        v = self.get(key)
        if v is not None:
            n = self._num(key, v)
            self._val -= n
            return True
        return False

    @override
    def clear1(self, key: str, e: Enum) -> bool:
        _log.debug("clear1 %s/%s", key, e)
        v = self.get(key)
        if v == e:
            n = self._num(key, v)
            self._val -= n
            return True
        return False

    def set(self, key: str, n: Enum) -> bool:
        _log.debug("set %s/%s", key, n)
        res = self.clearkey(key)
        self._val += self._num(key, n)
        _log.debug("clear? %s", res)
        return res

    def isset(self, key: str, n: Enum):
        _log.debug("isset %s/%s", key, n)
        return self.get(key) == n
