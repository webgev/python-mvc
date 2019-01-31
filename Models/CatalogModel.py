from Mvc.Model import Model

class ProductModel(Model):
    table_name = 'product'
    columns = [
        {"name":"id", "type":int, "primary":True, "key":True},
        {"name":"cat_id", "type":int, "is_null":True},
        {"name":"name", "type":str},
        {"name":"price", "type":str, "is_null":True}
    ]
    indexs = [
        {"name": "name", "columns": ["name"], "type": "index"},
        {"name": "cat_id", "columns": ["cat_id"], "type": "index"}
    ]

    foregions = [
        {"name": "cat_id_link", "column": 'cat_id', "table": 'cat', "link_column": 'id', "ondelete": "cascade"}
    ]
    
class CategoryModel(Model):
    table_name = 'cat'
    columns = [
        {"name":"id", "type":int, "primary":True, "key":True},
        {"name":"name", "type":str},
    ]

class CatalogModel(Model):
    __category_model = CategoryModel()
    __product_model = ProductModel()
    
       
    def List(self):
        return self.__product_model._List()
        
    def Read(self, id):
        return self.__product_model._Read(id)
        
    def Create(self, params):
        return self.__product_model._Create(params)
        
    @staticmethod
    def ProductModel():
        return CatalogModel.__product_model
        
    def CategoryModel():
        return CatalogModel.__category_model
        