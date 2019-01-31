from flask import Flask, jsonify, request, render_template, redirect, session, Response
import config
import sys, os, json
import log
import traceback
from basic_auth import requires_auth
from Mvc.Errors import NotFound, Warning
from Mvc.Auth import AuthManager
from Mvc.User import UserManager
from Mvc.Sql import Connect
from Controllers import controllers

from datetime import datetime

app = Flask(__name__, template_folder="Views")

    
@app.route('/auth')
@requires_auth
def authorization():
    return render_template('secret_page.html')

@app.route('/api/', methods=['POST'])
def api():
    controller_name = ""
    method = ""
    init_session()
    try:
        if request.is_json:
            body = request.get_json()
            params = body["params"] 
        else:
            body = request.form
            params = body["params"]
            params = json.loads(params)

        controller_name, method = body["method"].split(".")
        controller = get_controller_class(controller_name)
        if not controller:
            raise Warning("method not found controller")

        if not hasattr(controller, "api"):
            raise Warning("method not found api")

        api = getattr(controller, "api")
        log.LogMsg("вызов api метода: " + controller_name + "." +  method)
        result = request_method(api(), method, **params)
        Connect.CloseConnect()
        log.LogMsg("конец вызова api метода: " + controller_name + "." +  method)
    
        return result if type(result) is Response else jsonify(result = result)
    except Exception as ex:
        Connect.CloseConnect()
        log.LogMsg("Ошибка вызова api метода: " + controller_name + "." +  method + ": " + str(ex))
        log.ErrorMsg("Ошибка вызова api метода: " + controller_name + "." +  method + ": " + str(traceback.format_exc()))
        
        error = str(traceback.format_exc()) if config.debug else str(ex)
        return jsonify(error = error), 500

    return render_template('secret_page.html')
    
@app.route('/', defaults={'path': ''},  methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def index(path):
    init_session()
    result = None
    try:
        if not path:
            path = "Home"
        rout = path.split("/")
        controller = get_controller_class(rout[0])
       
        if not controller:
            raise NotFound("404 - no controller")

        log.LogMsg("обрашение к странице: " + path)
        method = rout[1].lower() if len(rout) > 1 and rout[1] else "index"
        result = request_method(controller(), method.lower())
        log.LogMsg("конец обращения к странице: " + path)
        if result == False:
            raise NotFound("404 - no method")
    except NotFound as ex:
        result = render_template('404.html', message=str(ex))
    except Exception as ex:
        Connect.CloseConnect()
        raise ex
    
    Connect.CloseConnect()
    return result

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
        raise NotFound("error: " + str(controller)+ " " + method + " " + str(data) + " - " + str(ex))
   

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