import config
import log
import pymysql.cursors
from datetime import date, datetime

class Connect:
    connect = None
    @staticmethod
    def Connect():
        if Connect.connect:
            return
        Connect.connect = pymysql.connect(
            host=config.host,
            user=config.user,
            password=config.password, 
            db=config.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    @staticmethod    
    def CloseConnect():
        if Connect.connect:
            Connect.connect.close()
            Connect.connect = None
        
def SqlQuery(query, *data):
    Connect.Connect()
    cursor = Connect.connect.cursor()
    if not config.convert:
        log.LogMsg("Вызов SQL с данными: " + str(data))
        log.LogMsg(query.strip())
    cursor.execute(query, data)
    if not config.convert:
        log.LogMsg("Конец вызова")
    return cursor.fetchall()
    
def SqlQueryItem(query, *data):
    result = self.SqlQuery(query, data)
    return result[0] if result else None   
    

class Type:
    @staticmethod
    def Get(type, size):
        if type is int:
            return Type.Int(size)
        if type is str:
            if size and size > 255:
                return Type.Text()
            return Type.String(size)
        if type is date:
            return Type.Date()
        if type is datetime:
            return Type.Datetime()
         
    @staticmethod
    def Int(n=5):
        return 'INT(%s) UNSIGNED' %(n or 5)
    @staticmethod
    def String(n=255):
        return 'VARCHAR(%s) character set utf8' %(n  or 255)
    @staticmethod    
    def Text():
        return 'TEXT character set utf8'
    @staticmethod    
    def Date():
        return 'DATE'
    @staticmethod   
    def Datetime():
        return 'DATETIME'


