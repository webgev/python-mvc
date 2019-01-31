from Mvc.Controller import Controller, ControllerApi
from Mvc.Auth import AuthManager
from flask import make_response, jsonify, redirect

class AuthControllerApi(ControllerApi):
    def login(self, login, password): 
        sid = AuthManager().Authenticate(login, password)

        if sid:
            response = jsonify( result = sid )
            response.set_cookie('sid', sid)
            
            return response
        else:
            return False

class AuthController(Controller):
    api = AuthControllerApi

    def index(self):
        return self.View("auth.html")


    def exit(self):
        AuthManager().Exit()
        response = make_response(redirect('/'))
        response.set_cookie('sid', '', expires=0)
        return response
