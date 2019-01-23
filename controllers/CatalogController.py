from models.CatalogModel import CatalogModel
from mvc.Controller import Controller, private, api, param, modelparam
from flask import jsonify, request
from basic_auth import auth

class CatalogController(Controller):
    model = None
    action = None
    menu_name = "Catalog"
    
    def __init__(self):
        super().__init__() 
        self.model = CatalogModel()
        
    def index(self):
        self.inner = True
        items = self.get_products()
        return self.View("catalog.html", items=items)
    
    def products(self):
        self.inner = True
        return self.products2()
        
    @private
    def products2(self):
        if self.action:
            product = self.get_product(id = self.action)
            return self.View("catalog.html", product=self.model.Read(self.action))
            
        return self.index()
        
    @api(methods=["POST"])
    def get_products(self):
        return self.model.List()
    
    @param(name="id", types=[int], require=True)
    @api()
    def get_product(self, id):
        return self.model.Read(id)
    
    #@auth(roles=["admin"])
    @modelparam(name="params", model=CatalogModel.ProductModel())
    @api()
    def create_product(self, params):
        return self.model.Create(params)