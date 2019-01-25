from mvc.Controller import Controller
from models.NewsModel import NewsModel 

class NewsApi():
    def __init__(self,):
        self.__model = NewsModel()

    def List(self):
        return self.__model._List()

    def Create(self, params):
        return self.__model._Create(params)

class NewsController(Controller):
    menu_name = "News"
    def __init__(self):
        super().__init__() 
        self.api = NewsApi()
   
    def index(self):
        news = self.api.List() 
        return self.View("news/news.html", news=news)

    def create(self):
        return self.View("news/create.html")