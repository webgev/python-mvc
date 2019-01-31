from Mvc.Model import Model
from Mvc.Sql import SqlQuery
from flask import jsonify, request, session

class UserModel(Model):
    table_name = 'User'
    columns = [
        {"name":"id", "type":int, "primary":True, "key":True}, 
        {"name":"name", "type":str},
        {"name":"login", "type":str},
        {"name":"password", "type":str},
        {"name":"email", "type":str, "is_null":True},
        {"name":"phone", "type":str, "is_null":True}
    ]

    def Find(self, **data):
        if not data:
            return
        where = []
        params = []
        columns = self.table.GetColumns()
        for field in data:
            if field in columns:
                where.append("`{}` = %s".format(field))
                params.append(data[field])

        if not where:
            return
        where = " AND ".join(where)
        return self._List(where=where, data=params)


class RolesModel(Model):
    table_name = 'Roles'
    columns = [
        {"name":"name", "type":str, "primary":True}
    ]

class UserRolesModel(Model):
    table_name = 'UserRoles'
    columns = [
        {"name":"user_id", "type":int},
        {"name":"role_name", "type":int}
    ]

    def GetUserRoles(self, user_id):
        result = self._List(columns=["role_name"], where="'user_id' = %s", data=[user_id])
        return list(rec.name for rec in result) if result else None


class User:
    user_id = None
    user = None

    def __init__(self):
        self.__user_model = UserModel()
        self.__roles_model = RolesModel()
        self.__userroles_model = UserRolesModel() 
        self.__user_roles = None

    def isAuth(self):
        return False

    def GetCurrentUserId(self):
        if not self.user_id:
            self.user_id = session.get('user_id')
        return self.user_id

    def GetUserRoles(self):
        return self.__userroles_model.GetUserRoles(user_id)
   
    def Find(self, **data):
        return self.__user_model.Find(**data)

    def GetCurrent(self):
        if self.user:
            return self.user
        user_id = self.GetCurrentUserId()
        if user_id:
            self.user = self.__user_model._Read(user_id)
            return self.user

manager = None
def UserManager(): 
    global manager
    if not manager:
        manager = User()
    return manager