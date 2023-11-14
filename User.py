import re

class User:
  
  def __init__(self, id_user, username , email, password, date, role):
    self.id_user = id_user 
    try:
      self.username = username
    except Exception as e:
      print("Error al ingresar username: " + str(e))
    try:
      self.__validar_email(email)
    except Exception as e:
      print("Error al ingresar email: " + str(e))
    try:
       self.password = password
    except Exception as e:
      print("Error al ingresar contraseña: " + str(e))
    
    self.date = date
    try:
       self.role = int(role) 
    except Exception as e:
      print("Error al ingresar rol: " + str(e))
   
    
   
    
   
   
  def __validar_email(self, email):

    # Expresión regular para validar un correo electrónico
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
 
    # Utilizar re.match() para validar el correo electrónico
    if re.match(patron, email):
       self.email = email
       return True 
    else:
       raise ValueError("Correo electrónico invalido")

  def getRole(self):
    return self.role
