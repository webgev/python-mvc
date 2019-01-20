import config
import pymysql.cursors

class Connect:
    connect = None
    @staticmethod
    def Connect():
        Connect.connect = pymysql.connect(
            host='localhost',
            user=config.user,
            password=config.password, 
            db=config.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    @staticmethod    
    def CloseConnect():
        if Connect.connect:
            Connect.connect.close();
        
def SqlQuery( query, *data):
    cursor = Connect.connect.cursor()
    cursor.execute(query, data)
    return cursor.fetchall()
    
def SqlQueryItem(query, *data):
    result = self.SqlQuery(query, data)
    return result[0] if result else None   
    
from datetime import date, datetime

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
        if type is datatime:
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