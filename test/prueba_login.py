import requests
import json
import base64

url = 'https://l1hnvthhsf.execute-api.us-east-1.amazonaws.com/default/prueba'

payload = {
    'mail': 'admin@gmail.com',
    'password': '12345'
}

headers = {'Content-Type': 'application/json'}
    
    # Realizar la solicitud POST con las imágenes codificadas en base64
response = requests.post(url, json=payload, headers=headers)

# Imprimir el código de estado y la respuesta
print(response.status_code)
print(response.json())