from __future__ import annotations

from typing import Any

import requests


def urljoin(base: str, path: str | None = None) -> str:
  if path is None or path == "":
    return base

  base = base if base.endswith("/") else f"{base}/"
  path = path.lstrip("/")
  return requests.compat.urljoin(base, path)


class Manager:
  base_url = "https://api.groupme.com/v3"

  def __init__(self, **options: Any):
    self.path = options.get("path")
    self.token = options.get("token")

  def __getitem__(self, key: str):
    return getattr(self, key)

  def __setitem__(self, key: str, value: Any):
    return setattr(self, key, value)

  def __str__(self):
    return self.url

  def __repr__(self):
    return f"{self.__class__.__name__}({self.url})"

  @property
  def url(self):
    return urljoin(self.base_url, self.path)

  def GET(self, path: str | None = None, **params: Any):
    url = urljoin(self.url, path)
    return requests.get(url, **params)

  def POST(self, path: str | None = None, **params: Any):
    url = urljoin(self.url, path)
    return requests.post(url, **params)

  def PATCH(self, path: str | None = None, **params: Any):
    url = urljoin(self.url, path)
    return requests.patch(url, **params)

  def PUT(self, path: str | None = None, **params: Any):
    url = urljoin(self.url, path)
    return requests.put(url, **params)

  def DELETE(self, path: str | None = None, **params: Any):
    url = urljoin(self.url, path)
    return requests.delete(url, **params)