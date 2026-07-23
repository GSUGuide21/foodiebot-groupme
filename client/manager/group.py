from __future__ import annotations

from typing import Any

from .base import Manager, urljoin


class Group(Manager):
  def __init__(self, group_id: str, **options: Any):
    super().__init__(path="groups", **options)
    self.group_id = group_id
    self.owner = None
    self.admins: dict[str, Any] = {}
    self.members: dict[str, Any] = {}

  def __eq__(self, other: Any):
    if not hasattr(other, "group_id"):
      return False
    return self.group_id == other.group_id

  @property
  def url(self):
    base_url = Manager.url.fget(self)
    return urljoin(base_url, self.group_id)

  def get_messages(self):
    headers = {"X-Access-Token": self.token}
    response = self.GET(headers=headers, path="/messages").json()["response"]
    return [response_message for response_message in response["messages"]]

  def get(self):
    headers = {"X-Access-Token": self.token}
    response = self.GET(headers=headers)
    return self._json_response_or_payload(response)

  def get_members(self) -> list[dict[str, Any]]:
    payload = self.get()
    if not isinstance(payload, dict):
      return []

    members = payload.get("members")
    if not isinstance(members, list):
      return []

    return [member for member in members if isinstance(member, dict)]

  def list_subgroups(self, page: int = 1, per_page: int = 10) -> list[dict[str, Any]]:
    headers = {"X-Access-Token": self.token}
    params = {
      "page": max(1, int(page)),
      "per_page": max(1, int(per_page)),
    }
    response = self.GET(headers=headers, path="/subgroups", params=params)
    payload = self._json_response_or_payload(response)

    if isinstance(payload, list):
      return [subgroup for subgroup in payload if isinstance(subgroup, dict)]

    if not isinstance(payload, dict):
      return []

    subgroups = payload.get("subgroups")
    if isinstance(subgroups, list):
      return [subgroup for subgroup in subgroups if isinstance(subgroup, dict)]

    response_value = payload.get("response")
    if isinstance(response_value, list):
      return [subgroup for subgroup in response_value if isinstance(subgroup, dict)]

    return []

  def update(self, **options: Any):
    headers = {"X-Access-Token": self.token}
    return self.POST(headers=headers, path="/update", **options).json()["response"]

  def destroy(self):
    headers = {"X-Access-Token": self.token}
    return self.POST(headers=headers, path="/destroy").json()["response"]

  def add_member(self, **options: Any):
    headers = {"X-Access-Token": self.token}
    response = self.POST(headers=headers, path="/members/add", **options)
    return self._json_response_or_payload(response)

  def readd_member(self, user_id: str, nickname: str, guid: str | None = None):
    member: dict[str, str] = {
      "user_id": str(user_id),
      "nickname": str(nickname),
    }
    if guid:
      member["guid"] = str(guid)

    return self.add_member(json={"members": [member]})
  
  def delete_message(self, message_id: str):
    headers = {"X-Access-Token": self.token}
    return self.POST(headers=headers, path=f"/messages/{message_id}/delete").json()["response"]

  @staticmethod
  def _json_response_or_payload(response: Any):
    if response is None:
      return None

    try:
      payload = response.json()
    except ValueError:
      return None

    if not isinstance(payload, dict):
      return payload

    if "response" in payload:
      return payload.get("response")

    return payload