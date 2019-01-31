from flask import Flask, jsonify, request, render_template
from Mvc.Controller import Controller

class HomeController(Controller):
    menu_name = "Home"
    def index(self):
        return self.View("index.html", path="sss", sss="xxx")