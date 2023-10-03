# FirecREST demo

## Requirements

- The requests examples will be provided in Python, but you can use `curl` or any other library/programming language you like.
- In order to follow the `pyfirecrest` part of the demo you will need `Python>=3.7` and to install pyfirecrest in your local env.

```bash
python -m venv pyfirecrest-demo-env
. pyfirecrest-demo-env/bin/activate
python -m pip install pyfirecrest
```

Setup environment with credentials and the necessary URLs:

```bash
export FIRECREST_CLIENT_ID=<client-id>
export FIRECREST_CLIENT_SECRET=<client-secret>
export AUTH_TOKEN_URL=https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token
export FIRECREST_URL=https://firecrest.cscs.ch
```

## Contents

1. [Basic usage of FirecREST](part1.md)

2. [Interacting with the scheduler and data transfers](part2.md)

3. [More advanced use cases of pyfirecrest](part3.md)
