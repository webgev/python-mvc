from Mvc.Sql import SqlQuery, Type

class Table:
    name = ''
    primary = ''
    columns = None
    def __init__(self, name, columns = None, indexs = None, foregions = None):
        self.name = name
        self.columns = {}
        self.indexs = indexs
        self.foregions = foregions
        if columns:
            for column in columns:
                self.AddColumn(**column)
        
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
        print(query)
        SqlQuery(query)
        
        self.UpdateColumn()
        self.CreateIndex()
        self.CreateForegion()
    
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
        

    def CreateForegion(self):
        if not self.foregions:
            return
        query = ""
        for foregion in self.foregions:
            query = """ 
                ALTER TABLE `{table_name}` 
                ADD CONSTRAINT `{name}`
                FOREIGN KEY (`{column}`) REFERENCES `{table}` (`{link_column}`)
            """.format(
                table_name = self.name,
                name = foregion["name"],
                column = foregion["column"],
                table = foregion["table"],
                link_column = foregion["link_column"]
            )
            if foregion.get("ondelete"):
                query +=  """ ON DELETE {} """.format(foregion.get("ondelete"))
            if foregion.get("onupdate"):
                query +=  """ ON UPDATE {} """.format(foregion.get("onupdate"))
            query += "; "
        print(query)
        SqlQuery(query)


    def CreateIndex(self):
        if not self.indexs:
            return
        query = ""
        current_indexs = SqlQuery("SHOW INDEX FROM `{table}`".format(table=self.name))
        current_index_name = set(column["Key_name"]  for column in current_indexs)
        
        indexs = list(index["name"] for index in self.indexs)

        new_columns = set(indexs) - current_index_name
        del_columns = current_index_name - set(indexs)
        
        if new_columns:           
            for index in self.indexs:
                if index["name"] not in new_columns:
                    continue
                query = """ 
                    ALTER TABLE `{table_name}` 
                    ADD {type} `{name}` ({columns});
                """.format(
                    table_name = self.name,
                    type = index["type"],
                    name = index["name"],
                    columns = ",".join(index["columns"])
                )
        if query:
            SqlQuery(query)        
        
        
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