from __future__ import annotations
from client.util.math.types import number
from client.util.math.functions.special.erf import erf

def erfi(x: number) -> number:
  return -1j * erf(1j * x)