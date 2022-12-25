from urllib import parse

def urljoin(base: str, path=None):
	if path == None or path == "": return base
	path = path if path.startswith("/") else f"/{path}"
	base = base if base.endswith("/") else f"{path}/"
	return parse.urljoin(base, str(path))