## Using pyfirecrest to access the API

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


## The storage workflow

For larger files the user cannot directly upload/download a file to/from FirecREST.
A staging area will be used and the process will require multiple requests from the user.

More about the [external download](external_download.pdf) and [external upload](external_upload.pdf) workflows in the links.

## External upload with pyfirecrest

the requested file will first have to be moved to the staging area. This could take a long time in case of a large file. When this process finishes, FirecREST will have created a dedicated space for this file and the user can download the file locally as many times as he wants. You can follow this process with the status codes of the task:

| Status | Description |
| ------ | ----------- |
| 116    | Started upload from filesystem to Object Storage |
| 117    | Upload from filesystem to Object Storage has finished successfully |
| 118    | Upload from filesystem to Object Storage has finished with errors |

In code it would look like this:

```python
# This call will only start the transfer of the file to the staging area
down_obj = client.external_download("daint", "</remote/full/path/to/the/file>")

print(type(down_obj))

# You can follow the progress of the transfer through the status property
print(down_obj.status)

# As soon as down_obj.status is 117 we can proceed with the download to a local file
down_obj.finish_download("my_local_file")

# You can get directly the link in the staging area and finish the download in your prefered way.
print(down_obj.object_storage_link)

# You can download the file as many times as we want from the staging area.
# After you finish, you should invalidate the link.
down_obj.invalidate_object_storage_link()
```

You can check all the details of the `ExternalDownload` object that will be created in the [docs](https://pyfirecrest.readthedocs.io/en/stable/reference_basic.html#the-externaldownload-class)

**[Optional]** You can also try to do this in the CLI of pyfirecrest.

## External download with pyfirecrest

The case of external upload is very similar.
To upload a file you would have to ask for the link in the staging area and upload the file there.
**Even after uploading the file there, it will take some time for the file to appear in the filesystem.**
You can follow the status of the task with the status method and when the file has been successfully uploaded the status of the task will be 114.

| Status | Description |
| ------ | ----------- |
| 110    | Waiting for Form URL from Object Storage to be retrieved |
| 111    | Form URL from Object Storage received |
| 112    | Object Storage confirms that upload to Object Storage has finished |
| 113    | Download from Object Storage to server has started |
| 114    | Download from Object Storage to server has finished |
| 115    | Download from Object Storage error |

```python
# This call will only create the link to Object Storage
up_obj = client.external_upload("daint", "/path/to/local/file", "/remote/path/to/filesystem")

# As soon as up_obj.status is 111 we can proceed with the upload of local file to the staging area
up_obj.finish_upload()

# You can follow the progress of the transfer through the status property
print(up_obj.status)
```

You can get the necessary components for the upload from the `object_storage_data` property.
You can get the link, as well as all the necessary arguments for the request to Object Storage and the full command you could perform manually from the terminal.

**[Optional]** You can also try to do this in the CLI of pyfirecrest.
