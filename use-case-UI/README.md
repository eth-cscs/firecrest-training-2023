# Use Case: UI

## Goal of the exercise

Create a Web UI application on Python (Flask) to interface HCP services at CSCS
In the repository, the file `src/client.py` provide a number of functions to be completed with pyFirecREST or FirecREST API.
This functions are the ones that has the `*_with_f7t` prefix.

Follow the Configuration guide to adapt your client credentials to the app.

## Prerequisites

- Training account (from CSCS)
- Create FirecREST API Keys using [OIDC Dashboard](https://oidc-dashboard-prod.cscs.ch)

- Docker installed
- Knowledge of Python


## Configuration

1. Copy the configuration file (`src/config.py.orig`) and rename it as `src/config.py`

```
$ cd src
$ cp config.py.orig config.py
```

2. Replace the follwing values with the specifics for this training 

```
...
class DevConfig(Config)
    OIDC_CLIENT_ID = "<CLIENT_ID>" # <--- obtained from oidc-dashboard (handle with care, it is a credential!)
    OIDC_CLIENT_SECRET = "<CLIENT_SECRET>" # <--- obtained from oidc-dashboard (it is a credential!)
    USER_GROUP="class08"
    OIDC_AUTH_BASE_URL = "https://auth.cscs.ch"
    OIDC_AUTH_REALM = "firecrest-clients"    
    FIRECREST_URL="https://firecrest.cscs.ch"
    SYSTEM_NAME="daint"
    
```

- For the configuration variables `SBATCH_TEMPLATE` and `POST_TEMPLATE`:
  - for debugging purposes, use the values `"demo.sh.tmpl"` and `"demo_post.sh.tmpl"`, respectively
  - for final test purposes, use the values `"cylinder.sh.tmpl"` and `"post_proc.sh.tmpl"`, respectively


## Build and run

```
make build
make run
```

- You can check the logs in `log/client.log`
```
tail -f log/client.log
```

Open a browser, and enter [http://localhost:9090](http://localhost:9090)

