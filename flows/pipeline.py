from prefect import flow, task
import subprocess

@task
def run_ingest():
    subprocess.run(["python", "flows/ingest.py"], check=True)

@task
def run_dbt():
    subprocess.run(["dbt", "run", "--project-dir", "dbt_project"], check=True)

@task
def run_dashboard():
    subprocess.run(["python", "dashboard/app.py"], check=True)

@flow
def pipeline():
    run_ingest()
    run_dbt()
    run_dashboard()

if __name__ == "__main__":
    pipeline()

