from Models.CatalogModel import CatalogModel
from Mvc.Controller import Controller, ControllerApi, private
from flask import jsonify, request
from basic_auth import auth

class CatalogApi(ControllerApi):
    def __init__(self):
        self.model = CatalogModel()
    
    def List(self):
        return self.model.List()

    def Read(self, id):
        return self.model.Read(id)

class CatalogController(Controller):
    action = None
    menu_name = "Catalog"
    api = CatalogApi
        
    def index(self):
        items = self.api.List()
        return self.View("catalog.html", items=items)
    
    def products(self):
        return self.products2()
        
    def products2(self):
        if self.action:
            product = self.api.Read(id = self.action)
            return self.View("catalog.html", product=product)
            
        return self.index()