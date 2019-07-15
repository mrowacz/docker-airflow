from __future__ import print_function
from airflow.operators import LivySparkOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.models import DAG
from datetime import datetime, timedelta
import os

"""
Pre-run Steps:

1. Open the Airflow WebServer
2. Navigate to Admin -> Connections
3. Add a new connection
    1. Set the Conn Id as "livy_http_conn"
    2. Set the Conn Type as "http"
    3. Set the host
    4. Set the port (default for livy is 8998)
    5. Save
"""

DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")

HTTP_CONN_ID = "livy_http_conn"
SESSION_TYPE = "pyspark"
SPARK_SCRIPT = """
print "sc: " + str(sc)

rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd_filtered = rdd.filter(lambda entry: entry > 3)
print(rdd_filtered.collect())
"""

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    }

dag = DAG(
    DAG_ID,
    default_args=default_args,
    schedule_interval=None,
    start_date=(datetime.now() - timedelta(minutes=1)),
    concurrency=4,
)

start_task = DummyOperator(
    task_id='start',
    dag=dag,
)
end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

tasks = []
for i in range(10):
    dummy = LivySparkOperator(
        task_id=f'livy-{SESSION_TYPE}-{i}',
        spark_script=SPARK_SCRIPT,
        http_conn_id=HTTP_CONN_ID,
        session_kind=SESSION_TYPE,
        dag=dag,
    )
    dummy.set_upstream(start_task)
    dummy.set_downstream(end_task)
    tasks.append(dummy)
