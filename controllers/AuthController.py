from mvc.Controller import Controller, param, methods
from mvc.Auth import AuthManager
from flask import make_response, jsonify, redirect

class AuthController(Controller):
    def index(self):
        return self.View("auth.html")

    @param(name="login", types=[str], require = True)
    @param(name="password", types=[str], require = True)
    @methods(methods=["POST"])
    def login(self, login, password):
        sid = AuthManager().Authenticate(login, password)

        if sid:
            response = make_response(jsonify( result = sid ))
            response.set_cookie('sid', sid)
            return response
        else:
            return jsonify( result = False )


    def exit(self):
        AuthManager().Exit()
        response = make_response(redirect('/'))
        response.set_cookie('sid', '', expires=0)
        return response
