import requests
import os
import json
import jwt


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
print(f"\nHeaders:\n{json.dumps(dict(response.headers), indent=4)}")
# Masking the actual token from the output
json_result = response.json()
json_result["access_token"] = "eyXXX"
print(f"\nJSON:\n{json.dumps(json_result, indent=4)}\n")
TOKEN = response.json()["access_token"]

# Uncomment the code below to decode the token

# decoded = jwt.decode(
#     response.json()["access_token"],
#     options={"verify_signature": False},
# )
# print("\nDecoded token:\n", json.dumps(decoded, indent=4))


# Checking the available systems in our deployment

FIRECREST_URL = os.environ.get("FIRECREST_URL")

response = requests.get(
    url=f'{FIRECREST_URL}/status/systems',
    headers={'Authorization': f'Bearer {TOKEN}'}
)

print(json.dumps(response.json(), indent=4))
