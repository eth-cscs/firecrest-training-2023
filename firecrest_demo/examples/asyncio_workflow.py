import asyncio
import firecrest
import logging
import os


# Setup variables for the client
client_id = os.environ.get("FIRECREST_CLIENT_ID")
client_secret = os.environ.get("FIRECREST_CLIENT_SECRET")
token_uri = os.environ.get("AUTH_TOKEN_URL")
firecrest_url = os.environ.get("FIRECREST_URL")

machine = "daint"
local_script_path = "script.sh"

# This is simply setup for logging, you can ignore it
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)



async def workflow(client, i):
    logger.info(f"{i}: Starting workflow")
    job = await client.submit(machine, local_script_path)
    logger.info(f"{i}: Submitted job with jobid: {job['jobid']}")
    while True:
        poll_res = await client.poll_active(machine, [job["jobid"]])
        if len(poll_res) < 1:
            logger.info(f"{i}: Job {job['jobid']} is no longer active")
            break

        logger.info(f"{i}: Job {job['jobid']} status: {poll_res[0]['state']}")
        await asyncio.sleep(30)

    output = await client.view(machine, job["job_file_out"])
    logger.info(f"{i}: job output: {output}")


async def main():
    auth = firecrest.ClientCredentialsAuth(client_id, client_secret, token_uri)
    client = firecrest.AsyncFirecrest(firecrest_url, authorization=auth)

    # Set up the desired polling rate for each microservice. The float number
    # represents the number of seconds between consecutive requests in each
    # microservice.
    client.time_between_calls = {
        "compute": 5,
        "reservations": 5,
        "status": 5,
        "storage": 5,
        "tasks": 5,
        "utilities": 5,
    }

    workflows = [workflow(client, i) for i in range(5)]
    await asyncio.gather(*workflows)


asyncio.run(main())
