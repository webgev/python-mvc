from flask import Flask, jsonify, request, render_template, redirect, session
import config
import os
import log
from basic_auth import requires_auth
from mvc.Errors import NotFound, Warning
from mvc.Auth import AuthManager
from mvc.User import UserManager
from mvc.Sql import Connect
from controllers import controllers

from datetime import datetime

app = Flask(__name__, template_folder="views")

    
@app.route('/auth')
@requires_auth
def authorization():
    return render_template('secret_page.html')

@app.route('/api/', methods=['POST'])
def api():
    Connect.Connect()
    init_session()
    try:
        body = request.get_json()
        params = body["params"] 
        controller_name, method = body["method"].split(".")
        controller = get_controller_class(controller_name)
        if not controller:
            raise Warning("method not found")

        if not hasattr(controller, "api"):
            raise Warning("method not found")

        api = getattr(controller, "api")
        result = request_method(api(), method, **params)
        Connect.CloseConnect()
        log.LogMsg("вызов api метода: " + controller_name + "." +  method)
        return jsonify(result = result)
    except Exception as ex:
        Connect.CloseConnect()
        log.ErrorMsg(str(ex))
        return jsonify(error = str(ex)), 500

    return render_template('secret_page.html')
    
@app.route('/', defaults={'path': ''},  methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
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
        
        method = rout[1].lower() if len(rout) > 1 and rout[1] else "index"
        result = request_method(controller(), method.lower())
        Connect.CloseConnect()
        print( str(datetime.now() - start) )
        return "404 - no method" if result == False else result
    except NotFound as ex:
        Connect.CloseConnect()
        return render_template('404.html')
    except Exception as ex:
        Connect.CloseConnect()
        raise ex

def get_controller_class(controller):
    try:
        controller = upper(controller.lower()) + 'Controller'
        return controllers.get(controller)
    except ModuleNotFoundError as ex:
        raise NotFound()

        
def request_method(controller, method, **data):    
    try:
        return getattr(controller, method)(**data)
    except AttributeError as ex:
        raise NotFound("method not found")
   

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