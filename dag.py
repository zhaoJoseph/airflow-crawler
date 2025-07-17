from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    dag_id="crawler_kubernetes_dag",
    default_args=args,
    schedule=None, 
    max_active_runs=1,
    catchup=False,
    tags=["crawler", "kubernetes"]
)

# Use your existing image as a Kubernetes pod
crawler_task = KubernetesPodOperator(
    task_id="run_crawler_task",
    name="crawler-pod",
    namespace="default",
    image="crawler-tasks:latest",
    image_pull_policy="IfNotPresent",
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag,
)