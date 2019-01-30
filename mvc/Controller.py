from flask import jsonify, request, render_template
from mvc.Errors import NotFound
from mvc.User import UserManager
from mvc.Menu import get_menu

def methods(methods=None):
    def my_decorator(function_to_decorate):
        def the_wrapper_around_the_original_function(self, **data):
            if not self.inner and request.method not in (methods or ["GET"]):
                raise NotFound()
            
            return function_to_decorate(self, **data)
        return the_wrapper_around_the_original_function
    return my_decorator

def private(function_to_decorate):
    def the_wrapper_around_the_original_function(self, *data):
        if self.inner == False:
            raise NotFound()
        return function_to_decorate(self, *data) 
    return the_wrapper_around_the_original_function

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
    
def modelparam():
    def my_decorator(function_to_decorate):
        def the_wrapper_around_the_original_function(self, **data):   
            if not self.model.CheckModel(data):
                raise Exception("param not model - %s" % (str(self.model)))   
            return function_to_decorate(self, data) 
        return the_wrapper_around_the_original_function
    return my_decorator

class ControllerApi:
    inner = False

class Controller:
    inner = False
    controller = 'home'
    api = None
    def __init__(self):
        if self.api:
            self.api = self.api()
            self.api.inner = True

        path = request.path.split("/")
        path = list(filter(lambda a: a != '', path))
        if path:
            self.controller = path[0]
            self.method = path[1] if len(path) > 1 else None
            self.action = path[2] if len(path) > 2 else None
            self.dops = list(p for p in path[3:] if p) if len(path) > 3 else []

    def View(self, page, **data):
        user = UserManager().GetCurrent() or {}
        return render_template(
            page, 
            menu=get_menu(), 
            active_page=self.controller, 
            user=user, 
            controller=self,
            **data
        )