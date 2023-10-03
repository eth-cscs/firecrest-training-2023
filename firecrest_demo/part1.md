# Basic usage of FirecREST

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

## How to use pyfirecrest

### Setting up the authentication

You can take care of the access token by yourself any way you want, or even better use a library to take care of this for you, depending on the **grant type** of your client. What pyFirecREST will need in the end is only a python object with the method `get_access_token()`, that when called will provide a valid access token.

Let’s say for example you have somehow obtained a long-lasting access token. The Authorization class you would need to make and give to Firecrest would look like this:

```python
class MyAuthorizationClass:
    def __init__(self):
        pass

    def get_access_token(self):
        return <TOKEN>
```

If you want to use the `Client Credentials` authorization grant, you can use the `ClientCredentialsAuth` class from pyFirecREST and setup the authorization object like this:

```python
import firecrest as f7t

keycloak = f7t.ClientCredentialsAuth(
    <client_id>, <client_secret>, <token_uri>
)
```

The `ClientCredentialsAuth` object will try to make the minimum requests that are necessary by reusing the access token while it is valid. More info on parameterizing it in the [docs]().


### Example of calls with pyfirecrest

Your starting point to use pyFirecREST will be the creation of a `FirecREST` object. This is simply a mini client that, in cooperation with the authorization object, will take care of the necessary requests that need to be made and handle the responses.

```python
import firecrest as f7t
import os


# Get the values from the env or set them directly in your file
CLIENT_ID = os.environ.get("FIRECREST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("FIRECREST_CLIENT_SECRET")
AUTH_TOKEN_URL = os.environ.get("AUTH_TOKEN_URL")
FIRECREST_URL = os.environ.get("FIRECREST_URL")

# Setup the auth object
auth = f7t.ClientCredentialsAuth(
    CLIENT_ID, CLIENT_SECRET, AUTH_TOKEN_URL
)

# Setup the client object
client = f7t.Firecrest(
    firecrest_url=FIRECREST_URL,
    authorization=auth
)

# After this setup, you can go on and try some of the methods of the object


systems = client.all_systems()
print(systems)

## Exercise:

# 1. Get tha different parameters of our deployment
# 2. Get the username of the user
# 3. List all microservices and their status
# 4. List the contents of a directory
# 5. Upload and download "small" files
```
