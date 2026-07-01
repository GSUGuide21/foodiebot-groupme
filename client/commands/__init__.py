from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import inspect
import importlib
import pkgutil
from dataclasses import dataclass
from typing import Callable

from client.commands.base import Command
from client.commands.result import CommandResult, CommandResultLike
from client.preconditions.base import Precondition
from client.parser import ParsedMessage, Parser

def unknown_command(command_name: str, prefix: str) -> str:
  return (
    f"Unknown command: {command_name}. "
    f"Try {prefix}help for a list of available commands."
  )

def command_error(message: str) -> str:
  return message.strip() or "Unable to process that command."

def command_timeout(command_name: str, timeout_seconds: float | None) -> str:
  if timeout_seconds is None:
    return f"{command_name}: the command timed out."
  return f"{command_name}: timed out after {timeout_seconds:g}s. Please try again."

from client.responses import (
  phrase_response
)


@dataclass(slots=True)
class CommandContext:
  prefix: str
  sender_id: str = ""
  group_id: str = ""
  token: str = ""


CommandHandler = Callable[[ParsedMessage, CommandContext], CommandResultLike]


class CommandRouter:
  _CATEGORY_ORDER: dict[str, int] = {
    "Core": 0,
    "Utilities": 1,
    "Moderation": 2,
    "Scheduling": 3,
    "Games": 4,
    "Fun": 5,
    "External": 6,
    "General": 99,
  }

  _COMMAND_CATEGORIES: dict[str, str] = {
    "help": "Core",
    "ping": "Core",
    "echo": "Utilities",
    "capitalize": "Utilities",
    "calc": "Utilities",
    "me": "Utilities",
    "everyone": "Utilities",
    "kick": "Moderation",
    "ban": "Moderation",
    "readd": "Moderation",
    "calendar": "Scheduling",
    "blackjack": "Games",
    "coin": "Games",
    "roll": "Games",
    "choose": "Games",
    "random": "Games",
    "dance": "Fun",
    "parrot": "Fun",
    "herewego": "Fun",
    "reddit": "External",
    "youtube": "External",
  }

  def __init__(self, prefix: str = "$", auto_discover_extensions: bool = True):
    self.prefix = prefix
    self.parser = Parser(prefix=prefix)
    self.handlers: dict[str, CommandHandler] = {}
    self.command_descriptions: dict[str, str] = {}
    self.command_aliases: dict[str, list[str]] = {}
    self.command_preconditions: dict[str, list[Precondition]] = {}
    self.command_categories: dict[str, str] = {}
    self.command_timeouts: dict[str, float | None] = {}
    self._loaded_extensions: set[str] = set()
    self._executor = ThreadPoolExecutor(max_workers=8)

    if auto_discover_extensions:
      self.discover_extensions()

  def set_prefix(self, prefix: str) -> None:
    self.prefix = prefix
    self.parser.set_prefix(prefix)

  def register(
    self,
    name: str,
    handler: CommandHandler,
    preconditions: list[Precondition] | None = None,
    description: str = "",
    aliases: list[str] | None = None,
    category: str = "General",
    timeout_seconds: float | None = None,
  ) -> None:
    command_name = name.lower()
    normalized_category = category.strip() or "General"
    if normalized_category == "General":
      normalized_category = self._category_for_command(command_name)

    self.handlers[command_name] = handler
    self.command_descriptions[command_name] = description.strip()
    self.command_preconditions[command_name] = preconditions or []
    self.command_categories[command_name] = normalized_category
    self.command_timeouts[command_name] = timeout_seconds

    normalized_aliases: list[str] = []
    for alias in aliases or []:
      alias_name = alias.lower().strip()
      if not alias_name:
        continue
      self.handlers[alias_name] = handler
      self.command_preconditions[alias_name] = self.command_preconditions[command_name]
      self.command_categories[alias_name] = self.command_categories[command_name]
      self.command_timeouts[alias_name] = timeout_seconds
      normalized_aliases.append(alias_name)

    self.command_aliases[command_name] = sorted(set(normalized_aliases))

  def register_command(self, command: Command) -> None:
    command.register(self)

  def _category_for_command(self, command_name: str) -> str:
    return self._COMMAND_CATEGORIES.get(command_name, "General")

  def _category_sort_key(self, category_name: str) -> tuple[int, str]:
    return (self._CATEGORY_ORDER.get(category_name, 98), category_name.lower())

  def list_command_lines(self) -> list[str]:
    lines: list[str] = []
    for command_name in sorted(self.command_descriptions.keys()):
      description = self.command_descriptions.get(command_name, "")
      aliases = self.command_aliases.get(command_name, [])

      suffix = f" - {description}" if description else ""
      if aliases:
        suffix = f"{suffix} (aliases: {', '.join(aliases)})" if suffix else f" (aliases: {', '.join(aliases)})"

      lines.append(f"{self.prefix}{command_name}{suffix}")

    return lines

  def list_command_groups(self) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}

    for command_name in sorted(self.command_descriptions.keys()):
      category = self.command_categories.get(command_name) or self._category_for_command(command_name)
      description = self.command_descriptions.get(command_name, "")
      aliases = self.command_aliases.get(command_name, [])

      suffix = f" - {description}" if description else ""
      if aliases:
        suffix = f"{suffix} (aliases: {', '.join(aliases)})" if suffix else f" (aliases: {', '.join(aliases)})"

      grouped.setdefault(category, []).append(f"{self.prefix}{command_name}{suffix}")

    return dict(sorted(grouped.items(), key=lambda item: self._category_sort_key(item[0])))

  def load_extension(self, module_name: str) -> bool:
    if module_name in self._loaded_extensions:
      return False

    module = importlib.import_module(module_name)
    command_classes = [
      obj
      for obj in vars(module).values()
      if inspect.isclass(obj)
      and issubclass(obj, Command)
      and obj is not Command
      and obj.__module__ == module.__name__
    ]

    if not command_classes:
      raise ValueError(f"Command extension '{module_name}' must define a Command subclass")

    for command_cls in sorted(command_classes, key=lambda cls: cls.__name__):
      self.register_command(command_cls.create(self))

    self._loaded_extensions.add(module_name)
    return True

  @property
  def loaded_extensions(self) -> tuple[str, ...]:
    return tuple(sorted(self._loaded_extensions))

  def discover_extensions(self, package_name: str = "client.commands.extensions") -> list[str]:
    package = importlib.import_module(package_name)
    loaded: list[str] = []

    for module_info in pkgutil.walk_packages(package.__path__, package_name + "."):
      name_parts = module_info.name.split(".")
      if any(part.startswith("_") for part in name_parts):
        continue

      if module_info.ispkg:
        continue

      try:
        if self.load_extension(module_info.name):
          loaded.append(module_info.name)
      except ValueError:
        # Ignore non-extension modules that do not expose a Command subclass.
        continue

    return loaded

  def handle(
    self,
    text: str | None,
    sender_id: str = "",
    group_id: str = "",
    token: str = "",
  ) -> CommandResultLike:
    parsed = self.parser.parse(text)
    if not parsed:
      return phrase_response(text)

    command_name = parsed.command
    handler = self.handlers.get(command_name)
    if handler is None:
      return unknown_command(command_name, self.prefix)

    context = CommandContext(
      prefix=self.prefix,
      sender_id=sender_id,
      group_id=group_id,
      token=token,
    )

    for precondition in self.command_preconditions.get(command_name, []):
      passed, message = precondition.handle(parsed, context)
      if not passed:
        return message

    try:
      timeout_seconds = self.command_timeouts.get(command_name)

      if timeout_seconds is None:
        return handler(parsed, context)

      future = self._executor.submit(handler, parsed, context)
      return future.result(timeout=timeout_seconds)
    except FutureTimeoutError:
      timeout_seconds = self.command_timeouts.get(command_name)
      return command_timeout(command_name, timeout_seconds)
    except ValueError as exc:
      return command_error(str(exc))
    except Exception:
      return command_error("The command failed unexpectedly. Please try again.")


__all__ = ["CommandContext", "CommandHandler", "CommandResult", "CommandResultLike", "CommandRouter"]
