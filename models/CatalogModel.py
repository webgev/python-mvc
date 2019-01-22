from mvc.Model import Model

class ProductModel(Model):
    table_name = 'product'
    columns = [
        {"name":"id", "type":int, "primary":True, "key":True},
        {"name":"cat_id", "type":int, "is_null":True},
        {"name":"name", "type":str},
        {"name":"price", "type":str, "is_null":True}
    ]
    
class CategoryModel(Model):
    table_name = 'cat'
    columns = [
        {"name":"id", "type":int, "primary":True, "key":True},
        {"name":"name", "type":str},
    ]

class CatalogModel(Model):
    __product_model = ProductModel()
    __category_model = CategoryModel()
       
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
        