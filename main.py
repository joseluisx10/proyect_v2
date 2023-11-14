from Connection import ConnectionSQLite
from bd import CreateTables
from UserConnection import UserConnection
from Admin import Admin
import datetime
from Cliente import Cliente
from Order import Order
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

app.debug = True

@app.route('/')
def menu():
  return render_template('menu.html')

if __name__ == "__main__":


  app.run(host='0.0.0.0', port=81)
  cnx = ConnectionSQLite()

  ct = CreateTables()

  cnx.execute_query(ct.create_table_user())
  cnx.execute_query(ct.create_table_category())
  cnx.execute_query(ct.create_table_order())
  cnx.execute_query(ct.create_table_product())
  cnx.execute_query(ct.create_table_detail())
  cnx.execute_query(ct.create_table_qualification())
  cnx.execute_query(ct.create_table_shipment())

  db_user = UserConnection()

  def login():

      user = input("Ingrese Usuario:\n")
      passw = input("Ingrese Contraseña:\n")

      if db_user.login(user, passw):
        print("Bienvenido")
        user = db_user.login(user, passw)
      
        print(user[5])
        if user[5] == 1:
          print("Usuario Administrador")
          adm = Admin(user[0], user[1], user[2], user[3], user[4], user[5])
          cnx.setUser(adm)
          adm.menu()
        elif user[5] == 0:
          print("Bienvenido: " + user[1])
          cliente = Cliente(user[0], user[1], user[2], user[3], user[4], user[5])
          cnx.setUser(cliente)
          if db_user.filter_orderByIDClient():
            data_order = db_user.filter_orderByIDClient()
            order = Order(data_order[0], data_order[1], data_order[2], data_order[3], data_order[4])
          else: 
            order = Order(None, None, datetime.date.today(), 0, user[0])         
            db_user.insert_order(order)

          #FORMA PARA TRABAJAR CON EL OBJETO ORDER GLOBALMENTE
          cnx.setOrder(order)
          cliente.menu()
      else:
        print("Usuario o contraseña incorrectos")


  def register_user():
      print("\n\nGracias por confiar en nosotros\n\n")
      current_date = datetime.date.today()
      username = input("Ingrese un Nombre de Usuario: ")
      email = input("Ingrese un Correo Electronico: ")
      passw = input("Ingrese Contraseña: ")
      try:
          db_user.insert_user(Cliente(None, username, email, passw, current_date, 0))      
          print("Bienvenidos al sistema de Restaurante")
      except Exception as e:
          print("Error al registrar usuario" + str(e))
        

  def iniciar():
      print("Bienvenido al sistema de Restaurante")
      print("1. Iniciar Sesión")
      print("2. Registrarse")
      print("3. Salir")
      opcion = int(input("Ingrese una opción: "))
      while True:
        if opcion == 1:
          login()       
        elif opcion == 2:
          register_user()
          pass
        elif opcion == 3:
          print("Programa finalizado.")
          break
        else:
          print(
              "Opción no válida. Por favor, selecciona una opción válida del menú."
          )
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = int(input("Ingrese una opción: "))


    
  iniciar()

