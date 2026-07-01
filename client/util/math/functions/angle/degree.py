from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

def degree(x: number, type: str = "radians") -> number:
  if isinstance(x, complex):
    return complex(degree(x.real, type), degree(x.imag, type))

  match type:
    case "radians":
      return x * 180 / math.pi
    case "grad" | "gradians":
      return x * 9 / 10
    case "turn" | "turns":
      return x * 360
    case "degrees":
      return x
    case _:
      raise DomainError(f"Invalid type: {type}. Must be 'radians', 'degrees', 'grad', 'gradians', 'turn', or 'turns'.")