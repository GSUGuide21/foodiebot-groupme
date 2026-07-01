from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

def radians(x: number, type: str = "radians") -> number:
  if isinstance(x, complex):
    return complex(radians(x.real, type), radians(x.imag, type))
  
  match type:
    case "radians":
      return x
    case "degrees":
      return x * math.pi / 180
    case "grad" | "gradians":
      return x * math.pi / 200
    case "turn" | "turns":
      return x * 2 * math.pi
    case _:
      raise DomainError(f"Invalid type '{type}' for radians function. Valid types are 'radians', 'degrees', 'grad', 'gradians', 'turn', or 'turns'.")