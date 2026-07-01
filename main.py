from __future__ import annotations

import os

from client.runtime import ClientRuntime

def _resolve_port(default: int = 5000) -> int:
	raw = os.environ.get("PORT")
	if not raw:
		return default

	try:
		return int(raw)
	except ValueError:
		return default


runtime = ClientRuntime()
runtime.dispatch()
app = runtime.app

if __name__ == "__main__":
	app.run(
		host=os.environ.get("HOST", "0.0.0.0"),
		port=_resolve_port(),
	)
