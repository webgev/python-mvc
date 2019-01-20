from flask import Flask, jsonify, request, render_template
from mvc.Controller import Controller

class HomeController(Controller):
    def index(self):
        return self.View("index.html", path="sss", sss="xxx")