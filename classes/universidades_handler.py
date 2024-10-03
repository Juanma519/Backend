from mongo_connection import connect_to_mongo

def create_universidad(nombre):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_universidades.create_index([("nombre", 1)], unique=True)
    universidad = {
        "nombre": nombre,
        "salones": []
    }
    collection_universidades.insert_one(universidad)
    return universidad

def update_nombre_universidad(nombre, nuevo_nombre):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.update_one({"nombre": nombre}, {"$set": {"nombre": nuevo_nombre}})
       
def delete_universidad(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.delete_one({"nombre": universidad})

def get_universidad(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    universidad = collection_universidades.find_one({"nombre": universidad})
    return universidad

def get_universidades():
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    universidades = collection_universidades.find()
    return universidades

def create_salon(salon, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.update_one({"nombre": universidad}, {"$push": {"salones": salon}})

def update_nombre_salon(salon, nuevo_salon, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.update_one({"nombre": universidad}, {"$set": {"salones.$[elem]": nuevo_salon}}, array_filters=[{"elem": salon}])

def delete_salon(salon, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.update_one({"nombre": universidad}, {"$pull": {"salones": salon}})

def get_salones(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    return collection_universidades.find({"nombre": universidad})

def get_alumnos_universidad(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_alumnos = db['alumnos']
    universidad = collection_universidades.find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']  

    return list(collection_alumnos.find({"universidad": universidad_id}))

def get_cursos_universidad(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_cursos= db['cursos']
    universidad = collection_universidades.find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']  

    return list(collection_cursos.find({"universidad": universidad_id}))

#TODO get usuarios universidad