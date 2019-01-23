from mvc.Controller import Controller
from models.NewsModel import NewsModel 

class NewsController(Controller):
    menu_name = "News"
    def __init__(self):
        super().__init__() 
        self.__model = NewsModel()
        
    def index(self):
        news = self.__model._List() 
        return self.View("news/news.html", news=news)

    def create(self):
        return self.View("news/create.html")

    def create_api(self, params):
        self.__model._Create(params)