from __future__ import annotations
from client.util.math.types import number
from client.util.math.functions.special.erf import erf

def erfc(x: number) -> number:
  return 1 - erf(x)