from mongo_connection import connect_to_mongo
#from argon2 import PasswordHasher

def create_usuario(nombre, apellido, passw, tipo, mail, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_alumnos = db['alumnos']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": universidad})

    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']

    #passw_encriptada = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
    
    #ph = PasswordHasher()
    #passw_encriptada = ph.hash("mi_contraseña")

    collection_alumnos.create_index([("mail", 1), ("universidad", 1)], unique=True)
    
    nuevo_usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "password": passw, #passw_encriptada,
        "tipo": tipo,
        "universidad": universidad_id,
        "mail": mail
    }
    
    try:
        resultado = collection_usuarios.insert_one(nuevo_usuario)
        return f"Usuario creado con ID: {resultado.inserted_id}"
    except Exception as e:
        return f"Error al crear usuario: {e}"

def get_usuario(mail, universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    
    universidad = collection_universidades.find_one({"nombre": universidad})
    
    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    usuario = collection_usuarios.find_one({"mail": mail, "universidad": universidad_id})

    if usuario:
        return {k: v for k, v in usuario.items() if k != "password"}
    else:
        return "Usuario no encontrado"

def update_usuario(mail, universidad, datos_actualizados):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    universidad = collection_universidades.find_one({"nombre": universidad})
    
    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    filtro = {"mail": mail, "universidad": universidad_id}

    if "password" in datos_actualizados:
        datos_actualizados["password"] =   passw_encriptada = bcrypt.hashpw(datos_actualizados["password"].encode('utf-8'), bcrypt.gensalt())

    try:
        resultado = collection_usuarios.update_one(filtro, {"$set": datos_actualizados})
        if resultado.matched_count > 0:
            return "Usuario actualizado con éxito"
        else:
            return "No se encontró al usuario"
    except Exception as e:
        return f"Error al actualizar usuario: {e}"

def delete_usuario(data):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    uni = collection_universidades.find_one({"nombre": data['universidad']})
    
    if not uni:
        return "Universidad no encontrada"
    
    universidad_id = uni['_id']
    filtro = {"mail": data['mail'], "universidad": universidad_id}

    try:
        resultado = collection_usuarios.delete_one(filtro)
        if resultado.deleted_count > 0:
            return "Usuario eliminado con éxito"
        else:
            return "No se encontró al usuario"
    except Exception as e:
        return f"Error al eliminar usuario: {e}"

def login(data):
    db = connect_to_mongo()
    collection_usuarios = db['usuarios']
    usuario = collection_usuarios.find_one({"mail": data['mail']}) 

    if usuario:
        if data['passw'] == usuario["password"]:
            return f"Login exitoso para el usuario: {usuario['nombre']} {usuario['apellido']}"
        else:
            return "Contraseña incorrecta"
    else:
        return "Usuario no encontrado"
    
    
def get_usuarios_universidad(universidad):
    db = connect_to_mongo()
    collection_universidades = db['universidades']
    collection_usuarios = db['usuarios']
    
    universidad = collection_universidades.find_one({"nombre": universidad})
    
    if not universidad:
        return "Universidad no encontrada"
    
    universidad_id = universidad['_id']
    usuarios = collection_usuarios.find({"universidad": universidad_id})
    
    return [usuario for usuario in usuarios]

