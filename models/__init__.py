names= []
import importlib
from mvc.Model import Model
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
names = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

models = {}

for name in names:
    try:
        
        mod = importlib.import_module("models." + name)
        x = dir(mod)    
        for _name in x:
            try:
                q = getattr(mod, _name)
                if issubclass(q, Model) and q != Model:
                    models[_name] = q
            except:
                pass
 
    except:
        pass