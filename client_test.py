import json
import requests


print("Retrieving token for user mosic")
r = requests.post(
    'http://localhost:8000/api-token-auth/',
    {"username": "mosic", "password": "mosicmosic"}
)
jwt_token = r.json()['token']
print(r)
print(jwt_token)
print("")


print("Removing seduta metadata recursively")
response = requests.delete(
    'http://localhost:8000/seduta/1/',
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


print("Creating seduta from json")
with open('./resources/fixtures/seduta.json', 'r') as f:
        seduta = json.load(f)
response = requests.post(
    'http://localhost:8000/seduta/',
    json=seduta,
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading Architettura file")
response = requests.put(
    'http://localhost:8000/upload_file/files/Architettura.pdf',
    files={'file': open('/Users/gu/Desktop/Architettura mammatrozzo.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading jwt-handbook file")
response = requests.put(
    'http://localhost:8000/upload_file/files/JWTHandbook.pdf',
    files={'file': open('/Users/gu/Desktop/Reading/jwt-handbook.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading file with no corresponding record in DB")
response = requests.put(
    'http://localhost:8000/upload_file/fils/JWTHandbook.pdf&format=json',
    files={'file': open('/Users/gu/Desktop/Reading/jwt-handbook.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


print("Retrieving full seduta")
response = requests.get(
    'http://localhost:8000/seduta/1/',
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print(response.json())
