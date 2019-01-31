
from Models import models
import config
from Mvc.Auth import AuthModel
from Mvc.User import UserModel

def convert():
    config.convert = True
    UserModel().InitDB(True)
    AuthModel().InitDB(True)

    for name in models:
        x = models[name]()
        x.InitDB(True)