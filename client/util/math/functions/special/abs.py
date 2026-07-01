from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import cmath
import math

_abs = abs

def abs(x: number) -> number:
  return _abs(x)