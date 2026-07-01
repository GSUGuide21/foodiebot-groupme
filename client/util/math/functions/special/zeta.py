from __future__ import annotations
from client.util.math.types import number
from client.util.math.errors import DomainError

_ZETA_TOLERANCE = 1e-15
_ZETA_MAX_TERMS = 200

def _zeta_complex(s: complex) -> complex:
  if s == 1:
    raise DomainError("Zeta has a pole at s = 1.")

  denominator = 1 - (2 ** (1 - s))
  if denominator == 0:
    raise DomainError("Zeta is undefined at this input.")

  total = 0j
  for n in range(_ZETA_MAX_TERMS):
    binomial = 1
    inner = 0j
    for k in range(n + 1):
      inner += ((-1) ** k) * binomial / ((k + 1) ** s)
      if k < n:
        binomial = binomial * (n - k) // (k + 1)

    delta = inner / (2 ** (n + 1))
    total += delta
    if abs(delta) < _ZETA_TOLERANCE:
      break

  return total / denominator

def zeta(s: number) -> number:
  result = _zeta_complex(s if isinstance(s, complex) else complex(s, 0))
  if isinstance(s, complex) or abs(result.imag) > 1e-12:
    return result
  return result.real