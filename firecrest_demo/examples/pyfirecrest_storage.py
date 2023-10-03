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

# This call will only start the transfer of the file to the staging area
down_obj = client.external_download("daint", "/scratch/snx3000/eirinik/a_file.txt")

print(type(down_obj))

# You can follow the progress of the transfer through the status property
print(down_obj.status)

# As soon as down_obj.status is 117 we can proceed with the download to a local file
down_obj.finish_download("my_local_file")

print(down_obj.status)

# You can get directly the link in the staging area and finish the download in your prefered way.
print("Direct link:", down_obj.object_storage_link)

# You can download the file as many times as we want from the staging area.
# After you finish, you should invalidate the link.
down_obj.invalidate_object_storage_link()

