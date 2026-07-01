from __future__ import annotations

from client.commands.base import Command

def help_message(
  prefix: str,
  commands: list[str] | None = None,
  command_groups: dict[str, list[str]] | None = None,
) -> str:
  if command_groups:
    lines: list[str] = ["Available commands by category:"]
    for category, category_commands in command_groups.items():
      if not category_commands:
        continue

      lines.append("")
      lines.append(f"{category}:")
      lines.extend(category_commands)

    if len(lines) > 1:
      return "\n".join(lines)

  command_lines = commands or []
  if not command_lines:
    command_lines = [f"{prefix}help - Show available commands"]

  return "\n".join(["Available commands:", *command_lines])

class HelpCommand(Command):
  name = "help"
  description = "Show available commands"

  def __init__(self, router):
    self.router = router

  def execute(self, message, context):
    return help_message(context.prefix, command_groups=self.router.list_command_groups())

  @classmethod
  def create(cls, router):
    return cls(router)
