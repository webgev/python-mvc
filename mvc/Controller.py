from flask import jsonify, request, render_template
from mvc.Errors import NotFound

def private(function_to_decorate):
    def the_wrapper_around_the_original_function(self, *data):
        if self.inner == False:
            raise NotFound()
        return function_to_decorate(self, *data) 
    return the_wrapper_around_the_original_function
    
def api(methods=None):
    def my_decorator(function_to_decorate):
        def the_wrapper_around_the_original_function(self, **data):
            if not self.inner and request.method not in (methods or ["POST"]):
                raise NotFound()
            
            result = function_to_decorate(self, **data)
            return result if self.inner else jsonify( result = result )
        return the_wrapper_around_the_original_function
    return my_decorator

def param(name, types, require=False):
    def my_decorator(function_to_decorate):
        def the_wrapper_around_the_original_function(self, **data):
            if require and name not in data:
                raise NotFound("param '%s' not found" % (name))
            if name in data and data.get(name) != None:
                if type(data.get(name)) not in types:
                    if not str(data.get(name)).isdigit() or type(int(data.get(name))) not in types:
                        raise NotFound("param '%s' not type - %s" % (name, str(types)))
                    
            return function_to_decorate(self, **data) 
        return the_wrapper_around_the_original_function
    return my_decorator
    
def modelparam(name, model, require=None):
    def my_decorator(function_to_decorate):
        def the_wrapper_around_the_original_function(self, **data):
            if not model or name not in data or type(data.get(name)) is not dict:
                raise NotFound("param '%s' not found" % (name))
                
            if not model.CheckModel(data.get(name)):
                raise NotFound("param '%s' not model - %s" % (name, str(model)))
                    
            return function_to_decorate(self, **data) 
        return the_wrapper_around_the_original_function
    return my_decorator
    
class Controller:
    inner = False
    def __init__(self):
        path = request.path.split("/")
        path = list(filter(lambda a: a != '', path))
        if path:
            self.controller = path[0]
            self.method = path[1] if len(path) > 1 else None
            self.action = path[2] if len(path) > 2 else None
            self.dops = list(p for p in path[3:] if p) if len(path) > 3 else []

    def View(self, page, **data):
        return render_template(page, **data)
        
 