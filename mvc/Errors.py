
class NotFound(Exception):
    def __init__(self, text=None):
        pass

class Warning(Exception):
    def __init__(self, text):
        self.text = text;