from mvc.Model import Model
from mvc.User import UserManager
from flask import request
from mvc.Sql import SqlQuery
import uuid

import config
from datetime import datetime

class AuthModel(Model):
    def __init__(self):
        if config.redis:
            pass
        else:
            self.columns = [
                {"name":"session_id", "type":str, "primary":True},
                {"name":"date", "type":datetime},
            ]
            self.table_name = "Session"

        super().__init__()

    def Delete(self, sid):
        if config.redis:
            pass
        else:
            SqlQuery("delete from `Session` where `session_id` = %s ", [sid])

class Auth():
    is_auth = None
    def __init__(self):
        self.__model = AuthModel()

    def Authenticate(self, login, password):
        user = UserManager().Find(login=login, password=password)
        if not user:
            return False
        user = user[0]
        user_hex = "0000000" + hex(user["id"])[2:]  
        sid = user_hex[-8:] + "-" + str(uuid.uuid4())
        if config.redis:
            pass
        else:
            self.__model._Create({
                "session_id": sid,
                "date": datetime.now()
            })

        return sid

    def IsAuth(self):
        if self.is_auth is not None:
            return self.is_auth
        self.is_auth = bool(self.__model._Read(request.cookies.get("sid")))
        return self.is_auth

    def Exit(self):
        if config.redis:
            pass
        else:
            sid = request.cookies.get("sid")
            if not sid:
                return

            self.__model.Delete(sid)

manager = None
def AuthManager():
    return manager or Auth()