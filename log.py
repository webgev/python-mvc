from datetime import datetime

def LogMsg(message):
    date = datetime.now()
    x = open('./logs/event.txt', "a", encoding="utf-8")
    x.write(str(date) + " : " + message + '\n')

def ErrorMsg(message):
    x = open('./logs/error.txt', "a", encoding="utf-8")
    x.write(str(date) + " : " + message + '\n')