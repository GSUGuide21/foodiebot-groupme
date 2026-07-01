from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class BotPayload:
  group_id: str
  name: str
  text: str
  user_id: str
  attachments: list[Any]