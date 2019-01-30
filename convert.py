
from models import models
from mvc.Sql import Connect
import config

def convert():
    config.convert = True
    Connect.Connect()
    for name in models:
        x = models[name]()
        x.InitDB(True)