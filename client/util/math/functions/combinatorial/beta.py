from __future__ import annotations
from client.util.math.types import number
from client.util.math.functions.combinatorial.gamma import gamma

def beta(x: number, y: number) -> number:
  return gamma(x) * gamma(y) / gamma(x + y)