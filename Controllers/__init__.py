names= []
import importlib
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
names = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

controllers = {}

for name in names:
    try:
        mod = importlib.import_module("Controllers." + name)
        controllers[name] = getattr(mod, name)
    except:
        pass
