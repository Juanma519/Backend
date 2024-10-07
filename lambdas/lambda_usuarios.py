import json
from pymongo import MongoClient
from bson import ObjectId
import os

def connect_to_mongo():
    mongo_uri = os.getenv('MONGODB_URI')
    client = MongoClient(mongo_uri)
    db = client['prueba']
    return db
    
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o) 
        return super().default(o)

def lambda_handler(event, context):
    db = connect_to_mongo()
    collection_usuarios = db['usuarios']
    
    # Obtener el cuerpo de la solicitud
    body = json.loads(event.get('body'))
    accion = body.get('accion')

    if accion == "create":
        return create_usuario(body)
    elif accion == "get":
        return get_usuario(body)
    elif accion == "update":
        return update_usuario(body)
    elif accion == "delete":
        return delete_usuario(body)
    elif accion == "login":
        return login(body)
    elif accion == "get_universidad_usuarios":
        return get_usuarios_universidad(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Acción no válida", "success": False})
        }

def create_usuario(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})

    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    nuevo_usuario = {
        "nombre": body.get('nombre'),
        "apellido": body.get('apellido'),
        "password": body.get('password'),  # Sin encriptación
        "tipo": body.get('tipo'),
        "universidad": universidad_id,
        "mail": body.get('mail')
    }
    
    try:
        resultado = collection_usuarios.insert_one(nuevo_usuario)
        return {
            'statusCode': 201,
            'body': json.dumps({"message": "Usuario creado con éxito", "user_id": str(resultado.inserted_id), "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al crear usuario: {str(e)}", "success": False})
        }

def get_usuario(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})

    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    usuario = collection_usuarios.find_one({"mail": body.get('mail'), "universidad": universidad_id})

    if usuario:
        usuario.pop('password', None)  # Eliminamos la contraseña de la respuesta
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
            'body': json.dumps({"message": "Usuario encontrado", "user": usuario, "success": True},cls=JSONEncoder)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Usuario no encontrado", "success": False})
        }

def update_usuario(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})

    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    filtro = {"mail": body.get('mail'), "universidad": universidad_id}

    datos_actualizados = body.get('datos_actualizados')
    
    try:
        resultado = collection_usuarios.update_one(filtro, {"$set": datos_actualizados})
        if resultado.matched_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Usuario actualizado con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Usuario no encontrado", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al actualizar usuario: {str(e)}", "success": False})
        }

def delete_usuario(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})

    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    filtro = {"mail": body.get('mail'), "universidad": universidad_id}

    try:
        resultado = collection_usuarios.delete_one(filtro)
        if resultado.deleted_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Usuario eliminado con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Usuario no encontrado", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar usuario: {str(e)}", "success": False})
        }

def login(body):
    db = connect_to_mongo()
    collection_usuarios = db['usuarios']
    usuario = collection_usuarios.find_one({"mail": body.get('mail')}) 

    if usuario:
        if body.get('password') == usuario["password"]:  # Sin encriptación
            usuario.pop('password', None)
            return {
                'statusCode' : 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({
                    "message": "Log in exitoso",
                    "succes": True,
                    "userType": usuario["tipo"],
                    "user": usuario  
                }, cls=JSONEncoder)  
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({"message": "Contraseña incorrecta", "success": False})
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Usuario no encontrado", "success": False})
        }

def get_usuarios_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})

    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    usuarios = collection_usuarios.find({"universidad": universidad_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps([usuario for usuario in usuarios])
    }
