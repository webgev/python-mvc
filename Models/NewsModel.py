from Mvc.Model import Model
from datetime import datetime
from flask import request
from Mvc.Image import SaveImage
import os
import random

class NewsModel(Model):
    table_name = "News"
    columns = [
        {"name": "id", "type":int, "primary":True, "key":True},
        {"name": "title", "type":str},
        {"name": "text", "type":str, "size": 10000},
        {"name": "img", "type":str, "is_null": True},
        {"name": "date", "type": datetime, "default": 'CURRENT_TIMESTAMP'}
    ]
    indexs = [
        {"name": "date", "columns": ["date"], "type": "index"}
    ]

    def Create(self, params):
        if not params.get('date'):
            params['date'] = datetime.now()

        logo = request.files.get('logo')
        if logo:    
            if not os.path.exists('static/news'):
                os.makedirs('static/news')

            logo_path = "static/news/"  + self.__get_img_name(logo.filename)
            SaveImage(logo, logo_path)
            params["img"] = "/" + logo_path

        self._Create(params)

    def __get_img_name(self, name):
        name = name or "image"
        name = str(random.randint(100, 900000)) +  "-" + name 

        if os.path.exists('static/news/' + name):
            n =+ 1;
            name = self.__save_img(name)

        return name 
