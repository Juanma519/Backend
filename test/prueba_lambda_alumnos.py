import requests
import json

# URL de la API Lambda
url = 'https://l1hnvthhsf.execute-api.us-east-1.amazonaws.com/default/prueba'

def test_lambda(payload):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

# Prueba de creación de alumno
payload_create_alumno = {
    "accion": "create_alumno",
    "nombre": "Carlos",
    "apellido": "Sanchez",
    "foto": "ruta/foto/carlos.jpg",  # Suponiendo que tienes una ruta para la imagen
    "universidad": "Universidad de Montevideo",
    "ci": "12345678"
}
test_lambda(payload_create_alumno)

# Prueba de obtención de un alumno
payload_get_alumno = {
    "accion": "get_alumno",
    "ci": "12345678",
    "universidad": "Universidad de Montevideo"
}
test_lambda(payload_get_alumno)

# Prueba de actualización de alumno
payload_update_alumno = {
    "accion": "update_alumno",
    "ci": "12345678",
    "universidad": "Universidad de Montevideo",
    "datos_actualizados": {
        "nombre": "Carlos Alberto",
        "apellido": "Sanchez Garcia"
    }
}
test_lambda(payload_update_alumno)

# Prueba de eliminación de alumno
payload_delete_alumno = {
    "accion": "delete_alumno",
    "ci": "12345678",
    "universidad": "Universidad de Montevideo"
}
test_lambda(payload_delete_alumno)

# Prueba de obtener todos los alumnos de una universidad
payload_get_alumnos_universidad = {
    "accion": "get_alumnos_universidad",
    "universidad": "Universidad de Montevideo"
}
test_lambda(payload_get_alumnos_universidad)
