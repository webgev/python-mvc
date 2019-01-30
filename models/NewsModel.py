from mvc.Model import Model
from datetime import datetime
from flask import request

class NewsModel(Model):
    table_name = "News"
    columns = [
        {"name": "id", "type":int, "primary":True, "key":True},
        {"name": "title", "type":str},
        {"name": "text", "type":str, "size": 10000},
        {"name": "img", "type":str, "is_null": True},
        {"name": "date", "type": datetime, "default": 'CURRENT_TIMESTAMP'}
    ]

    def Create(self, params):
        if not params.get('date'):
            params['date'] = datetime.now()
        logo_path = "static/news/aasa.png"
        logo = request.files.get('logo')
        logo.save(logo_path)
        params["img"] = "/" + logo_path
        self._Create(params)