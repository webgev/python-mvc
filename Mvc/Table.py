from Mvc.Sql import SqlQuery, Type

class Table:
    name = ''
    primary = ''
    columns = None
    def __init__(self, name):
        self.name = name
        self.columns = {}
        
    def AddColumn(self, name, type, primary=False, key=False, default="", is_null=False, size=None):
        self.columns[name] = Column(name, type, primary, key, default, is_null)
        if primary:
            self.primary = name
    
    def GetColumns(self):
        return self.columns
    
    def CreateTable(self):
        sq_columns = []
        primary = None
        
        for name in self.columns:
            column = self.columns[name]
            if column.primary:
                primary = name
            sq_columns.append("`{name}` {type} {default} {is_null} {key}".format(
                name = name,
                type = column.sql_type,
                key = column.key,
                is_null = column.is_null,
                default = column.default
            ))
            
        query = """
            CREATE TABLE IF NOT EXISTS `{table}` ( 
            {columns}
            {primary}
           ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 
        """.format(
            table = self.name,
            columns = ",".join(sq_columns),
            primary = ",PRIMARY KEY (`%s`)  " % (primary) if primary else ''
        )
        
        SqlQuery(query)
        self.UpdateColumn()
    
    def UpdateColumn(self):
        current_columns = SqlQuery("SHOW COLUMNS FROM `{table}`".format(table=self.name))
        current_columns_name = set(column["Field"]  for column in current_columns)
        
        new_columns = set(self.columns) - current_columns_name
        del_columns = current_columns_name - set(self.columns)
        
        if new_columns: 
            arr = []
            query = """ ALTER TABLE `{table}` {columns}"""
            for name in new_columns:
                column = self.columns[name]
                arr.append(""" ADD `{name}` {type} {default} {is_null} {key} """.format(
                    name = column.name,
                    type = column.sql_type,
                    default = column.default,
                    is_null = column.is_null,
                    key = column.key
                ))
            
            SqlQuery(query.format(table=self.name, columns=", ".join(arr)))
                
        
class Column:
    is_change = False
    old_name = None
    
    name = None
    type = None
    primary = None
    key = None
    default = None
    is_null = None
    
    def __init__(self, name, type, primary=False, key=False, default="", is_null=False, size=None):
        self.name = name
        self.first_name = name
        self.type = type
        self.sql_type = Type.Get(type, size)
        self.primary = primary
        self.key = "auto_increment" if key else ''
        self.is_null = "NOT NULL" if not is_null else ''
        self.default = "default %s" % (default) if default  else ''
        
    def SetChange(self, value=True):
        self.is_change = value
        
    def Change(self, field, value):
        if field == 'name':
            self.name = value
        elif field == 'type':
            self.type = value  
        elif field == 'primary':
            self.primary = value
        elif field == 'key':
            self.key = value
        elif field == 'dafault':
            self.dafault = value
        elif field == 'is_null':
            self.is_null = value
        else:
            return False
            
        self.SetChange()
        return True