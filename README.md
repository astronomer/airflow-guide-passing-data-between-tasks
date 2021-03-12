# airflow-guide-passing-data-between-tasks
This repo contains an Astronomer project with multiple example DAGs showing how to pass data between your Airflow tasks. A guide discussing the DAGs and concepts in depth can be found [here](https://www.astronomer.io/guides/airflow-passing-data-between-tasks).

## Tutorial Overview
This tutorial covers two methods for passing data between tasks:

 - Using XCom
 - Using Intermediate Data Storage
 
There are example DAGs for each. The XCom example also includes a DAG using the [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html), which is a new feature released with Airflow 2.0.


## Getting Started
The easiest way to run these example DAGs is to use the Astronomer CLI to get an Airflow instance up and running locally:

 1. [Install the Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)
 2. Clone this repo somewhere locally and navigate to it in your terminal
 3. Initialize an Astronomer project by running `astro dev init`
 4. Start Airflow locally by running `astro dev start`
 5. Navigate to localhost:8080 in your browser and you should see the tutorial DAGs there
