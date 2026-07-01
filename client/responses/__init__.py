from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import inspect
import importlib
import pkgutil

from typing import Callable
from dataclasses import dataclass

import re

from client.responses.base import Response
from client.responses.parser import ResponseParser, TargetSpec
from client.responses.result import ResponseResult, ResponseResultLike
from client.responses.triggers import ParsedTrigger, TriggerParser
from client.parser import ParsedMessage, Parser

def _normalize_phrase(text: str) -> str:
  lowered = text.lower().strip()
  lowered = re.sub(r"[^a-z0-9\s]", "", lowered)
  return re.sub(r"\s+", " ", lowered).strip()

_PHRASE_RESPONSES: dict[str, str] = {
  "what is your name": "I'm FoodieBot.",
  "whats your name": "I'm FoodieBot.",
  "good morning": "Good morning!",
}


def phrase_response(text: str | None) -> str | None:
  normalized = _normalize_phrase(str(text or ""))
  if not normalized:
    return None
  return _PHRASE_RESPONSES.get(normalized)

@dataclass(slots=True)
class ResponseContext:
  sender_id: str = ""
  sender_name: str = ""
  group_id: str = ""
  message_id: str = ""
  token: str = ""

ResponseHandler = Callable[[ParsedMessage, ResponseContext], ResponseResultLike]


def _dispatch_response(
  handler: ResponseHandler | None,
  response_name: str,
  normalized_text: str,
  context: ResponseContext,
) -> ResponseResultLike | None:
  if handler is None:
    return None

  parsed = ParsedMessage(raw=normalized_text, command=response_name)
  return handler(parsed, context)

class ResponseRouter:
  def __init__(self, auto_discover_extensions: bool = True) -> None:
    self.handlers: dict[str, ResponseHandler] = {}
    self.response_descriptions: dict[str, str] = {}
    self.response_timeouts: dict[str, float | None] = {}
    self.response_parser = ResponseParser()
    self.trigger_parser = TriggerParser()
    self._loaded_extensions: set[str] = set()
    self._executor = ThreadPoolExecutor(max_workers=4)

    if auto_discover_extensions:
      self.discover_extensions()

  def register(
    self,
    name: str,
    handler: ResponseHandler,
    description: str = "",
    targets: list[TargetSpec] | None = None,
    triggers: list[str] | None = None,
    priority: int = 0,
    timeout_seconds: float | None = None,
  ) -> None:
    response_name = name.lower()
    self.handlers[response_name] = handler
    self.response_descriptions[response_name] = description.strip()
    self.response_timeouts[response_name] = timeout_seconds
    self.response_parser.register(response_name, targets, priority=priority)
    self.trigger_parser.register(response_name, triggers, priority=priority)

  def register_response(self, response: Response) -> None:
    response.register(self)

  def list_responses(self) -> list[str]:
    return sorted(self.handlers.keys())

  def load_extensions(self, module_name: str) -> bool:
    if module_name in self._loaded_extensions:
      return False

    try:
      module = importlib.import_module(module_name)
      response_classes = [
        obj
        for obj in vars(module).values()
        if inspect.isclass(obj) and issubclass(obj, Response) 
        and obj is not Response
        and obj.__module__ == module.__name__
      ]
    except ImportError:
      return False

    if not response_classes:
      raise ValueError(f"No Response subclasses found in module '{module_name}'.")

    for response_class in sorted(response_classes, key=lambda cls: cls.__name__):
      response_instance = response_class.create(self)
      self.register_response(response_instance)

    self._loaded_extensions.add(module_name)
    return True
  
  @property
  def loaded_extensions(self) -> tuple[str, ...]:
    return tuple(sorted(self._loaded_extensions))

  def discover_extensions(self, package_name: str = "client.responses.extensions") -> list[str]:
    package = importlib.import_module(package_name)
    loaded: list[str] = []

    for module_info in pkgutil.walk_packages(package.__path__, f"{package_name}."):
      name_parts = module_info.name.split(".")
      if any(part.startswith("_") for part in name_parts):
        continue

      if module_info.ispkg:
        continue
      try:
        if self.load_extensions(module_info.name):
          loaded.append(module_info.name)
      except ValueError:
        # Ignore non-extension modules that do not expose a Response subclass.
        continue

    return loaded
  
  def handle(
    self,
    text: str | None,
    sender_id: str = "",
    sender_name: str = "",
    group_id: str = "",
    message_id: str = "",
    token: str = "",
  ) -> ResponseResultLike:
    normalized_text = str(text or "").strip()
    context = ResponseContext(
      sender_id=sender_id,
      sender_name=sender_name,
      group_id=group_id,
      message_id=message_id,
      token=token,
    )

    target_match = self.response_parser.parse(normalized_text)
    if target_match:
      return _dispatch_response(
        self.handlers.get(target_match.name),
        target_match.name,
        normalized_text,
        context,
      )

    trigger_match = self.trigger_parser.parse(normalized_text)
    if trigger_match:
      return _dispatch_response(
        self.handlers.get(trigger_match.name),
        trigger_match.name,
        normalized_text,
        context,
      )

    parsed = Parser().parse(normalized_text)
    if not parsed:
      return phrase_response(text)

    response_name = parsed.command.lower()
    handler = self.handlers.get(response_name)
    if not handler:
      return phrase_response(text)

    return handler(parsed, context)
  
__all__ = [
  "ResponseContext",
  "ResponseHandler",
  "ResponseRouter",
  "ResponseResult",
  "ResponseResultLike"
]