import json
from datetime import datetime
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
    collection_clases = db['clases']
    
    # Obtener el cuerpo de la solicitud
    body = json.loads(event.get('body'))
    accion = body.get('accion')

    if accion == "create":
        return create_clase(body)
    elif accion == "get":
        return get_clase(body)
    elif accion == "update":
        return update_clase(body)
    elif accion == "delete":
        return delete_clase(body)
    elif accion == "get_all":
        return get_clases(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Acción no válida", "success": False})
        }

def create_clase(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    curso = collection_cursos.find_one({"nombre": body.get('curso'), "universidad": uni['_id']})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }
    
    alumnos = [{"alumno_id": alumno_id, "estado": "ausente"} for alumno_id in curso["alumnos"]]
    
    nueva_clase = {
        "fecha": datetime.strptime(body.get('fecha'), "%Y-%m-%d-%H-%M"),
        "curso": curso['_id'],
        "universidad": uni['_id'],
        "alumnos": alumnos
    }

    try:
        resultado = collection_clases.insert_one(nueva_clase)
        return {
            'statusCode': 201,
            'body': json.dumps({"message": "Clase creada con éxito", "clase_id": str(resultado.inserted_id), "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al crear clase: {str(e)}", "success": False})
        }

def get_clase(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    curso = collection_cursos.find_one({"nombre": body.get('curso'), "universidad": uni['_id']})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }
    
    clase = collection_clases.find_one({
        "fecha": datetime.strptime(body.get('fecha'), "%Y-%m-%d-%H-%M"),
        "curso": curso['_id'],
        "universidad": uni['_id']
    })

    if clase:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Clase encontrada", "clase": clase, "success": True}, cls=JSONEncoder)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Clase no encontrada", "success": False})
        }

def update_clase(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    curso = collection_cursos.find_one({"nombre": body.get('curso'), "universidad": uni['_id']})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    filtro = {
        "fecha": datetime.strptime(body.get('fecha'), "%Y-%m-%d-%H-%M"),
        "curso": curso['_id'],
        "universidad": uni['_id']
    }

    datos_actualizados = body.get('datos_actualizados')
    
    if "fecha" in datos_actualizados:
        datos_actualizados["fecha"] = datetime.strptime(datos_actualizados["fecha"], "%Y-%m-%d-%H-%M")

    try:
        resultado = collection_clases.update_one(filtro, {"$set": datos_actualizados})
        if resultado.matched_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Clase actualizada con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Clase no encontrada", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al actualizar clase: {str(e)}", "success": False})
        }

def delete_clase(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    curso = collection_cursos.find_one({"nombre": body.get('curso'), "universidad": uni['_id']})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    filtro = {
        "fecha": datetime.strptime(body.get('fecha'), "%Y-%m-%d-%H-%M"),
        "curso": curso['_id'],
        "universidad": uni['_id']
    }

    try:
        resultado = collection_clases.delete_one(filtro)
        if resultado.deleted_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Clase eliminada con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Clase no encontrada", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar clase: {str(e)}", "success": False})
        }

def get_clases(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    curso = collection_cursos.find_one({"nombre": body.get('curso'), "universidad": uni['_id']})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    clases = collection_clases.find({"curso": curso['_id'], "universidad": uni['_id']})

    return {
        'statusCode': 200,
        'body': json.dumps([clase for clase in clases], cls=JSONEncoder)
    }
