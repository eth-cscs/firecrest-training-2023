import os
import tempfile
import time

import firecrest as f7t
from airflow.models.baseoperator import BaseOperator
from airflow import AirflowException


# Workaround to run tasks that do http request from the Airflow UI on arm64 macs
# https://github.com/apache/airflow/discussions/24463#discussioncomment-4404542
# Other discussions on the topic:
# https://stackoverflow.com/questions/75980623/why-is-my-airflow-hanging-up-if-i-send-a-http-request-inside-a-task
# from _scproxy import _get_proxy_settings
# _get_proxy_settings()


class FirecRESTBaseOperator(BaseOperator):
    """Base class defining a FireCrest client used in the
    FirecREST Operators
    """
    # get the firecrest credentials from the environment variables

    # setup the keycload authorization class

    # create a firecrest client
    pass


class FirecRESTSubmitOperator(FirecRESTBaseOperator):
    """Airflow Operator to submit a job via FirecREST"""

    def __init__(self, system: str, script: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.system = system
        self.script = script

    def execute(self, context):
        # create a batch a script from `self.script`
        # and submit the job to Piz Daint

        # wait until job finishes

        # raise `AirflowException` if the job's state is not `COMPLETED`

        return  # the dictionary returned by pyfrecrest when submitting the job


class FirecRESTDownloadOperator(FirecRESTBaseOperator):
    """Airflow Operator to fetch the output file of a job
    submitted via FirecREST"""

    def __init__(self,
                 system: str,
                 local_path: str,
                 target_task_id: str,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.system = system
        self.local_path = local_path
        self.target_task_id = target_task_id

    def execute(self, context):
        # get the job dict from a previous submit task
        # with id `self.target_task_id`
        job = context["ti"].xcom_pull(key="return_value",
                                      task_ids=self.target_task_id)

        # download job's output to `self.local_path`


class FirecRESTUploadOperator(FirecRESTBaseOperator):
    """Airflow Operator to updload the input file for a job
    to be submitted via FirecREST later in the DAG"""

    def __init__(self,
                 system: str,
                 source_path: str,
                 target_path: str,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.system = system
        self.source_path = source_path
        self.target_path = target_path

    def execute(self, context):
        # upload the local file `self.source_path` piz daint
        # as `self.target_path`
        pass
