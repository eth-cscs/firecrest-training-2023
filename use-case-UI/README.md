# Use Case: UI

## Prerequisites

- Training account (from CSCS)
- Create FirecREST API Keys using [OIDC Dashboard](https://oidc-dashboard.cscs.ch)

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
    OIDC_AUTH_BASE_URL = "https://auth.cscs.ch"
    OIDC_AUTH_REALM = "firecrest-clients"    
    FIRECREST_URL="https://firecrest.cscs.ch"
    SYSTEM_NAME="daint"
    USER_GROUP="" # <--- obtained from trainers
```


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

