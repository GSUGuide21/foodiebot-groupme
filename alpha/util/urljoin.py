from urllib import parse

def urljoin(base_url, path=None):
	if path == None:
		url = base_url
	else:
		url = "{base}/".format(base=base_url) if not base_url.endswith("/") else base_url
		url = parse.urljoin(base_url, str(path))

	return url