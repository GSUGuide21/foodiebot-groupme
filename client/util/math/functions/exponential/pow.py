from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

def pow(x: number, y: number) -> number:
  if isinstance(x, complex) or isinstance(y, complex):
    return x ** y
  try:
    return math.pow(x, y)
  except ValueError:
    return x ** y