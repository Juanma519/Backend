from mongo_connection import connect_to_mongo
import boto3
from botocore.exceptions import ClientError

def generate_image_bytes(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        return imagen.read()

def face_comparison(ruta_imagen1,ruta_imagen2):
    bytes_1 = generate_image_bytes(ruta_imagen1)
    bytes_2 = generate_image_bytes(ruta_imagen2)
    
    cliente = boto3.client('rekognition', region_name = 'us-east-1')

    try:
        respuesta = cliente.compare_faces(SourceImage = {'Bytes' : bytes_1}, 
                                          TargetImage = {'Bytes': bytes_2},
                                          SimilarityThreshold = 60,
                                          QualityFilter = 'NONE')

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        # UnmatchedFaces
        for i in respuesta['UnmatchedFaces']:
            print(i)
            print('\n')

        # FaceMatches
        for i in respuesta['FaceMatches']:
            print('Similarity: ', i['Similarity'])           

def add_face_collection(nombre_coleccion,ruta_imagen,name):
    cliente = boto3.client('rekognition', region_name = 'us-east-1')
    bytes_1 = generate_image_bytes(ruta_imagen)
    nombre_imagen = name
    try:
        response = cliente.index_faces(CollectionId = nombre_coleccion,
                                       Image = {'Bytes':bytes_1},
                                       ExternalImageId = nombre_imagen,
                                       MaxFaces = 1,
                                       QualityFilter = "AUTO")
    
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def remove_face_collection(nombre_coleccion,face_id_aws):
    cliente = boto3.client('rekognition', region_name = 'us-east-1')
    try:
        response = cliente.delete_faces(CollectionId = nombre_coleccion,FaceIds = [face_id_aws])
        print('Rostros eliminados: ' + str(response['DeletedFaces']))
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def list_face_collection(nombre_coleccion):
    print("Listando rostros en la coleccion: ")
    cliente = boto3.client('rekognition', region_name = 'us-east-1')
    try:
        response = cliente.list_faces(CollectionId = nombre_coleccion)
        tokens = True
        while tokens:
            faces = response['Faces']
    
            for face in faces:
                print('Identificador AWS: ', face['FaceId'])
                print('Identificador personal: ' + face['ExternalImageId'])
            if 'NextToken' in response:
                nextToken = response['NextToken']
                response = cliente.list_faces(CollectionId = nombre_coleccion,NextToken = nextToken)
            else:
                tokens = False
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def compare_face_collection(nombre_coleccion,ruta_imagen):
    cliente = boto3.client('rekognition', region_name = 'us-east-1')
    bytes_1 = generate_image_bytes(ruta_imagen)
    try:
        response = cliente.search_faces_by_image(CollectionId = nombre_coleccion,
                                                 Image = {'Bytes':bytes_1},
                                                 FaceMatchThreshold = 85)
        rostrosCoincidentes = response['FaceMatches']
        for i in rostrosCoincidentes:
            print('Similarity: ' + str(i['Similarity']))
            print('Identificador AWS: ' + i['Face']['FaceId'])
            print('Identificador personal: ' + i['Face']['ExternalImageId'])

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)
