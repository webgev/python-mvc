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
            dir_name = '/static/news/' 
            url  = os.path.dirname(os.path.abspath(__file__)) + '/..' + dir_name
            if not os.path.exists(url):
                os.makedirs(url)
            name = self.__get_img_name(logo.filename)
            SaveImage(logo, url + name)
            params["img"] = dir_name + name

        self._Create(params)

    def __get_img_name(self, name):
        name = name or "image"
        name = str(random.randint(100, 900000)) +  "-" + name 

        if os.path.exists('static/news/' + name):
            n =+ 1;
            name = self.__save_img(name)

        return name 
