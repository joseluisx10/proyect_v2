class Product:

  def __init__(self, id_product, name, description, ingredients, inf_nutrition, price,
               stock, date, ranking, id_category):
## agregar id del producto
    self.id_product = id_product
    try:
      self.name = name
    except Exception as e:
      print("Error al ingresar el nombre del producto")
    try:
      self.description = description
    except Exception as e:
      print("Error al ingresar la descripcion del producto")
    try:
      self.ingredients = ingredients
    except Exception as e:
      print("Erro al ingresar los ingredientes del producto")
    try:
      self.info_nutrition = inf_nutrition
    except Exception as e:
      print("Error al ingresar la informacion nutricional del producto")
    try:  
      self.price = float(price)
    except Exception as e:
      print("Error al ingresar el precio del producto")
    try: 
      self.stock = int(stock)
    except Exception as e:
      print("Error al ingresar stock del producto")
    try:
      self.ranking = int(ranking)
    except Exception as e:
      print("Error al ingresar el ranking del producto")
    try:
      self.id_category = int(id_category)
    except Exception as e:
      print(f"Error al ingresar la categoria del producto")
    self.date = date