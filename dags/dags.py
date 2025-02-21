# import datetime library, we will use it for scheduling activities
from datetime import datetime, timedelta

# import DAG
from airflow.models.dag import DAG

# import operations package
from airflow.operators.python import PythonOperator

# import python callable function
from config.t1_extract import extract
from config.t2_transform import transform
from config.t3_load import load

# instantiate the DAG
with DAG (
   # define dag-id
   dag_id = 'my-opcv-projects-dag',

   # set up the default arguments
   # default arguments means we pre-define the default values, then apply it to all operators
   default_args = {
         'depends_on_past': False,
         'email': ['test@airflow.com'],
         'email_on_failure': False,
         'email_on_retry': False,
         'retries': 3, # unit in minites
         'retry_delay': timedelta(minutes = 10)
   },
   schedule = timedelta(days=1),
   start_date = datetime(2025, 2, 20)
) as dag:

   # set the tasks list
   t1 = PythonOperator(
      task_id = 'extract',
      python_callable = extract,
      dag = dag
   )

   t2 = PythonOperator(
      task_id = 'transform',
      python_callable = transform,
      dag = dag
   )

   t3 = PythonOperator(
      task_id = 'load',
      python_callable = load,
      dag = dag
   )

   # set the dependencies sequence
   t1 >> t2 >> t3