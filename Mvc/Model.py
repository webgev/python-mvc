import config
from Mvc.Sql import SqlQuery
from Mvc.Table import Table

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
        if not self.table:
            return False
        where = """
            {column_id} = %s
        """.format(column_id=self.table.primary)
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

    def _Delete(self, _id, column_id=None):
        column_id= column_id or self.table.primary
        if not column_id:
            raise Warning("Not primary key!")
            
        SqlQuery(""" 
            DELETE FROM 
                {table}
            WHERE 
                {column_id} = %s
        """.format(
            table = self.table.name,
            column_id=self.table.primary
        ), _id)
        
 
    def CheckModel(self, obj):
        columns = self.table.GetColumns()
        for field in columns:
            column = columns[field]
            if column.is_null and not column.default and not column.key:
                if column.name in obj:
                    continue
                print(column.is_null)
                return False

        return True