import unittest
from flask import Flask
from app import app, db, Cuenta, Operacion

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
    
    # probar que la ruta contactos funcione
    def test_get_contacts_success(self):
        response = self.client.get('http://127.0.0.1:5000/billetera/contactos?minumero=123')
        self.assertEqual(response.status_code, 200)
    # probar que la ruta contactos no acepte un numero de cuenta que no exista
    def test_get_contacts_fail(self):
        response = self.client.get('/billetera/contactos?minumero=999')
        self.assertEqual(response.status_code, 404)
    
    def test_get_historial_success(self):
        response = self.client.get('/billetera/historial?minumero=21345')
        self.assertEqual(response.status_code, 200)

    def test_get_historial_fail(self):
        response = self.client.get('/billetera/historial?minumero=111')
        self.assertEqual(response.status_code, 404)

    def test_pagar_success(self):
        response = self.client.get('/billetera/pagar?minumero=123&numerodestino=456&valor=50')
        self.assertEqual(response.status_code, 200)

    def test_pagar_fail(self):
        response = self.client.get('/billetera/pagar?minumero=222&numerodestino=333&valor=999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()