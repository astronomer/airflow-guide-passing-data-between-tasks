from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta

from io import StringIO
import os
import pandas as pd
import requests

s3_conn_id = 's3-conn'
bucket = 'astro-workshop-bucket'
state = 'wa'
date = '{{ yesterday_ds_nodash }}'

def upload_to_s3(state, date):
    '''Grabs data from Covid endpoint and saves to flat file on S3
    '''
    # Connect to S3
    s3_hook = S3Hook(aws_conn_id=s3_conn_id)

    # Get data from API
    url = 'https://covidtracking.com/api/v1/states/'
    res = requests.get(url+'{0}/{1}.csv'.format(state, date))

    # Save data to CSV on S3
    s3_hook.load_string(res.text, '{0}_{1}.csv'.format(state, date), bucket_name=bucket, replace=True)


def process_data(state, date):
    '''Reads data from S3, processes, and saves to new S3 file
    '''
    # Connect to S3
    s3_hook = S3Hook(aws_conn_id=s3_conn_id)

    # Read data
    data = StringIO(s3_hook.read_key(key='{0}_{1}.csv'.format(state, date), bucket_name=bucket))
    df = pd.read_csv(data, sep=',')

    # Process data
    processed_data = df[['date', 'state', 'positive', 'negative']]

    # Save processed data to CSV on S3
    s3_hook.load_string(processed_data.to_string(), '{0}_{1}_processed.csv'.format(state, date), bucket_name=bucket, replace=True)


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


with DAG('intermediary_data_storage_dag',
         start_date=datetime(2021, 1, 1),
         max_active_runs=1,
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False
         ) as dag:
    
    generate_file = PythonOperator(
        task_id='generate_file_{0}'.format(state),
        python_callable=upload_to_s3,
        op_kwargs={'state': state, 'date': date}
    )

    process_data = PythonOperator(
        task_id='process_data_{0}'.format(state),
        python_callable=process_data,
        op_kwargs={'state': state, 'date': date}
    )

    generate_file >> process_data
    