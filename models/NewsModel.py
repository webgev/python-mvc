from mvc.Model import Model
from datetime import datetime

class NewsModel(Model):
    table_name = "News"
    columns = [
        {"name": "id", "type":int, "primary":True, "key":True},
        {"name": "title", "type":str},
        {"name": "text", "type":str, "size": 10000},
        {"name": "date", "type": datetime}
    ]