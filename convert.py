
from Models import models
import config
from Mvc.Auth import AuthModel
from Mvc.User import UserModel
from Mvc.Sql import Connect

if __name__ == '__main__':
    config.convert = True
    UserModel().InitDB(True)
    AuthModel().InitDB(True)

    for name in models:
        x = models[name]()
        x.InitDB(True)

    Connect.CloseConnect()