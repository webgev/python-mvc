from mvc.Controller import Controller, api, param, methods
from mvc.Auth import AuthManager
from flask import make_response, jsonify

class AuthController(Controller):
    def index(self):
        return self.View("auth.html")

    @param(name="login", types=[str], require = True)
    @param(name="password", types=[str], require = True)
    @methods(methods=["POST"])
    def login(self, login, password):
        sid = AuthManager().Authenticate(login, password)

        if sid:
            resp = make_response(jsonify( result = sid ))
            resp.set_cookie('sid', sid)
            return resp
        else:
            return jsonify( result = False )
