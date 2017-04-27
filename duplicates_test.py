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


print("Creating seduta from json")
with open('./resources/fixtures/duplicates_1.json', 'r') as f:
    seduta_1 = json.load(f)

response = requests.post(
    '{0}/precipe'.format(service_url),
    json=seduta_1,
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading Torino file. First time.")
response = requests.put(
    '{0}/upload_file/files/torino.pdf'.format(service_url),
    files={'file': open('./resources/fixtures/docs/torino.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


with open('./resources/fixtures/duplicates_2.json', 'r') as f:
    seduta_2 = json.load(f)

response = requests.post(
    '{0}/precipe'.format(service_url),
    json=seduta_2,
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")

print("Uploading Torino file. Second time.")
response = requests.put(
    '{0}/upload_file/files/torino.pdf'.format(service_url),
    files={'file': open('./resources/fixtures/docs/torino.pdf', 'rb')},
    headers={'Authorization': 'JWT ' + jwt_token}
)
print(response)
print("")


# removing seduta 2
print("Retrieving seduta internal id")
response = requests.get(
    '{0}/seduta/precipe/2'.format(service_url),
    headers={'Authorization': 'JWT ' + jwt_token}
)
if 'id' in response.json():
    print("Delete seduta 2")
    seduta_id = response.json()['id']

    response = requests.delete(
        '{0}/precipe/{1}'.format(service_url, seduta_id),
        headers={'Authorization': 'JWT ' + jwt_token}
    )
    print(response)

# removing seduta 3
print("Retrieving seduta internal id")
response = requests.get(
    '{0}/seduta/precipe/3'.format(service_url),
    headers={'Authorization': 'JWT ' + jwt_token}
)
if 'id' in response.json():
    seduta_id = response.json()['id']

    print("Delete seduta 3")
    response = requests.delete(
        '{0}/precipe/{1}'.format(service_url, seduta_id),
        headers={'Authorization': 'JWT ' + jwt_token}
    )
    print(response)
