from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass
from typing import Callable

from client.preconditions.base import Precondition

@dataclass(slots=True)
class PreconditionContext:
  sender_id: str = ""
  sender_name: str = ""
  group_id: str = ""
  token: str = ""

PreconditionHandler = Callable[[str, PreconditionContext], bool]

class PreconditionRouter:
  def __init__(self, auto_discover_extensions: bool = True) -> None:
    self.handlers: dict[str, PreconditionHandler] = {}

    if auto_discover_extensions:
      self.discover_extensions()

  def discover_extensions(self) -> None:
    package_name = "client.preconditions"
    package = importlib.import_module(package_name)

    for module_info in pkgutil.walk_packages(package.__path__, f"{package_name}."):
      name_parts = module_info.name.split(".")
      if any(part.startswith("_") for part in name_parts):
        continue

      if module_info.ispkg:
        continue

      importlib.import_module(module_info.name)

  def register_precondition(
    self,
    name: str,
    handler: PreconditionHandler,
    description: str = "",
    priority: int = 0,
  ) -> None:
    if name in self.handlers:
      raise ValueError(f"Precondition '{name}' is already registered.")
    self.handlers[name] = handler