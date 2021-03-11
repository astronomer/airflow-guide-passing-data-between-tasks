from airflow.decorators import dag, task
from datetime import datetime

import requests
import json

url = 'https://covidtracking.com/api/v1/states/'
state = 'co'

default_args = {
    'start_date': datetime(2021, 1, 1)
}

@dag('xcom_taskflow_dag', schedule_interval='@daily', default_args=default_args, catchup=False)
def taskflow():

    @task
    def get_testing_increase(state):
        """
        Gets totalTestResultsIncrease field from Covid API for given state and returns value
        """
        res = requests.get(url+'{0}/current.json'.format(state))
        return{'testing_increase': json.loads(res.text)['totalTestResultsIncrease']}

    @task
    def analyze_testing_increases(testing_increase: int):
        """
        Evaluates testing increase results
        """
        print('Testing increases for {0}:'.format(state), testing_increase)
        #run some analysis here

    analyze_testing_increases(get_testing_increase(state))

dag = taskflow()
