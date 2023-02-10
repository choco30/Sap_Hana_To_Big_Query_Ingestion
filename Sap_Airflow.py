from datetime import timedelta,datetime,date
from airflow import models
from airflow import DAG
from airflow.contrib.operators import gcs_to_bq
from airflow.operators.python_operator import PythonOperator 
from airflow.models import Variable
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from google.cloud import bigquery
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from audit_class import audit_class_bq_ds_auditcntrl
from email_class import Notification_Email

common_config=Variable.get("common_config", deserialize_json=True)
table_list=common_config["table_list"]
BQ_PROJECT=common_config['BQ_PROJECT']
connection_details=common_config["connection_details"]
BQ_landing_dataset=common_config['BQ_landing_dataset']
source_bucket=common_config["source_bucket"]
BQ_stg_dataset=common_config['BQ_stg_dataset']
dataflow_bucket=common_config["dataflow_bucket"]

email_list=Variable.get("email_config", deserialize_json=True)

DEFAULT_ARGS = {
    'depends_on_past': False,
    'start_date': datetime(2022,6,5),
    'catchup': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

dag= DAG(
    'SAP_TABLES_EXTRACT',
    catchup=False,
    default_args=DEFAULT_ARGS,
    schedule_interval='31 18 * * *'
	)
    

def date_extract(**kwargs):
            
    today_date=datetime.now()+timedelta(hours=5,minutes=30)-timedelta(days=1)
    partition_date=str(today_date.strftime("%Y-%m-%d"))
    kwargs['ti'].xcom_push(key="partition_date",value=partition_date)
    
        
DATE_FUNCTION=PythonOperator(
    task_id="DATE_FUNCTION",
    python_callable=date_extract,
    provide_context=True,
    dag=dag
)

def email_func(**kwargs):
    load_date=kwargs['load_date']
    Notification_Email.failure_email(email_list,"KRNOSPBI_DAG_KRONOS_TABLES_EXTRACT",load_date)
        
Email_notification=PythonOperator(
task_id="Email_notification",
python_callable=email_func,
op_kwargs={'load_date':partition_date},
trigger_rule="all_failed",
dag=dag)


    
    
start_dataflow_job=BashOperator(
    task_id=table+"_start_dataflow_job",
    bash_command='''job_date=$(date '+%Y-%m-%d-%H-%M-%S'); python3 /home/airflow/gcs/dags/sql_server_to_gcs.py --runner DataflowRunner --project project_name --region asia-south1 --temp_location gs://bucket-name/temp --network  --max_num_workers 5 --job_name {5}-$job_date --worker_machine_type {7} --service_account_email  service_account-name --setup_file /home/airflow/gcs/dags/setup.py --df_bucket bucket_name '''
    dag=dag)

DATE_FUNCTION>>start_dataflow_job>>Email_notification
