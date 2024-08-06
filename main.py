from Connection import ConnectionSQLite
from bd import CreateTables
from UserConnection import UserConnection
import datetime
from User import User
from Order import Order
from Detail import Detail
from Product import Product
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Asegúrate de cambiar esto en un entorno de producción
cnx = ConnectionSQLite()


@app.route('/')
def main():
  categorys = cnx.category_findall()
  mylikes = None
  if('id_user' in session):
    mylikes = cnx.get_all_likes()
  return render_template('index.html', categorys=categorys, mylikes=mylikes)

@app.route('/login_test', methods=['GET', 'POST'])
def login_test():
    Message = None
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        user_data = cnx.login_test(user, password)
        if user_data:
           Message = "Logueado"
        else:
            Message = 'Error usuario o contraseña inavalida'
    return Message

@app.route('/register_test',  methods=['GET', 'POST'])
def register_test():
    Message = None
    if request.method == 'POST':
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            Message = "Todos los campos son obligatorios."
        elif not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$', email):
            Message = "Por favor ingrese un correo electrónico válido."
        elif len(password) < 6:
            Message = "La contraseña debe tener al menos 6 caracteres."
        else:
            user = User(1, username, email, password, datetime.date.today(), 0)
            cnx.insert_user_test(user)
            Message = "Usuario registrado con éxito."
            return Message
    return Message

@app.route('/register',  methods=['GET', 'POST'])
def register():
    Message = None
    if request.method == 'POST':
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            Message = "Todos los campos son obligatorios."
        elif not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$', email):
            Message = "Por favor ingrese un correo electrónico válido."
        elif len(password) < 6:
            Message = "La contraseña debe tener al menos 6 caracteres."
        else:
            user = User(1, username, email, password, datetime.date.today(), 0)
            cnx.insert_user(user)
            Message = "Usuario registrado con éxito."
            return redirect(url_for('register', Message=Message))
    return render_template('register.html', Message=Message)

  

@app.route('/login', methods=['GET', 'POST'])
def login_app():

  if request.method == 'POST':
    user = request.form['user']
    password = request.form['password']
    Message = ''
    user_data = cnx.login(user, password)
    if user_data:
      if user_data[5] == 1:
        session['id_user'] = user_data[0]
        session['rol'] = 'Admin'
        session['username'] = user
        return redirect(url_for('panel_admin'))
      elif user_data[5] == 0:
        session['id_user'] = user_data[0]
        order_data = cnx.filter_orderByIDClient()
        if order_data:
          session['id_ord']= order_data[0]
          session['rol'] = 'User'
          session['username'] = user
          order = Order(order_data[0], order_data[1], order_data[2], order_data[3], order_data[4])
        else: 
          order = Order(None, None, datetime.date.today(), 0, user_data[0])         
          cnx.insert_order(order)    
        return redirect(url_for('panel_usuario'))
    else:
        Message = 'Error usuario o contraseña inavalida'
        return render_template('login.html', Message= Message)
  else:

    return render_template('login.html')

@app.route('/panel-usuario')
def panel_usuario():
   if (not('id_user' in session)):
     return redirect(url_for('main'))
   mylikes = cnx.get_all_likes()
   return render_template('panel_usuario.html', mylikes=mylikes)

@app.route('/panel-admin')
def panel_admin():
   if (not('id_user' in session and session['rol']  == "Admin")):
     return redirect(url_for('main'))
   return render_template('panel_admin.html')


@app.route('/view_product')
def view_product():
    # Lógica para mostrar productos
    if (not('id_user' in session)):
      return redirect(url_for('main'))
    return render_template('view_product.html', products = cnx.product_findall())


@app.route('/filter_bycategory', methods=['GET', 'POST'])
def filter_bycategory():
  if request.method == 'POST':
      id_category = request.form.get('id_category')
      products = cnx.filter_product_ByIdCategory(id_category)
      return render_template('view_product.html', products = products, id_category = id_category)
  categorys = cnx.category_findall()
  return render_template('filter_bycategory.html',categorys=categorys)

@app.route('/personalized_plate')
def personalized_plate():
  return render_template('personalized_plate.html', categorys=cnx.category_findall())


@app.route('/panel_admin/view_user')
def view_user():
  users = cnx.view_users()
  return render_template('view_users.html', users=users)


@app.route('/insert_user', methods = ['GET','POST'])
def insert_user():
  if(request.method == 'POST'):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    date = request.form['date']
    role= request.form['role']
    user = User(1, username, email, password, date, role)
    cnx.insert_user(user)
    return redirect(url_for('main'))

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    date = request.form['date']
    id_user = request.form['id_user']
    role= request.form['role']
    user = User(id_user, username, email, password, date, role)
    cnx.edit_user(id_user, user)
    return redirect(url_for('main'))


@app.route('/delete_user')
def delete_user():
  id_user = int(request.args.get('id_user'))
  cnx.delete_user(id_user)
  return redirect(url_for('view_user'))


@app.route('/set_rol_user')
def set_rol_user():
  id_user = int(request.args.get('id_user'))
  rol = int(request.args.get('rol'))
  if rol == 0:
    rol = 1
  elif rol == 1:
    rol = 0
  cnx.set_rol_user(id_user, rol)
  return redirect(url_for('view_user'))
  


@app.route('/view_detail')
def view_detail():
  if (not('id_user' in session)):
    return redirect(url_for('main'))
  return render_template('view_detail.html', list_products=session.get('datos', []))


@app.route('/insert_detail')
def insert_detail():
  id_product = request.args.get('id_product') 
  list_delivery = cnx.getListDetail()
  cont = 0
  print(list_delivery)
  for product in list_delivery:
    if int(product[0]) == int(id_product):
      cont += 1
  prod= cnx.product_findByID(id_product)
  stock = int(prod[6])
  if stock > cont:
    cnx.setListDetail(prod)
    # Obtener la lista actual de datos desde la sesión (si existe)
    if('datos' in session):
        
        datos_en_sesion = session.get('datos', [])

        # Agregar el nuevo dato a la lista
        datos_en_sesion.append(prod)

        # Guardar la lista actualizada en la sesión
        session['datos'] = datos_en_sesion
    else:
        datos_en_sesion = []
        datos_en_sesion.append(prod)
        session['datos'] = datos_en_sesion

    session['msj'] = 'Su pedido se agrego con exito'
  else:
    session['msj'] = 'No hay mas stock de este producto'
  return redirect(url_for('main'))


@app.route('/eliminar_detail')
def eliminar_detail():
  id_product = request.args.get('id_product') 
  print('id' + str(id_product))
  prod= cnx.product_findByID(int(id_product))
  cnx.removeProductoDetail(prod)
  if('datos' in session):
        
    datos_en_sesion = session.get('datos', [])

    datos_en_sesion.remove(prod)

    # Guardar la lista actualizada en la sesión
    session['datos'] = datos_en_sesion
  return redirect(url_for('panel_usuario'))


@app.route('/abm_products')
def abm_products():
  products = cnx.product_findall()
  categorys = cnx.category_findall()
  return render_template('abm_products.html', products=products, categorys=categorys)


@app.route('/insert_product', methods = ['GET','POST'])
def insert_product():
    name = request.form['name']
    description = request.form['description']
    ingredients = request.form['ingredients']
    inf_nutrition = request.form['inf_nutrition']
    price = request.form['price']
    stock= request.form['stock']
    date = request.form['date']
    ranking = request.form['ranking']
    id_category = request.form['id_category']
    product = Product(None, name, description, ingredients, inf_nutrition, price, stock, date, ranking, id_category)
    cnx.insert_product(product)
    return redirect(url_for('main'))


@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
  if request.method == 'POST':
    name = request.form['name']
    description = request.form['description']
    ingredients = request.form['ingredients']
    inf_nutrition = request.form['inf_nutrition']
    price = request.form['price']
    stock= request.form['stock']
    date = request.form['date']
    ranking = request.form['ranking']
    id_product = int(request.form['id_product'])
    id_category = request.form['id_category']
    product = Product(id_product, name, description, ingredients, inf_nutrition, price, stock, date, ranking, id_category)
    cnx.edit(id_product, product)
    return redirect(url_for('main'))


@app.route('/delete_product')
def delete_product():
  id_product = int(request.args.get('id_product'))
  cnx.delete(id_product)
  return redirect(url_for('abm_products'))

#FIN DE COMPRA
@app.route('/finalize_buies')
def finalize_buies():
  list_prod = []
  price_tot = 0
  if('datos' in session):
    datos_en_sesion = session.get('datos', [])
    for dato in datos_en_sesion:
      cant_product = 0
      #CANTIDAD DE PRODUCTOS AGREGADOS
      for prod in datos_en_sesion:
        if prod[0] == dato[0]:
          cant_product += 1
      if not(dato[0] in list_prod):
        list_prod.append(dato[0])
        detail = Detail(None, float(dato[5]), cant_product, datetime.date.today(), int(session['id_ord']), dato[0])
        cnx.insert_detail(detail)
        prod= cnx.product_findByID(dato[0])
        stock = int(prod[6])
        cnx.edit_stock_product(stock-cant_product, dato[0])
      price_tot += cant_product * float(dato[5])
    cnx.set_pricetot_status_oder(price_tot, 1, int(session['id_ord']))
    session['datos']=[]
    cnx.cleanDetail()
    session['msj'] = "Gracias por su compra, su pedido esta siendo preparado"
  return redirect(url_for('resumen_compra'))

@app.route('/resumen_compra', methods=['GET', 'POST'])
def resumen_compra():
   orders = cnx.get_buies()
   return render_template('car_buies.html', orders=orders)

@app.route('/detail_buies', methods=['GET', 'POST'])
def detail_buies():
  if request.method == 'POST':
    startdate = request.form.get('start')
    enddate = request.form.get('end')
    print(str(startdate) + "ho")
    print(enddate)
    list_orders = cnx.filter_bydate_orders(startdate, enddate)
    return render_template('view_ord.html', list_orders = list_orders)
  return render_template('detail_buies.html')

@app.route('/view_mylikes', methods=['GET', 'POST'])
def view_mylikes():
  categorys = cnx.category_findall()
  mylikes = cnx.get_all_likes()
  return render_template('view_mylikes.html', categorys = categorys, mylikes=mylikes)


@app.route('/toggle_like', methods=['GET', 'POST'])
def toggle_like():
  mylike = request.args.get('mylike')
  print(mylike)
  list_likes = cnx.get_all_likes()
  like = False
  for dato in list_likes:  
    if (mylike == dato[1]):
      like = True
      break
  if like is True:
    print(like)
    cnx.delete_like(mylike)   
    return jsonify(success=True, action='delete')
  else:
    print(like)
    cnx.insert_like(mylike)
    return jsonify(success=True, action='insert')


@app.route('/close_session')
def close_session():
  session.clear()
  cnx.cleanDetail()
  return redirect(url_for('main'))



if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=81)
  ct = CreateTables()
  cnx.execute_query(ct.create_table_user())
  cnx.execute_query(ct.create_table_category())
  cnx.execute_query(ct.create_table_order())
  cnx.execute_query(ct.create_table_product())
  cnx.execute_query(ct.create_table_detail())
  cnx.execute_query(ct.create_table_qualification())
  cnx.execute_query(ct.create_table_shipment())
  cnx.execute_query(ct.create_table_mylikes())
 
