from mvc.Controller import Controller, ControllerApi, private, modelparam
from models.NewsModel import NewsModel 

class NewsApi(ControllerApi):
    def __init__(self,):
        self.model = NewsModel()

    def List(self):
        return self.model._List()

    @modelparam()
    def Create(self, params):
        return self.model.Create(params)

class NewsController(Controller):
    menu_name = "News"
    api = NewsApi
   
    def index(self):
        self.inner = True
        news = self.api.List() 
        return self.View("news/news.html", news=news)

    def create(self):
        return self.View("news/create.html")

    @private
    def get_create_url(self):
        return "/news/create/"