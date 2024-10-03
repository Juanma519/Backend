import requests
import json
import base64

url = 'https://l1hnvthhsf.execute-api.us-east-1.amazonaws.com/default/prueba_reko'

# Ruta de las imágenes
image_path1 = r"C:\Users\mrbla\Downloads\messi2.jpg"
image_path2 = r"C:\Users\mrbla\Downloads\messi1.png"

# Leer las imágenes en binario y convertirlas a base64 para enviarlas en JSON
with open(image_path1, 'rb') as image_file1, open(image_path2, 'rb') as image_file2:
    image_data1 = base64.b64encode(image_file1.read()).decode('utf-8')
    image_data2 = base64.b64encode(image_file2.read()).decode('utf-8')

    payload = {
        'file1': image_data1,
        'file2': image_data2
    }

    headers = {'Content-Type': 'application/json'}
    
    # Realizar la solicitud POST con las imágenes codificadas en base64
    response = requests.post(url, json=payload, headers=headers)

# Imprimir el código de estado y la respuesta
print(response.status_code)
print(response.json())