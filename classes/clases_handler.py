from mongo_connection import connect_to_mongo
from datetime import datetime

def create_clase(fecha, curso_nombre, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso_nombre, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    alumnos = [{"alumno_id": alumno_id, "estado": "ausente"} for alumno_id in curso["alumnos"]]
    
    nueva_clase = {
        "fecha": datetime.strptime(fecha, "%Y-%m-%d-%H-%M"),
        "curso": curso['_id'],
        "universidad": uni['_id'],
        "alumnos": alumnos
    }

    return collection_clases.insert_one(nueva_clase)

def get_clase(fecha, curso_nombre, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso_nombre, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    return collection_clases.find_one({"fecha": datetime.strptime(fecha, "%Y-%m-%d-%H-%M"), "curso": curso['_id'], "universidad": uni['_id']})

def update_clase(fecha, curso_nombre, universidad, datos_actualizados):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso_nombre, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    if "fecha" in datos_actualizados:
        datos_actualizados["fecha"] = datetime.strptime(datos_actualizados["fecha"], "%Y-%m-%d-%H-%M")
    
    collection_clases.update_one({"fecha": datetime.strptime(fecha, "%Y-%m-%d-%H-%M"), "curso": curso['_id'], "universidad": uni['_id']}, {"$set": datos_actualizados})
    
def delete_clase(fecha, curso_nombre, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso_nombre, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    collection_clases.delete_one({"fecha": datetime.strptime(fecha, "%Y-%m-%d-%H-%M"), "curso": curso['_id'], "universidad": uni['_id']})
    
def get_clases(curso_nombre, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']

    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso_nombre, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    return collection_clases.find({"curso": curso['_id'], "universidad": uni['_id']})


def get_clases_curso(curso, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_clases = db['clases']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    curso = collection_cursos.find_one({"nombre": curso, "universidad": uni['_id']})
    if not curso:
        return "Curso no encontrado"
    
    clases = collection_clases.find({"curso": curso["_id"], "universidad": uni['_id']})

    for clase in clases:
        print(clase)
        
    return clases