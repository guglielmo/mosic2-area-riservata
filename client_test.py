import json
import requests


# test locally or with remote service_url
service_url = "http://localhost:8000"
password = 'mosicmosic'

# service_url = "http://area-riservata.mosic2.celata.com"
# password = 'cowpony-butter-vizor'

print("Retrieving token for user mosic")
r = requests.post(
    '{0}/api-token-auth/'.format(service_url),
    {"username": "mosic", "password": password}
)
jwt_token = r.json()['token']
print(r)
print(jwt_token)
print("")


print("Retrieving seduta internal id")
response = requests.get(
    '{0}/seduta/precipe/1'.format(service_url),
    headers={'Authorization': 'JWT ' + jwt_token}
)
seduta_id = response.json()['id']
print("")

print("Removing seduta metadata recursively")
response = requests.delete(
    '{0}/precipe/{1}'.format(service_url, seduta_id),
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


print("Creating seduta from json")
with open('./resources/fixtures/seduta.json'.format(service_url), 'r') as f:
        seduta = json.load(f)
response = requests.post(
    '{0}/precipe'.format(service_url),
    json=seduta,
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading Architettura file")
response = requests.put(
    '{0}/upload_file/files/Architettura.pdf'.format(service_url),
    files={'file': open('./resources/fixtures/docs/architettura.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading jwt-handbook file")
response = requests.put(
    '{0}/upload_file/files/JWTHandbook.pdf'.format(service_url),
    files={'file': open('./resources/fixtures/docs/jwt_handbook.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading file with no corresponding record in DB")
response = requests.put(
    '{0}/upload_file/fils/JWTHandbook.pdf&format=json'.format(service_url),
    files={'file': open('./resources/fixtures/docs/jwt_handbook.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


print("Retrieving seduta internal id")
response = requests.get(
    '{0}/seduta/precipe/1'.format(service_url),
    headers={'Authorization': 'JWT ' + jwt_token}
)
seduta_id = response.json()['id']
seduta_url = response.json()['url']
print("")

print("Retrieving full seduta")
response = requests.get(
    '{0}/precipe/{1}'.format(service_url, seduta_id),
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)

print(response.json())

print("public url: {0}".format(seduta_url))
