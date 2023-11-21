import sqlite3
from flask import session

#INTENTO DE APLICAR SINGLETON 
class ConnectionSQLite(object):
  
    _instance = None
    
      
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConnectionSQLite, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect("restaurante.db", check_same_thread=False)
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.detail = []
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


    def setListDetail(self, value):
        self.detail.append(value)


    def getListDetail(self):
        return self.detail
    
    def cleanDetail(self):
        self.detail = []

    
    #LOGUEO DE USUARIO  
    def login(self, user, passw):
        user_data =  self.one_fetch_data(
            '''SELECT * FROM user WHERE username = ? AND password = ?''',
            (user, passw))    
        return user_data



    #TRAER USUARIOS
    def view_users(self):
        return self.fetch_data("SELECT * FROM user")



    #METODO PARA INSERTAR USUARIO EN LA BASE DE DATOS
    def insert_user(self, user):
        user_data = (user.username, user.email, user.password, user.date, user.role)
        query = '''INSERT INTO user (username, email, password, date, role) VALUES (?, ?, ?, ?, ?)'''
        self.execute_query(query, user_data)

    

    #EDITAR USUARIO
    def edit_user(self, id, user):
        values = (user.username, user.email, user.password, user.date, user.role, id)
        query = '''UPDATE user SET username = ?, email = ?, password = ?, date = ?, role = ? WHERE id_user = ?'''
        self.execute_query(query, values)



    #ELIMINAR USUARIO
    def delete_user(self, id):
        self.execute_query("DELETE FROM user WHERE id_user=?", (id, ))

    
    #FITRAR ODEN DE COMPRA
    def filter_orderByIDClient(self):
        return self.one_fetch_data("SELECT * FROM orders WHERE id_user = ?", (session['id_user'],))
    
    

    def insert_detail(self, detail):
        values = (detail.price, detail.quantity, detail.date, detail.id_ord, detail.id_product)
        query =  '''INSERT INTO deatail (price, quantity, date, id_ord, id_product) VALUES (?, ?, ?, ?, ?)'''
        self.execute_query(query, values)


    def insert_order(self, ord):
        values = (ord.quantity, ord.date, ord.status, ord.id_user)
        query =  '''INSERT INTO orders (quantity, date, status, id_user) VALUES (?, ?, ?, ?)'''
        self.execute_query(query, values)



    #TRAER PRODUCTO POR ID
    def product_findByID(self, id_product):
        return self.one_fetch_data("SELECT * FROM product WHERE id_product = ?", (id_product, ))
        
        
    #TRAER TODOS LOS PRODUCTOS
    def product_findall(self):
        return self.fetch_data("SELECT * FROM product")


    #INSERTAR PRODUCTO A LA BAS DE DATOS
    def insert_product(self, product):
        values = (product.name, product.description, product.ingredients,
            product.info_nutrition, product.price, product.stock,
            product.date, product.ranking, product.id_category)
        query ='''INSERT INTO product(name, description, ingredients, inf_nutrition, price, stock, date, ranking, id_category) VALUES(?,?,?,?,?,?,?,?,?)'''
        self.execute_query(query, values)
        
          
    #EDITAR PRODUCTO EN LA BASE DE DATOS
    def edit(self, id, product):
        values = (product.name, product.description, product.ingredients,
            product.info_nutrition, product.price, product.stock,
            product.date, product.ranking, product.id_category, id)
        query = '''UPDATE product SET name = ?, description = ?, ingredients = ?, inf_nutrition = ?, price = ?, stock = ?, date = ?, ranking = ?, id_category = ? WHERE id_product = ?'''
        self.execute_query(query, values)
    
    
    #ELIMINAR PRODUCTO 
    def delete(self, id):
        self.execute_query("DELETE FROM product WHERE id_product=?", (id, ))


    #TRAER CATEGORIAS 
    def category_findall(self):
        return self.fetch_data("SELECT * FROM category")
    
    
    #INSERTAR CATEGORAS 
    def insert_category(self, category):
        value = (category.name,)
        query ='''INSERT INTO category (name) VALUES (?)'''
        return self.execute_query(query, value)
    
    
    #FILTRAR POR CATEGORIA
    def filter_product_ByIdCategory(self, id_category):
        return self.fetch_data("SELECT * FROM product WHERE id_category = ?", (id_category, ))