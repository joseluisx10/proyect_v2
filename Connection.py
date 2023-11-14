import sqlite3

#INTENTO DE APLICAR SINGLETON 
class ConnectionSQLite(object):
  
    _instance = None
    
      
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConnectionSQLite, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect("restaurante.db")
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.user = None
            cls._instance.order = None
   
        return cls._instance
    

    def execute_query(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()



    def fetch_data(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
    def one_fetch_data(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()


    def setOrder(self, order):
        self.order = order


    def getOrder(self):
        return self.order
    
    def setUser(self, user):
        self.user = user


    def getUser(self):
        return self.user