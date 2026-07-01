from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

import math

def grad(x: number, type: str = "radians") -> number:
  if isinstance(x, complex):
    return complex(grad(x.real, type), grad(x.imag, type))

  match type:
    case "radians":
      return x * 200 / math.pi
    case "degrees":
      return x * 10 / 9
    case "turn" | "turns":
      return x * 400
    case "grad" | "gradians":
      return x
    case _:
      raise DomainError(f"Invalid type '{type}' for grad function. Valid types are 'radians', 'degrees', 'grad', 'gradians', 'turn', or 'turns'.")