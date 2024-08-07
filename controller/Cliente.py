from modelos.ProductConnection import ProductConnection
from entities.Detail import Detail
import datetime
from UserConnection import UserConnection


from entities.User import User
#PROCESO PARA CORRER EN LA TERMINAL NO PERTECE A LA APLICACION WEB
#ADMINISTRACION DEL USUARIO COMUN O CLIENTE
class Cliente(User):

  def __init__(self, id_user, username , email, password, date, role):
    
    super().__init__(id_user, username , email, password, date, role)
    self.cnx_user = UserConnection()
    self.cnx_product  = ProductConnection()



  def menu(self):

    while True:
      print("\nMenú:")
      print("1. Mostrar Menu")
      print("2. Agregar Pedido por Categoria")
      print("3. Agregar un pedido")
      print("4. Editar un pedido")
      print("5. Eliminar un Pedido")
      print("6. Salir")

      opcion = input("Selecciona una opción: ")

      if opcion == '1':
        print("Menu de platos")
        self.view_prdutcs()
      elif opcion == '2':
        self.view_categorys()
        id_category = int(input("Ingresar el ID de la categoria: "))
        list_products = self.cnx_product.filter_product_ByIdCategory(id_category)
        if len(list_products) > 0:
          for product in list_products:
              print(
                          f"ID: {product[0]}, nombre: {product[1]}, Descripcion: {product[2]}"
                      )
        else:
          print("No se encontraron registros de productos en la Base de Datos")
        id_product = int(input("Ingrese el ID del plato: "))
        quantity = int(input("Ingrese Cantidad: "))
        product = self.cnx_product.product_findByID(id_product)
        ord = self.cnx_user.filter_orderByIDClient()
        try:
          detail = Detail(None, product[5], quantity, datetime.date.today(), ord[0], product[0])
          self.cnx_user.insert_detail(detail)
        except Exception as e:
          print("Error al agregar el pedido.")
      elif opcion == '3':
        self.view_prdutcs()
        id_product = int(input("Ingrese el ID del plato: "))
        quantity = int(input("Ingrese Cantidad: "))
        product = self.cnx_product.product_findByID(id_product)
        ord = self.cnx_user.filter_orderByIDClient()
        try:
          detail = Detail(None, product[5], quantity, datetime.date.today(), ord[0], product[0])
          #VALIDAR PEDIDO
          self.cnx_user.insert_detail(detail)
        except Exception as e:
          print("Error al agregar el pedido.")
        
      elif opcion == '4':
        print("4")
      elif opcion == '5':
        print("5")
      elif opcion == '6':
        print("Programa finalizado.")
        break
      else:
          print(
              "Opción no válida. Por favor, selecciona una opción válida del menú."
          )
  
  #VER PRODUCTOS
  def view_prdutcs(self):
    list_products = self.cnx_product.product_findall()
    if len(list_products) > 0:
        for product in list_products:
            print(
                        f"ID: {product[0]}, nombre: {product[1]}, Descripcion: {product[2]}"
                    )
    else:
        print("No se encontraron registros de productos en la Base de Datos")
  

  #VER CATEGORIAS
  def view_categorys(self):
    list_categorys = self.cnx_product.category_findall()
    if len(list_categorys) > 0:
      for category in list_categorys:
        print(f"ID: {category[0]}, nombre: {category[1]}")
    else:
      print("No se encontraron registros de categorias en la Base de Datos")

  

     
     
