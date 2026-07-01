from __future__ import annotations

from typing import Any

from .base import Manager, urljoin


class Member(Manager):
  def __init__(self, **options: Any):
    super().__init__(path="groups", **options)
    raw = options.get("user", options.get("member", {})) or {}

    self.group = options.get("group")
    self.token = options.get("token", getattr(self.group, "token", None))

    self.raw = raw
    self.state: dict[str, Any] = {}

    self.nick: str = raw.get("nickname", "")
    self.name: str = raw.get("name", "")
    self.id: str | int = raw.get("id", options.get("id"))
    self.user_id: str = raw.get("user_id", options.get("user_id", ""))
    self.roles: list[str] = raw.get("roles", [])
    self.muted: bool = raw.get("muted", False)
    self.avatar_url: str = raw.get("image_url", raw.get("avatar_url", ""))

  def __eq__(self, other: Any):
    if not hasattr(other, "id"):
      return False
    return self.id == other.id

  @property
  def url(self):
    if self.group is None or self.id is None:
      return Manager.url.fget(self)

    base_url = Manager.url.fget(self)
    return urljoin(base_url, f"/{self.group.group_id}/members/{self.id}")

  def kick(self):
    if self.token is None:
      raise ValueError("Cannot remove member without an access token")

    headers = {"X-Access-Token": self.token}
    response = self.POST(path="/remove", headers=headers)
    return self._json_response_or_none(response)

  def ban(self):
    if self.token is None:
      raise ValueError("Cannot ban member without an access token")
    if self.group is None or getattr(self.group, "group_id", None) is None:
      raise ValueError("Cannot ban member without a group")

    manager = Manager(path="", token=self.token)
    manager.base_url = "https://v2.groupme.com"
    headers = {"X-Access-Token": self.token}
    path = f"/groups/{self.group.group_id}/memberships/{self.id}/destroy"
    response = manager.POST(path=path, headers=headers)
    return self._json_response_or_none(response)

  @staticmethod
  def _json_response_or_none(response: Any):
    if response is None:
      return None

    try:
      payload = response.json()
    except ValueError:
      return None

    if isinstance(payload, dict):
      return payload.get("response")

    return None