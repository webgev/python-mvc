import config
from mvc.Sql import SqlQuery
from mvc.Table import Table

class Model:
    table_name = ""
    dbs = None
    
    def __init__(self):
        self.InitDB()
                
    def InitDB(self, flag=False):
        if not self.table_name:
            return
        self.table = Table(self.table_name)
        for column in self.columns:
            self.table.AddColumn(**column)
            
        if config.initDb or flag:
            self.table.CreateTable()

    def _List(self, columns=None, where='', offset=None, limit=None, data=[]):
        if not self.table:
            return False
     
        columns = columns or  self.table.GetColumns()
        where = where.format(column_id=self.table.primary)
        return SqlQuery(""" 
            select 
                {columns}
            from 
                {table}
            {where}
            {limit}
            {offset}
            """.format(
                columns = ",".join(columns), 
                table = self.table.name,
                where = """
                    where %s
                """ % (where) if where else '',
                limit = """
                    limit %s
                """ % (limit) if limit else '',
                offset = """
                    offset %s
                """ % (offset) if offset else ''
            ), *data
        )
        
    def _Read(self, id):
        where = """
            {column_id} = %s
        """
        result = self._List(where=where, data=[id])
        return result[0] if result else None   
     
     
    def _Create(self, params):
        values = []
        columns = self.table.GetColumns()
        for column in columns:
            value = params.get(column)
            values.append(value)
        
        SqlQuery(""" 
            INSERT INTO 
                {table}
            ( {columns} )
            VALUES ({values})
            """.format(
                table = self.table.name,
                columns = ",".join(columns), 
                values = ",".join(list("%s" for column in columns))
            )
        , *values)
        
 
    def CheckModel(self, obj):
        for field in obj:
            columns = self.table.GetColumns()
            if field in columns:
                if columns[field].type is type(obj[field]):
                    continue
            return False
        return True
        