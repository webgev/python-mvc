from datetime import datetime
from threading import Thread
from flask import session
import os

url = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(url):
    os.makedirs(url)

if not os.path.exists('./logs'):
    os.makedirs('./logs')

def writer(filename, message):
    with open(filename, "a", encoding="utf-8") as fout:
        fout.write(message)
        fout.close()

def LogMsg(message):
    
    user_id = session.get('user_id')
    date = datetime.now()
    message = str(date) + "; " + str(user_id) + "; " + message + '\n'
    t1 = Thread(target=writer, args=('./logs/event.txt', message))
    t1.start()

def ErrorMsg(message):
    
    user_id = session.get('user_id')
    date = datetime.now()
    message = str(date) + "; " + str(user_id) + "; " + message + '\n'
    t1 = Thread(target=writer, args=('./logs/error.txt', message))
    t1.start()