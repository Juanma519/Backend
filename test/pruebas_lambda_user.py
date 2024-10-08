import requests
import json

# URL de la API Lambda
url = 'https://l1hnvthhsf.execute-api.us-east-1.amazonaws.com/default/usuarios'


def test_lambda(payload):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

# Prueba de creación de usuario
payload_create = {
    "accion": "create",
    "nombre": "Juan",
    "apellido": "Perez",
    "password": "123456",  # Sin encriptación
    "tipo": "alumno",
    "mail": "juan.perez@example.com",
    "universidad": "Universidad de Montevideo"
}
#test_lambda(payload_create)

# Prueba de login
payload_login = {
    "accion": "login",
    "mail": "juan.perez@example.com",
    "password": "123456"  # Sin encriptación
}
test_lambda(payload_login)

# Prueba de obtener usuario
payload_get = {
    "accion": "get",
    "mail": "juan.perez@example.com",
    "universidad": "Universidad de Montevideo"
}
#test_lambda(payload_get)

# Prueba de actualización de usuario
payload_update = {
    "accion": "update",
    "mail": "juan.perez@example.com",
    "universidad": "Universidad de Montevideo",
    "datos_actualizados": {
        "nombre": "Juanito"
    }
}
#test_lambda(payload_update)

# Prueba de eliminación de usuario
payload_delete = {
    "accion": "delete",
    "mail": "juan.perez@example.com",
    "universidad": "Universidad de Montevideo"
}
#test_lambda(payload_delete)
