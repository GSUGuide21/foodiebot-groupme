from os import listdir
from os.path import dirname
from importlib import import_module

preconditions = {}
files = [f for f in listdir(dirname(__file__)) if f.endswith(".py")]
files = list(filter(lambda f: f not in ["__init__.py", "base.py"], files))

for file in files:
	filename = file[0:-len(".py")]
	try:
		preconditions[filename] = import_module(f".{filename}", __name__).load()
	except ModuleNotFoundError:
		preconditions[filename] = {}