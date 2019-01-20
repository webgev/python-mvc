from flask import Flask, jsonify, request, render_template, redirect
import importlib
import config
from  mvc.Sql import Connect
from basic_auth import requires_auth
from mvc.Errors import NotFound

app = Flask(__name__, template_folder="views")
    
@app.route('/auth')
@requires_auth
def authorization():
    return render_template('secret_page.html')

    
@app.route('/', defaults={'path': ''},  methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    try:
        Connect.Connect()
        if not path:
            path = "Home"
        rout = path.split("/")
        controller = get_controller_class(rout[0])
       
        if not controller:
            Connect.CloseConnect()
            return "404 - no controller"
        
        params = request.get_json() if request.method == "POST" else {}
        result = request_method(controller, rout[1].lower() if len(rout) > 1 and rout[1] else "index", **params)
        Connect.CloseConnect()
        return "404 - no method" if result == False else result
    except NotFound as ex:
        if request.method == "GET":
            return render_template('404.html')
        else: 
            return jsonify(error = str(ex))
def get_controller_class(controller):
    try:
        controller = upper(controller.lower()) + 'Controller'
        mod = importlib.import_module("controllers." + controller)
        return getattr(mod, controller)
    except ModuleNotFoundError as ex:
        raise NotFound()
        
def request_method(controller, method, **data):    
    try:
        return getattr(controller(), method.lower())(**data)
    except AttributeError as ex:
        raise NotFound()
   

def upper(value):
    return value[0].upper() + value[1:]
 
def raise_error(ex):
    if config.debug:
        raise ex

if __name__ == '__main__':
    app.run(debug=config.debug)