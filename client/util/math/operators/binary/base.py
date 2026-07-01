from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(slots=True)
class Operator:
  symbols: list[str]

  @classmethod
  def create(cls, symbols: list[str]) -> Operator:
    return cls(symbols=symbols)
  
  @abstractmethod
  def execute(self, x, y):
    raise NotImplementedError("This method should be implemented by subclasses.")