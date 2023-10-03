# Interracting with the scheduler and data transfers

FirecREST offers three basic functionalities of the scheduler:
1. submit jobs on behalf of a user,
1. poll for the jobs of the user and
1. cancel jobs.

## The `compute` workflow

See the workflow [here](compute_sbatch.pdf).

On a job scheduler like Slurm, every job has a unique `job ID`, which is created when a job is submitted and can be used to track the state of the job. With calls like `squeue` and `sacct` the user can see the state of the job (RUNNING, COMPLETED, etc.) as well as get information for the job.
Similarly, for every task FirecREST will assign a `task ID` with which the user can track the state of the request and get information about it.

## Implement the job submission with pyfirecrest

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

client.submit("daint", "script.sh")
```

## Implement the job submission with direct calls to the api:

```python
localPath = 'script.sh'

response = requests.post(
    url=f'{FIRECREST_IP}/compute/jobs/upload',
    headers={'Authorization': f'Bearer {TOKEN}',
             'X-Machine-Name': "daint"},
    files={'file': open(localPath, 'rb')}
)

print(json.dumps(response.json(), indent=4))

taskid = response.json()['task_id']

while True:
    response = requests.get(
        url=f'{FIRECREST_IP}/tasks/{taskid}',
        headers={'Authorization': f'Bearer {TOKEN}'}
    )

    print(json.dumps(response.json(), indent=4))

    if response.json()["status"] < 200:
        continue

    break
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
