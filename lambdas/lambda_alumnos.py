import json
from pymongo import MongoClient
from bson import ObjectId

def connect_to_mongo():
    client = MongoClient("mongodb+srv://mrasnik:matias1234@prueba.iwcws.mongodb.net/?retryWrites=true&w=majority&appName=prueba")
    db = client['prueba']
    return db

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o) 
        return super().default(o)

def lambda_handler(event, context):
    db = connect_to_mongo()
    
    # Obtener el cuerpo de la solicitud
    body = json.loads(event.get('body'))
    accion = body.get('accion')

    if accion == "create_alumno":
        return create_alumno(body)
    elif accion == "get_alumno":
        return get_alumno(body)
    elif accion == "update_alumno":
        return update_alumno(body)
    elif accion == "delete_alumno":
        return delete_alumno(body)
    elif accion == "get_alumnos_universidad":
        return get_alumnos_universidad(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Acción no válida", "success": False})
        }

def create_alumno(body):
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
    nuevo_alumno = {
        "nombre": body.get('nombre'),
        "apellido": body.get('apellido'),
        "foto": body.get('foto'),
        "universidad": universidad_id,
        "ci": body.get('ci')
    }
    
    try:
        resultado = collection_alumnos.insert_one(nuevo_alumno)
        return {
            'statusCode': 201,
            'body': json.dumps({"message": "Alumno creado con éxito", "alumno_id": str(resultado.inserted_id), "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al crear alumno: {str(e)}", "success": False})
        }

def get_alumno(body):
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
    alumno = collection_alumnos.find_one({"ci": body.get('ci'), "universidad": universidad_id})

    if alumno:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({"message": "Alumno encontrado", "alumno": alumno, "success": True}, cls=JSONEncoder)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Alumno no encontrado", "success": False})
        }

def update_alumno(body):
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
    filtro = {"ci": body.get('ci'), "universidad": universidad_id}
    datos_actualizados = body.get('datos_actualizados')
    
    try:
        resultado = collection_alumnos.update_one(filtro, {"$set": datos_actualizados})
        if resultado.matched_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Alumno actualizado con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Alumno no encontrado", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al actualizar alumno: {str(e)}", "success": False})
        }

def delete_alumno(body):
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
    filtro = {"ci": body.get('ci'), "universidad": universidad_id}

    try:
        resultado = collection_alumnos.delete_one(filtro)
        if resultado.deleted_count > 0:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Alumno eliminado con éxito", "success": True})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"message": "Alumno no encontrado", "success": False})
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar alumno: {str(e)}", "success": False})
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
    alumnos = collection_alumnos.find({"universidad": universidad_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps([alumno for alumno in alumnos], cls=JSONEncoder)
    }
