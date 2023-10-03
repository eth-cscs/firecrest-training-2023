import requests
import os
import json
import time


CLIENT_ID = os.environ.get("FIRECREST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FIRECREST_CLIENT_SECRET")
AUTH_TOKEN_URL = os.environ.get("AUTH_TOKEN_URL")
FIRECREST_URL = os.environ.get("FIRECREST_URL")

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}
response = requests.post(
    AUTH_TOKEN_URL,
    data=data,
)

TOKEN = response.json()["access_token"]

# Submit a job
localPath = 'script.sh'

response = requests.post(
    url=f'{FIRECREST_URL}/compute/jobs/upload',
    headers={'Authorization': f'Bearer {TOKEN}',
             'X-Machine-Name': "daint"},
    files={'file': open(localPath, 'rb')}
)

print(json.dumps(response.json(), indent=4))

taskid = response.json()['task_id']

while True:
    response = requests.get(
        url=f'{FIRECREST_URL}/tasks/{taskid}',
        headers={'Authorization': f'Bearer {TOKEN}'}
    )

    print(json.dumps(response.json(), indent=4))

    if int(response.json()["task"]["status"]) < 200:
        time.sleep(5)
        continue

    break

print(json.dumps(response.json()["task"]["data"], indent=4))

# As an excercise try to poll for a job
