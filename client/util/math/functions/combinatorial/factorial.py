from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

def factorial(x: number) -> number:
  if isinstance(x, (complex, float)) or x < 0 or not float(x).is_integer():
    raise DomainError("factorial() only accepts non-negative integers.")
  return math.factorial(x)