from ctypes import cdll
from pathlib import Path


_libcyclops = cdll.LoadLibrary(Path(__file__).parent / "libcyclops.so")


def init():
    assert False, "NotImplemented"


def cycles() -> int:
    assert False, "NotImplemented"


class Cyclops:
    def __init__(self):
        self.cycles = 0

    def __enter__(self):
        _libcyclops.cyclops_init()
        self._enter_cycles = _libcyclops.cyclops_cycles() & 0xFFFFFFFF
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.cycles = (_libcyclops.cyclops_cycles() & 0xFFFFFFFF) - self._enter_cycles
