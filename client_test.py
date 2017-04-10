import json
import requests

with open('./resources/fixtures/seduta.json', 'r') as f:
        seduta = json.load(f)

r = requests.post(
    'http://localhost:8000/api-token-auth/',
    {"username": "mosic", "password": "mosicmosic"}
).json()
jwt_token = r['token']
print("Token retrieved for user mosic: {0}".format(jwt_token))

response = requests.delete(
    'http://localhost:8000/seduta/1/',
    headers={'Authorization': 'JWT ' + jwt_token}
)
print("Seduta removed")


response = requests.post(
    'http://localhost:8000/seduta/',
    json=seduta,
    headers={'Authorization': 'JWT ' + jwt_token}
)
print("Seduta created")

response = requests.put(
    'http://localhost:8000/upload_file/files/Architettura.pdf',
    files={'file': open('/Users/gu/Desktop/Architettura mammatrozzo.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
response = requests.put(
    'http://localhost:8000/upload_file/files/JWTHandbook.pdf',
    files={'file': open('/Users/gu/Desktop/Reading/jwt-handbook.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print("2 files uploaded")

response = requests.get(
    'http://localhost:8000/seduta/1/',
    headers={'Authorization': 'JWT ' + jwt_token}
)
print("Seduta retrieved")

print(response.json())
