from mongo_connection import connect_to_mongo
from datetime import datetime


def create_curso(nombre, universidad, fecha_inicio, fecha_fin, salones, horas_inicio, horas_fin, dias):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})

    if not uni:
        return "Universidad no encontrada"

    universidad_id = uni['_id']

    collection_cursos.create_index([("nombre", 1), ("universidad", 1)], unique=True)
    
    horarios = []
    for salon, hora_inicio, hora_fin, dia in zip(salones, horas_inicio, horas_fin, dias):
        horario = {
            "salon": salon,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
        horarios.append(horario)
        
    nuevo_curso = {
        "nombre": nombre,
        "universidad": universidad_id,
        "docentes": [],
        "alumnos": [],
        "fecha_inicio": datetime.strptime(fecha_inicio, "%Y-%m-%d"),
        "fecha_fin": datetime.strptime(fecha_fin, "%Y-%m-%d"),
        "horario": horarios 
    }

    try:
        resultado = collection_cursos.insert_one(nuevo_curso)
        return f"Curso creado con ID: {resultado.inserted_id}"
    except Exception as e:
        return f"Error al crear curso: {e}"

def get_curso(nombre, universidad):   
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    
    if not uni:
        return "Universidad no encontrada"
    
    universidad_id = uni['_id']

    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})

    if curso:
        return curso
    else:
        return "Curso no encontrado"
    
def update_curso(nombre, universidad, datos_actualizados):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    
    if not uni:
        return "Universidad no encontrada"

    universidad_id = uni['_id']
    try:
        resultado = collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$set": datos_actualizados})
        if resultado.matched_count > 0:
            return "Curso actualizado con éxito"
        else:
            return "No se encontró el curso"
    except Exception as e:
        return f"Error al actualizar curso: {e}"
    
def eliminar_curso(nombre, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    
    if not uni:
        return "Universidad no encontrada"
    
    universidad_id = uni['_id']

    try:
        resultado = collection_cursos.delete_one({"nombre": nombre, "universidad": universidad_id})
        if resultado.deleted_count > 0:
            return "Curso eliminado con éxito"
        else:
            return "No se encontró el curso"
    except Exception as e:
        return f"Error al eliminar curso: {e}"
    
def add_profesor(nombre, universidad, mail_profesor):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_usuarios = db['usuarios']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    usuario = collection_usuarios.find_one({"mail": mail_profesor, "universidad": universidad_id})
    if not usuario:
        return "Usuario no encontrado"
    
    return collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$push": {"docentes": usuario['_id']}})

def remove_profesor(nombre, universidad, mail_profesor):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_usuarios = db['usuarios']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    usuario = collection_usuarios.find_one({"mail": mail_profesor, "universidad": universidad_id})
    if not usuario:
        return "Usuario no encontrado"
    
    return collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$pull": {"docentes": usuario['_id']}})

def add_alumno(nombre, universidad, ci):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_alumnos = db['alumnos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    alumno = collection_alumnos.find_one({"ci": ci, "universidad": universidad_id})
    if not alumno:
        return "Alumno no encontrado"
    
    return collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$push": {"alumnos": alumno['_id']}})

def remove_alumno(nombre, universidad, ci):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    collection_alumnos = db['alumnos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    alumno = collection_alumnos.find_one({"ci": ci, "universidad": universidad_id})
    if not alumno:
        return "Alumno no encontrado"
    
    return collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$pull": {"alumnos": alumno['_id']}})

def add_horario(nombre, universidad, salon, horas_inicio, horas_fin, dias):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    for salon, hora_inicio, hora_fin, dia in zip(salon, horas_inicio, horas_fin, dias):
        horario = {
            "salon": salon,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
        collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$push": {"horario": horario}})
    
    return "Horario agregado con éxito"

def remove_horario(nombre, universidad, salon, horas_inicio, horas_fin, dias):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos = db['cursos']
    
    uni = collection_universidades.find_one({"nombre": universidad})
    if not uni:
        return "Universidad no encontrada"
    universidad_id = uni['_id']
    
    curso = collection_cursos.find_one({"nombre": nombre, "universidad": universidad_id})
    if not curso:
        return "Curso no encontrado"

    for salon, hora_inicio, hora_fin, dia in zip(salon, horas_inicio, horas_fin, dias):
        horario = {
            "salon": salon,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "dia": dia
        }
        collection_cursos.update_one({"nombre": nombre, "universidad": universidad_id}, {"$pull": {"horario": horario}})
    
    return "Horario eliminado con éxito"

def get_cursos_profesor(mail_profesor):
    db = connect_to_mongo()
    collection_cursos = db['cursos']
    collection_usuarios = db['usuarios']
    
    usuario = collection_usuarios.find_one({"mail": mail_profesor})
    if not usuario:
        return "Usuario no encontrado"
    
    cursos = collection_cursos.find({"docentes": usuario['_id']})
    
    for curso in cursos:
        print(curso)

    return cursos

