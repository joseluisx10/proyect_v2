import sqlite3

#CREACIONN DE TABLAS 

class CreateTables:
  
  
  def create_table_user(self):
    return '''CREATE TABLE IF NOT EXISTS user (
      id_user INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT,
      email TEXT,
      password TEXT,
      date DATETIME,
      role INT    
    )'''


  def create_table_product(self):
    return '''CREATE TABLE IF NOT EXISTS product (
      id_product INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      description TEXT,
      ingredients TEXT,
      inf_nutrition TEXT,
      price FLOAT,
      stock INT,
      date DATETIME,
      ranking INT,
      id_category INT,
      FOREIGN KEY (id_category) REFERENCES category(id_category)
    )'''


  def create_table_category(self):
    return '''CREATE TABLE IF NOT EXISTS category (
      id_category INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT
    )'''


  def create_table_order(self):
    return '''CREATE TABLE IF NOT EXISTS orders (
      id_ord INTEGER PRIMARY KEY AUTOINCREMENT,
      price_tot FLOAT,
      date DATETIME,
      status INT,
      id_user INT REFERENCES user(id_user)
    )'''


  def create_table_detail(self):
    return '''CREATE TABLE IF NOT EXISTS deatail (
      id_detail_ord INTEGER PRIMARY KEY AUTOINCREMENT,
      price FLOAT,
      quantity INT,
      date DATETIME,
      id_ord INT REFERENCES orders(id_ord),
      id_product INT REFERENCES product(id_product)
    )'''


  def create_table_qualification(self):
    return '''CREATE TABLE IF NOT EXISTS qualification (
      id_qualification INTEGER PRIMARY KEY AUTOINCREMENT,
      description TEXT,
      qualification INT,
      date DATETIME,
      id_ord INT REFERENCES orders(id_ord)
    )'''


  def create_table_shipment(self):
    return '''CREATE TABLE IF NOT EXISTS shipment (
      id_shipment INTEGER PRIMARY KEY AUTOINCREMENT,
      addres TEXT,
      phone TEXT,
      deparment INT,
      detail_order,
      status INT,
      id_ord INT REFERENCES orders(id_ord)
    )'''


