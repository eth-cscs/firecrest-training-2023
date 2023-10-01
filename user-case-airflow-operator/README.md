# Airflow operator with FirecREST

[Apache Airflow](https://airflow.apache.org) is an open-source workflow management platform. Airflow uses directed acyclic graphs (DAGs) to manage the workflows. Tasks and dependencies are defined in Python and then Airflow takes care of the scheduling and execution. DAGs can be run either on a schedule or based on external event triggers.

For this tutorial we have defined an Airflow DAG that combines small tasks which can run localy and compute intensive tasks that must run on a supercomputer. We will run Airflow on our personal computers and our goal will be to add the support for executing the DAG's intensive tasks on Piz Daint via [FirecREST](https://firecrest.readthedocs.io). For that we are going to write [custom Airflow operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html) that will use FirecREST to access Piz Daint.

The idea behind this it's very simple.
Operators are defined as units of work for Airflow to complete and custom ones can be written by extending Airflow's [`BaseOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html#airflow.models.baseoperator.BaseOperatorMeta) class.
We just need to define the arguments specific to our logic and the `execute` function that will use [PyFirecrest](https://pyfirecrest.readthedocs.io/en/stable/) to submit the jobs as well as transfering files to and from the HPC facilities.
Our operator will look something like this

```python
class FirecRESTCustomOperator(BaseOperator):
    def init(self, arg1, arg2, **kwargs):
        super().__init__(**kwargs)
        self.arg1 = arg1
        self.arg2 = arg2

    def execute(self, context):
        # pyfirecrest suff
```


## Setting up the credentials for PyFirecrest

We can export as environment variables the credentials that FirecREST will use and read them within our operators.

```bash
export FIRECREST_CLIENT_ID=<client-id>
export FIRECREST_CLIENT_SECRET=<client-secret>
export AUTH_TOKEN_URL=https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token
export FIRECREST_URL=https://firecrest.cscs.ch
```

## Installing Apache Airflow

We recommend installing Apache Airflow as well as PizFirecREST on a virtual environment in your personal computer.
You just need to do the following:
```bash
python -m venv fc-training-env
. fc-training-env/bin/activate
pip install apache-airflow pyfirecrest
```

### Launching Airflow

Before launching Airflow, we need to initialize it's database
```bash
export AIRFLOW_HOME=$HOME/airflow-fc-training
airflow db init
```
Airflow will come with many examples that show up in the dashboard. You can set `load_examples = False` in your `airflow-fc-etraining/airflow.cfg` configuration file to start Airflow with a clean dashboard.

Let's launch Airflow in standalone mode (only suitable for testing)
```bash
airflow standalone
```

When Airflow starts, it will print this lines by the end of the initialization message
```
standalone | Airflow is ready
standalone | Login with username: admin  password: HUDEIDRBRVGvhgjde
standalone | Airflow Standalone is for development purposes only. Do not use this in production!
```
where you can find the username and password to login in the dashboard at http://127.0.0.1:8080.

## Hands On

For this example we want to propose you the following:
Let's say that we have a simulation that's finding the geometry of new crystal structures and anytime one geometry is produced we would like to trigger a Quantum Espresso calculation to computes certain properties of it. We have defined an Airflow DAG that will the do the job in the file [airflow-dag.py](airflow-dag.py). It's tasks are:
 - Detect that a new structure has been produced
 - Upload the sturcture and it's pseudopotential to Piz Daint
 - Submit a job to Piz Daint to compute the properties
 - Download the output of the calculation
 - Log the relevant values from the output on a table
 - Delete the file with the structurel

We have set this processe to be scheduled daily.

To see on Airflow's dashboard we must place the file in `$AIRFLOW_HOME/dags`:
```bash
mkdir $AIRFLOW_HOME/dags
cp airflow-dag.py $AIRFLOW_HOME/dags
```
It will show up with the name `firecrest_example` after a some seconds / refreshing the page.

You can click on it and browse the differen tabs such as *Graph*.
You can trigger he DAG it by clicking on the *Play* button at the righ hand side of the dashboard next to teh tabs.

The file [firecrest_airflow_operators.py](firecrest_airflow_operators.py) has already part of the implementation of the operators writen.
As it is now, the DAG can be executed but it doesn't do any work since all the FirecREST logic is missing.
We invite you to go through the comments in the file and add the missing parts.

For Airflow to see our module, the file must be in the `$PYTHONPATH`. You can install it with
```bash
cd use-case-airflow-operator
pip install .
```
