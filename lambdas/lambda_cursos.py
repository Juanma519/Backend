import json
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
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

# Handler principal de la Lambda
def lambda_handler(event, context):
    db = connect_to_mongo()
    body = json.loads(event.get('body'))
    accion = body.get('accion')

    if accion == "create_curso":
        return create_curso(body)
    elif accion == "get_curso":
        return get_curso(body)
    elif accion == "update_curso":
        return update_curso(body)
    elif accion == "delete_curso":
        return delete_curso(body)
    elif accion == "add_profesor":
        return add_profesor(body)
    elif accion == "remove_profesor":
        return remove_profesor(body)
    elif accion == "add_alumno":
        return add_alumno(body)
    elif accion == "remove_alumno":
        return remove_alumno(body)
    elif accion == "add_horario":
        return add_horario(body)
    elif accion == "remove_horario":
        return remove_horario(body)
    elif accion == "get_cursos_profesor":
        return get_cursos_profesor(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Acción no válida", "success": False})
        }

# Función para crear un curso
def create_curso(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

    universidad_id = uni['_id']
    collection_cursos.create_index([("nombre", 1), ("universidad", 1)], unique=True)
    
    horarios = []
    for salon, hora_inicio, hora_fin, dia in zip(body.get('salones'), body.get('horas_inicio'), body.get('horas_fin'), body.get('dias')):
        horario = {
            "salon": salon,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
        horarios.append(horario)
        
    nuevo_curso = {
        "nombre": body.get('nombre'),
        "universidad": universidad_id,
        "docentes": [],
        "alumnos": [],
        "fecha_inicio": datetime.strptime(body.get('fecha_inicio'), "%Y-%m-%d"),
        "fecha_fin": datetime.strptime(body.get('fecha_fin'), "%Y-%m-%d"),
        "horario": horarios
    }

    try:
        resultado = collection_cursos.insert_one(nuevo_curso)
        return {
            'statusCode': 201,
            'body': json.dumps({"message": "Curso creado con éxito", "curso_id": str(resultado.inserted_id), "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al crear curso: {str(e)}", "success": False})
        }

# Función para obtener un curso
def get_curso(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

    universidad_id = uni['_id']
    curso = collection_cursos.find_one({"nombre": body.get('nombre'), "universidad": universidad_id})

    if curso:
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Curso encontrado", "curso": curso, "success": True}, cls=JSONEncoder)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

# Función para actualizar un curso
def update_curso(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

    universidad_id = uni['_id']
    curso = collection_cursos.find_one({"nombre": body.get('nombre'), "universidad": universidad_id})

    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    update_fields = {
        "fecha_inicio": datetime.strptime(body.get('fecha_inicio'), "%Y-%m-%d"),
        "fecha_fin": datetime.strptime(body.get('fecha_fin'), "%Y-%m-%d")
    }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$set": update_fields})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Curso actualizado con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al actualizar curso: {str(e)}", "success": False})
        }

# Función para eliminar un curso
def delete_curso(body):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": body.get('universidad')})
    if not uni:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Universidad no encontrada", "success": False})
        }

    universidad_id = uni['_id']
    curso = collection_cursos.find_one({"nombre": body.get('nombre'), "universidad": universidad_id})

    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    try:
        collection_cursos.delete_one({"_id": curso['_id']})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Curso eliminado con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar curso: {str(e)}", "success": False})
        }

# Función para añadir un profesor a un curso
def add_profesor(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']
    collection_profesores = db['profesores']

    profesor = collection_profesores.find_one({"nombre": body.get('profesor')})
    if not profesor:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Profesor no encontrado", "success": False})
        }

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$addToSet": {"docentes": profesor['_id']}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Profesor añadido con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al añadir profesor: {str(e)}", "success": False})
        }

# Función para quitar un profesor de un curso
def remove_profesor(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']
    collection_profesores = db['profesores']

    profesor = collection_profesores.find_one({"nombre": body.get('profesor')})
    if not profesor:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Profesor no encontrado", "success": False})
        }

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$pull": {"docentes": profesor['_id']}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Profesor eliminado con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar profesor: {str(e)}", "success": False})
        }

# Función para añadir un alumno a un curso
def add_alumno(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']
    collection_alumnos = db['alumnos']

    alumno = collection_alumnos.find_one({"nombre": body.get('alumno')})
    if not alumno:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Alumno no encontrado", "success": False})
        }

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$addToSet": {"alumnos": alumno['_id']}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Alumno añadido con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al añadir alumno: {str(e)}", "success": False})
        }

# Función para quitar un alumno de un curso
def remove_alumno(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']
    collection_alumnos = db['alumnos']

    alumno = collection_alumnos.find_one({"nombre": body.get('alumno')})
    if not alumno:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Alumno no encontrado", "success": False})
        }

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$pull": {"alumnos": alumno['_id']}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Alumno eliminado con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar alumno: {str(e)}", "success": False})
        }

# Función para añadir un horario a un curso
def add_horario(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    nuevo_horario = {
        "salon": body.get('salon'),
        "hora_inicio": body.get('hora_inicio'),
        "hora_fin": body.get('hora_fin'),
        "dia": body.get('dia')
    }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$push": {"horario": nuevo_horario}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Horario añadido con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al añadir horario: {str(e)}", "success": False})
        }

# Función para eliminar un horario de un curso
def remove_horario(body):
    db = connect_to_mongo()
    collection_cursos = db['cursos']

    curso = collection_cursos.find_one({"nombre": body.get('curso')})
    if not curso:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Curso no encontrado", "success": False})
        }

    horario_a_eliminar = {
        "salon": body.get('salon'),
        "hora_inicio": body.get('hora_inicio'),
        "hora_fin": body.get('hora_fin'),
        "dia": body.get('dia')
    }

    try:
        collection_cursos.update_one({"_id": curso['_id']}, {"$pull": {"horario": horario_a_eliminar}})
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Horario eliminado con éxito", "success": True})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Error al eliminar horario: {str(e)}", "success": False})
        }

# Función para obtener todos los cursos de un profesor
def get_cursos_profesor(body):
    db = connect_to_mongo()
    collection_profesores = db['profesores']
    collection_cursos = db['cursos']

    profesor = collection_profesores.find_one({"nombre": body.get('profesor')})
    if not profesor:
        return {
            'statusCode': 404,
            'body': json.dumps({"message": "Profesor no encontrado", "success": False})
        }

    cursos = collection_cursos.find({"docentes": profesor['_id']})

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Cursos encontrados", "cursos": list(cursos), "success": True}, cls=JSONEncoder)
    }
