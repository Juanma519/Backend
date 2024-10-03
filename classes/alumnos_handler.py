from mongo_connection import connect_to_mongo

def create_alumno(nombre, apellido, foto, universidad, ci):
    db = connect_to_mongo()
    collection_alumnos = db['alumnos']
    collection_alumnos.create_index([("ci", 1), ("universidad", 1)], unique=True)
    
    universidad = db['universidades'].find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    
    alumno = {
        "nombre": nombre,
        "apellido": apellido,
        "foto": foto,
        "universidad": universidad_id,
        "ci": ci
    }
    
    return collection_alumnos.insert_one(alumno)

def update_alumno(ci, universidad, cambios): 
    db = connect_to_mongo()
    collection_alumnos = db['alumnos']
    
    universidad = db['universidades'].find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    
    return collection_alumnos.update_one({"ci": ci, "universidad": universidad_id}, {"$set": cambios})
    
def delete_alumno(ci, universidad):
    db = connect_to_mongo()
    collection_alumnos = db['alumnos']
    
    universidad = db['universidades'].find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    
    return collection_alumnos.delete_one({"ci": ci, "universidad": universidad_id})

def get_alumno(ci, universidad):
    db = connect_to_mongo()
    collection_alumnos = db['alumnos']
    
    universidad = db['universidades'].find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    
    alumnos = collection_alumnos.find_one({"ci": ci, "universidad": universidad_id})
    return alumnos