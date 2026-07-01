from dataclasses import dataclass

@dataclass(slots=True)
class Operator:
  symbols: list[str]
  position: str = 'prefix'  # Default position is 'prefix'

  def execute(self, x):
    raise NotImplementedError("This method should be implemented by subclasses.")