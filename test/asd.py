from pymongo import MongoClient


client = MongoClient("mongodb+srv://mrasnik:matias1234@prueba.iwcws.mongodb.net/?retryWrites=true&w=majority&appName=prueba")
db = client['prueba']
collection_universidades = db['universidades']
universidad = collection_universidades.find_one({"nombre": "Universidad de Montevideo"})
salones = universidad.get('salones')

print(universidad)
print(salones[1])