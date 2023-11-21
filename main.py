from Connection import ConnectionSQLite
from bd import CreateTables
from UserConnection import UserConnection
from Admin import Admin
import datetime
from Cliente import Cliente
from Order import Order
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Asegúrate de cambiar esto en un entorno de producción
cnx = ConnectionSQLite()


@app.route('/')
def main():
  msj=None
  if (not('id_user' in session)):
    return render_template('index.html')
  if 'msj' in session:
    msj = session['msj']
    session['msj'] = None
    return render_template('menu.html', msj = msj)
  return render_template('menu.html', msj= msj)
    

@app.route('/login', methods=['GET', 'POST'])
def login_app():

  if request.method == 'POST':
    user = request.form['user']
    password = request.form['password']
    Message = ''
    if cnx.login(user, password):
      user = cnx.login(user, password)
      if user[5] == 1:
        session['id_user'] = user[0]
        session['rol'] = 'Admin'
        return redirect(url_for('main'))
      elif user[5] == 0:
        session['id_user'] = user[0]
        if cnx.filter_orderByIDClient():
          data_order = cnx.filter_orderByIDClient()
          session['id_ord']= data_order[0]
          session['rol'] = 'User'
          order = Order(data_order[0], data_order[1], data_order[2], data_order[3], data_order[4])
        else: 
          order = Order(None, None, datetime.date.today(), 0, user[0])         
          cnx.insert_order(order)    
        return redirect(url_for('main'))
    else:
        Message = 'Error usuario o contraseña inavalida'
        return render_template('index.html', Message= Message)
  else:

    return render_template('index.html')


@app.route('/view_product')
def view_product():
    # Lógica para mostrar productos
    if (not('id_user' in session)):
      return render_template('index.html')  
    return render_template('view_product.html', products = cnx.product_findall())


@app.route('/filter_bycategory', methods=['GET', 'POST'])
def filter_bycategory():
  if (not('id_user' in session)):
    return render_template('index.html')
  # Lógica para mostrar productos
  if request.method == 'POST':
      id_category = request.form.get('id_category')
      products = cnx.filter_product_ByIdCategory(id_category)
      return render_template('view_product.html', products = products)
  categorys = cnx.category_findall()
  return render_template('filter_bycategory.html',categorys=categorys)


@app.route('/insert_detail')
def insert_detail():
  id_product = request.args.get('id_product')

  
  list_delivery = cnx.getListDetail()
  cont = 0

  for product in list_delivery:
    if int(product[0]) == int(id_product):
      print(str(product[0])+'dgdg')
      cont += 1

  prod= cnx.product_findByID(id_product)
  stock = int(prod[6])
  if stock > cont:
    cnx.setListDetail(prod)
    session['msj'] = 'Su pedido se agrego con exito'
  else:
    session['msj'] = 'No hay mas stock de este producto'
  return redirect(url_for('main'))


@app.route('/view_detail')
def view_detail():
  if (not('id_user' in session)):
    return render_template('index.html')
  return render_template('view_detail.html', list_products=cnx.getListDetail())


@app.route('/personalized_plate')
def personalized_plate():
  return render_template('personalized_plate.html', categorys=cnx.category_findall())


@app.route('/perfil_admin')
def perfil_admin():
  return render_template('perfil_admin.html')


@app.route('/perfil_admin/view_user')
def view_user():
  return render_template('view_users.html')


@app.route('/close_session')
def close_session():
  session.clear()
  cnx.cleanDetail()
  return redirect(url_for('main'))

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=81)
 
