import requests
import json

# URL de la API Lambda
url = 'https://l1hnvthhsf.execute-api.us-east-1.amazonaws.com/default/universidad'

def test_lambda(payload):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

# Prueba de creación de usuario
payload_get_salones = {
    "accion": "get_salones",
    "nombre": "Universidad de Montevideo"
}
test_lambda(payload_get_salones)