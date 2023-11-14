from Connection import ConnectionSQLite

class ProductConnection:

  def __init__(self):
    self.cnx = ConnectionSQLite()
    
    
#TRAER PRODUCTO POR ID
  def product_findByID(self, id_product):
    return self.cnx.one_fetch_data("SELECT * FROM product WHERE id_product = ?", (id_product, ))
    
    
#TRAER TODOS LOS PRODUCTOS
  def product_findall(self):
    return self.cnx.fetch_data("SELECT * FROM product")


#INSERTAR PRODUCTO A LA BAS DE DATOS
  def insert_product(self, product):
    values = (product.name, product.description, product.ingredients,
         product.info_nutrition, product.price, product.stock,
         product.date, product.ranking, product.id_category)
    query ='''INSERT INTO product(name, description, ingredients, inf_nutrition, price, stock, date, ranking, id_category) VALUES(?,?,?,?,?,?,?,?,?)'''
    self.cnx.execute_query(query, values)
        
          
#EDITAR PRODUCTO EN LA BASE DE DATOS
  def edit(self, id, product):
    values = (product.name, product.description, product.ingredients,
         product.info_nutrition, product.price, product.stock,
         product.date, product.ranking, product.id_category, id)
    query = '''UPDATE product SET name = ?, description = ?, ingredients = ?, inf_nutrition = ?, price = ?, stock = ?, date = ?, ranking = ?, id_category = ? WHERE id_product = ?'''
    self.cnx.execute_query(query, values)
 
    
#ELIMINAR PRODUCTO 
  def delete(self, id):
    self.cnx.execute_query("DELETE FROM product WHERE id_product=?", (id, ))


#TRAER CATEGORIAS 
  def category_findall(self):
    return self.cnx.fetch_data("SELECT * FROM category")
  
  
#INSERTAR CATEGORAS 
  def insert_category(self, category):
    value = (category.name,)
    query ='''INSERT INTO category (name) VALUES (?)'''
    return self.cnx.execute_query(query, value)
  
  
#FILTRAR POR CATEGORIA
  def filter_product_ByIdCategory(self, id_category):
    return self.cnx.fetch_data("SELECT * FROM product WHERE id_category = ?", (id_category, ))