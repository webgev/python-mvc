from flask import Flask, jsonify, request, render_template, redirect, session
import importlib
import config
from basic_auth import requires_auth
from mvc.Errors import NotFound
import os
from mvc.Auth import AuthManager
from mvc.User import UserManager
from mvc.Sql import Connect

from datetime import datetime

app = Flask(__name__, template_folder="views")

    
@app.route('/auth')
@requires_auth
def authorization():
    return render_template('secret_page.html')

    
@app.route('/', defaults={'path': ''},  methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    start = datetime.now()
    Connect.Connect()
    init_session()
    try:
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
        print( str(datetime.now() - start) )
        return "404 - no method" if result == False else result
    except NotFound as ex:
        Connect.CloseConnect()
        if request.method == "GET":
            return render_template('404.html')
        else: 
            return jsonify(error = str(ex))
    except Exception as ex:
        Connect.CloseConnect()
        raise ex

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

def init_session():
    if AuthManager().IsAuth():
        sid = request.cookies.get("sid")
        user_id = sid.split("-")[0]
        user_id = int(user_id, 16)
        session['user_id'] = user_id
    else:
        session.pop('user_id', '')

app.secret_key = os.urandom(16)
if __name__ == '__main__':
    app.run(debug=config.debug)