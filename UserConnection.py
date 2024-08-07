from modelos.Connection import ConnectionSQLite
from flask import session

class UserConnection:

  def __init__(self):
    self.cnx = ConnectionSQLite()
    

  #LOGUEO DE USUARIO  
  def login(self, user, passw):
    user_data =  self.cnx.one_fetch_data(
        '''SELECT * FROM user WHERE username = ? AND password = ?''',
        (user, passw))    
    return user_data



  #TRAER USUARIOS
  def view_users(self):
    return self.cnx.fetch_data("SELECT * FROM user")



  #METODO PARA INSERTAR USUARIO EN LA BASE DE DATOS
  def insert_user(self, user):
    user_data = (user.username, user.email, user.password, user.date, user.role)
    query = '''INSERT INTO user (username, email, password, date, role) VALUES (?, ?, ?, ?, ?)'''
    self.cnx.execute_query(query, user_data)

  

  #EDITAR USUARIO
  def edit_user(self, id, user):
    values = (user.username, user.email, user.password, user.date, user.role, id)
    query = '''UPDATE user SET username = ?, email = ?, password = ?, date = ?, role = ? WHERE id_user = ?'''
    self.cnx.execute_query(query, values)



  #ELIMINAR USUARIO
  def delete_user(self, id):
    self.cnx.execute_query("DELETE FROM user WHERE id_user=?", (id, ))

  
  #FITRAR ODEN DE COMPRA
  def filter_orderByIDClient(self):
    return self.cnx.one_fetch_data("SELECT * FROM orders WHERE id_user = ?", (session['id_user'],))
  
  

  def insert_detail(self, detail):
    values = (detail.price, detail.quantity, detail.date, detail.id_ord, detail.id_product)
    query =  '''INSERT INTO deatail (price, quantity, date, id_ord, id_product) VALUES (?, ?, ?, ?, ?)'''
    self.cnx.execute_query(query, values)


  def insert_order(self, ord):
    values = (ord.quantity, ord.date, ord.status, ord.id_user)
    query =  '''INSERT INTO orders (quantity, date, status, id_user) VALUES (?, ?, ?, ?)'''
    self.cnx.execute_query(query, values)