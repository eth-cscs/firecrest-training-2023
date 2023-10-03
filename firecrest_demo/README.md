# FirecREST demo

## Requirements

- The requests examples will be shown in Python, so previous experience with the language can help you follow more easily.
- In order to follow the `pyfirecrest` part of the demo you will need `Python>=3.7` and to install pyfirecrest in your local env.

```bash
cd firecrest-demo
python -m venv pyfirecrest-demo-env
. pyfirecrest-demo-env/bin/activate
python -m pip install -r requirements.txt
```

Setup environment with credentials and the necessary URLs:

```bash
export FIRECREST_CLIENT_ID=<client-id>
export FIRECREST_CLIENT_SECRET=<client-secret>
export AUTH_TOKEN_URL=https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token
export FIRECREST_URL=https://firecrest.cscs.ch

# Optional for the CLI
export FIRECREST_SYSTEM=daint
```

## Contents

1. [Basic usage of FirecREST through the API directly](part1.md)

2. [Using pyfirecrest to access the API](part2.md)

3. [More advanced use cases of pyfirecrest](part3.md)
