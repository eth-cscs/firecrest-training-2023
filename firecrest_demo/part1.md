# Basic usage of FirecREST through the API directly

## HTTP requests

[FirecREST API]((https://firecrest-api.cscs.ch/)) is based on REST principles: data resources are accessed via standard HTTP requests to an API endpoint.

Every request is made of:

1. the endpoint or requested URL
1. the method (one of GET, POST, PUT and DELETE depending on the appropriate action)
1. the headers (metadata necessary for the request)
1. the body (form data, files to be uploaded, etc)

The necessary information for every call is passed through query parameters, the headers and the body of the request.

Here is a quick overview of the methods:
| Method | Description                            |
| ------ | -------------------------------------- |
| GET    | Used for retrieving resources.         |
| POST   | Used for creating/updating resources.  |
| PUT    | Used for creating/updating resources.* |
| DELETE | Used for deleting resources.           |

> \* The difference between `POST` and `PUT` is that `PUT` requests are idempotent. That is, calling the same `PUT` request multiple times will always produce the same result. In contrast, calling a `POST` request repeatedly have side effects of creating the same resource multiple times.

Similar to the requests, the response of FirecREST will consist of:

1. a status code
1. the headers
1. the body in json form

Here is a quick overview of the status codes and their meaning.
| #   | Category      | Description |
| --- | ------------- | ----------- |
| 1xx | Informational | Communicates transfer protocol-level information. |
| 2xx | Success | Indicates that the client’s request was accepted successfully. |
| 3xx | Redirection | Indicates that the client must take some additional action in order to complete their request. |
| 4xx | Client Error | This category of error status codes points the finger at clients. |
| 5xx | Server Error | The server takes responsibility for these error status codes. |


## Obtain credentials

All the requests in the FirecREST API require authorization, in the form of an *access token*.
This token allows you to make requests on behalf of the authenticated user and is provided by Keycloak.
It has to be included in the header of all the API calls, but you should keep in mind that validation tokens usually have an expiration date and are short-lived.

In order to get an access token we need to make a `GET` request to `https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token`:

In python you can try it like this:

```python
import requests
import os
import json


CLIENT_ID = os.environ.get("FIRECREST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FIRECREST_CLIENT_SECRET")
AUTH_TOKEN_URL = os.environ.get("AUTH_TOKEN_URL")

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}
response = requests.post(
    AUTH_TOKEN_URL,
    data=data,
)

print(f"Status code: {response.status_code}")
print(f"Headers:\n{json.dumps(dict(response.headers), indent=4)}")
print(f"JSON:\n{json.dumps(response.json(), indent=4)}")
```

If you have `curl` installed the request will look like this:
```bash
curl -s -X POST "$(AUTH_TOKEN_URL)" \
     --data "grant_type=client_credentials" \
     --data "client_id=$(FIRECREST_CLIENT_ID)" \
     --data "client_secret=$(FIRECREST_CLIENT_SECRET)"
```

Example response:
```json
{
    "access_token":"ey...",
    "expires_in":300,
    "refresh_expires_in":0,
    "token_type":"Bearer",
    "not-before-policy":0,
    "scope":"firecrest profile email"
}
```

### [Optional] Inspecting the token with jwt

You can try inspecting an access token with

```python
decoded = jwt.decode(
    response.json()["access_token"],
    options={"verify_signature": False},
)
print("Decoded token:", json.dumps(decoded, indent=4))
```

## Making our first request to the API

After we obtain the token we can use this to make our first request to FirecREST:

To test the credentials we can use a simple call to the `Status` microservice. We can call the [status/systems](https://firecrest-api.cscs.ch/#/Status/get_status_systems) endpoint with a `GET` operation to get more information about the systems that are available through this deployment fo FirecREST. The access token has to be included in the header.

```python

FIRECREST_URL = os.environ.get("FIRECREST_URL")

response = requests.get(
    url=f'{FIRECREST_URL}/status/systems',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

print(json.dumps(response.json(), indent=4))
```

We should get some response like this:
```json
{
    "description": "List of systems with status and description.",
    "out": [
        {
            "description": "Filesystem /scratch/e1000 is not available",
            "status": "not available",
            "system": "eiger"
        },
        {
            "description": "System ready",
            "status": "available",
            "system": "daint"
        }
    ]
}
```

## Interracting with the scheduler

FirecREST offers three basic functionalities of the scheduler:
1. submit jobs on behalf of a user,
1. poll for the jobs of the user and
1. cancel jobs.

## The `compute` workflow

See the workflow [here](compute_sbatch.pdf).

On a job scheduler like Slurm, every job has a unique `job ID`, which is created when a job is submitted and can be used to track the state of the job. With calls like `squeue` and `sacct` the user can see the state of the job (RUNNING, COMPLETED, etc.) as well as get information for the job.
Similarly, for every task FirecREST will assign a `task ID` with which the user can track the state of the request and get information about it.

## Implement the job submission with direct calls to the api:

```python
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
        continue

    break

print(json.dumps(response.json()["task"]["data"], indent=4))
```