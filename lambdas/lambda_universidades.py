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
    collection_universidades = db['universidades']
    
    # Obtener el cuerpo de la solicitud
    body = json.loads(event.get('body'))
    accion = body.get('accion')

    if accion == "create_universidad":
        return create_universidad(body)
    elif accion == "update_universidad":
        return update_nombre_universidad(body)
    elif accion == "delete_universidad":
        return delete_universidad(body)
    elif accion == "get_universidad":
        return get_universidad(body)
    elif accion == "get_universidades":
        return get_universidades()
    elif accion == "create_salon":
        return create_salon(body)
    elif accion == "update_salon":
        return update_nombre_salon(body)
    elif accion == "delete_salon":
        return delete_salon(body)
    elif accion == "get_salones":
        return get_salones(body)
    elif accion == "get_alumnos_universidad":
        return get_alumnos_universidad(body)
    elif accion == "get_cursos_universidad":
        return get_cursos_universidad(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Acción no válida", "success": False})
        }

def create_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_universidades.create_index([("nombre", 1)], unique=True)
    universidad = {
        "nombre": body.get('nombre'),
        "salones": []
    }
    try:
        collection_universidades.insert_one(universidad)
        return {
            'statusCode': 201,
            'body': json.dumps({"message": "Universidad creada con éxito", "universidad": universidad, "success": True}, cls=JSONEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al crear universidad: {str(e)}", "success": False})
        }

def update_nombre_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    resultado = collection_universidades.update_one({"nombre": body.get('nombre')}, {"$set": {"nombre": body.get('nuevo_nombre')}})
    
    if resultado.matched_count > 0:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Nombre de la universidad actualizado con éxito", "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

def delete_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    resultado = collection_universidades.delete_one({"nombre": body.get('nombre')})
    
    if resultado.deleted_count > 0:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Universidad eliminada con éxito", "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

def get_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    universidad = collection_universidades.find_one({"nombre": body.get('nombre')})
    
    if universidad:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Universidad encontrada", "universidad": universidad, "success": True}, cls=JSONEncoder)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

def get_universidades():
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    universidades = collection_universidades.find()

    return {
        'statusCode': 200,
        'body': json.dumps([uni for uni in universidades], cls=JSONEncoder)
    }

def create_salon(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    resultado = collection_universidades.update_one({"nombre": body.get('universidad')}, {"$push": {"salones": body.get('salon')}})
    
    if resultado.matched_count > 0:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Salón creado con éxito", "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

def update_nombre_salon(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    resultado = collection_universidades.update_one({"nombre": body.get('universidad')}, {"$set": {"salones.$[elem]": body.get('nuevo_salon')}}, array_filters=[{"elem": body.get('salon')}])
    
    if resultado.matched_count > 0:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Salón actualizado con éxito", "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad o salón no encontrado", "success": False})
        }

def delete_salon(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    resultado = collection_universidades.update_one({"nombre": body.get('universidad')}, {"$pull": {"salones": body.get('salon')}})
    
    if resultado.matched_count > 0:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Salón eliminado con éxito", "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad o salón no encontrado", "success": False})
        }

def get_salones(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})
    
    if universidad:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Salones encontrados", "salones": universidad.get('salones'), "success": True})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

def get_alumnos_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_alumnos = db['alumnos']
    
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    alumnos = list(collection_alumnos.find({"universidad": universidad_id}))

    return {
        'statusCode': 200,
        'body': json.dumps(alumnos, cls=JSONEncoder)
    }

def get_cursos_universidad(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    universidad = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not universidad:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }
    
    universidad_id = universidad['_id']
    cursos = list(collection_cursos.find({"universidad": universidad_id}))

    return {
        'statusCode': 200,
        'body': json.dumps(cursos, cls=JSONEncoder)
    }
