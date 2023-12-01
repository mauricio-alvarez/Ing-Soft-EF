from flask import Flask, request, jsonify
import flask_cors
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/transacciones"
db = SQLAlchemy(app)
flask_cors.CORS(app)


# Rutas
@app.route('/')
def hello():
    return "<h1>API Transacciones</h1>"

@app.route('/billetera/contactos', methods=['GET'])
def get_contactos():
    number = request.args.get('minumero')
    cuenta = db.session.query(Cuenta).filter_by(numero=number).first()
    contacts = []
    for contacto in cuenta.contactos:
        contacts.append(f"{contacto}: {db.session.query(Cuenta).filter_by(numero=contacto).first().nombre}")
    return jsonify(contacts)

@app.route('/billetera/historial', methods=['GET'])
def get_historial():
    number = request.args.get('minumero')
    cuenta = db.session.query(Cuenta).filter_by(numero=number).first()
    pagos = db.session.query(Operacion).filter_by(numero_origen=number).all()
    cobros = db.session.query(Operacion).filter_by(numero_destino=number).all()
    response = []
    response.append(f"Saldo disponible: {cuenta.saldo}")
    response.append("Operaciones realizadas:")
    for pago in pagos:
        response.append(f"El {pago.fecha}: Pago realizado de {pago.valor} a {pago.numero_destino}")
    for cobro in cobros:
        response.append(f"El {cobro.fecha}: Cobro realizado de {cobro.valor} a {cobro.numero_origen}")
    return jsonify(response)

@app.route('/billetera/pagar', methods=['GET'])
def pagar():
    numero_origen = request.args.get('minumero')
    numero_destino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))
    fecha = datetime.now()  # Get the current date and time
    cuenta_origen = db.session.query(Cuenta).filter_by(numero=numero_origen).first()
    cuenta_destino = db.session.query(Cuenta).filter_by(numero=numero_destino).first()
    if cuenta_origen.saldo >= valor:
        cuenta_origen.saldo -= valor
        cuenta_destino.saldo += valor
        db.session.add(Operacion(numero_origen, numero_destino, fecha, valor))
        db.session.commit()
        return jsonify(f"Realizado el {fecha}")
    else:
        return jsonify({"ERROR": "Saldo insuficiente"})

# Tablas
class Cuenta(db.Model):
    __tablename__ = 'cuenta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    numero = db.Column(db.String(10), nullable=False, unique=True)
    saldo = db.Column(db.Float, nullable=False)
    contactos = db.Column(db.ARRAY(db.String(10)), nullable=False)

    def __init__(self, numero, saldo):
        self.numero = numero
        self.saldo = saldo

    def __repr__(self):
        return f"<Numero: {self.numero}, Saldo disponible: {self.saldo}>"

class Operacion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_origen = db.Column(db.String(50), nullable=False)
    numero_destino = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(60), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def __init__(self, numero_origen, numero_destino, fecha, valor):
        self.numero_origen = numero_origen
        self.numero_destino = numero_destino
        self.fecha = fecha
        self.valor = valor
    
    def __repr__(self):
        return f"<Numero origen: {self.numero_origen}, Numero destino: {self.numero_destino}, Fecha: {self.fecha}, Valor: {self.valor}>"

# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
