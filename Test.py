import unittest
from flask_testing import TestCase
from main import app, cnx  # Asegúrate de que 'main.py' es el archivo correcto

class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # Configuración de la base de datos de prueba
        self.db = cnx
        self.db.execute_query('''
        CREATE TABLE IF NOT EXISTS test_user (
          test_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT,
          email TEXT,
          password TEXT,
          date DATETIME,
          role INT
        )''')  # Agrega aquí la estructura de la tabla user
        # Agrega las estructuras de otras tablas necesarias para las pruebas

    def tearDown(self):
        # Limpieza de la base de datos de prueba
        self.db.execute_query("DROP TABLE IF EXISTS test_user")

    def test_register_success(self):
        response = self.client.post('/register_test', data=dict(
            user='testuser',
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn('Usuario registrado con éxito.'.encode('utf-8'), response.data)

    def test_register_missing_field(self):
        response = self.client.post('/register_test', data=dict(
            user='',
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn('Todos los campos son obligatorios.'.encode('utf-8'), response.data)

    def test_register_invalid_email(self):
        response = self.client.post('/register_test', data=dict(
            user='testuser',
            email='invalid-email',
            password='password'
        ), follow_redirects=True)
        self.assertIn('Por favor ingrese un correo electrónico válido.'.encode('utf-8'), response.data)

    def test_login_success(self):
        response = self.client.post('/login_test', data=dict(
            user='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertIn('panel_usuario'.encode('utf-8'), response.data)

    def test_login_failure(self):
        response = self.client.post('/login_test', data=dict(
            user='nonexistent',
            password='password'
        ), follow_redirects=True)
        self.assertIn('Error usuario o contraseña invalida'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()