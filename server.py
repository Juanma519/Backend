from flask import Flask, request, jsonify
from flask_pymongo import Pymongo
from bson.objectid import ObjectId
#para que estos import funcionen hay que instalar flask en sus computadoras
#pip install flask
#pip install flask-pymongo
#pip install pymongo

# Configuración de la URI para MongoDB local o MongoDB Atlas
app.config["MONGO_URI"] = ""  # Poner  la URI entre las comillas 
mongo = PyMongo(app)
db = mongo.db

app = Flask(__name__)

# Ruta para insertar un documento
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    user_id = db.users.insert_one({'name': name, 'email': email}).inserted_id
    return jsonify(message="Usuario añadido", id=str(user_id)), 201

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    users_list = []
    for user in users:
        users_list.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email']})
    return jsonify(users_list), 200

# Ruta para obtener un usuario por su ID
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    if user:
        return jsonify({'id': str(user['_id']), 'name': user['name'], 'email': user['email']}), 200
    return jsonify(message="Usuario no encontrado"), 404





#Esto de aca es para recibir los https de flutter (hay q modificar la mayoria para configurarlo, pero para tenerlo de base)
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Recibe el JSON enviado desde Flutter
    print(f"Datos recibidos: {data}")
    response = {"message": "Datos recibidos con éxito"}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)