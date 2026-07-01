from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError
from typing import Optional

_round = round

def round(x: number, precision: Optional[int] = None) -> number:
  if isinstance(x, complex):
      return complex(_round(x.real, precision), _round(x.imag, precision))
  return _round(x, precision)