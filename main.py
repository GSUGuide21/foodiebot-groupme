from __future__ import annotations

import os

from client.runtime import ClientRuntime


def _should_send_initializer() -> bool:
	if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
		return True

	return not bool(os.environ.get("FLASK_RUN_FROM_CLI"))

def _resolve_port(default: int = 5000) -> int:
	raw = os.environ.get("PORT")
	if not raw:
		return default

	try:
		return int(raw)
	except ValueError:
		return default


runtime = ClientRuntime()
runtime.dispatch(send_init=_should_send_initializer())
app = runtime.app

if __name__ == "__main__":
	app.run(
		host=os.environ.get("HOST", "0.0.0.0"),
		port=_resolve_port(),
	)
