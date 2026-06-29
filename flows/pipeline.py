from prefect import flow, task
import subprocess
from ingest import ingest_superstore

@task
def run_ingest():
    df = ingest_superstore()
    return df.shape

@task
def run_dbt():
    # Ejecuta dbt dentro del contenedor
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError("Error en dbt run")
    return "dbt run completado"

@flow(name="superstore_pipeline")
def pipeline():
    # Paso 1: ingesta con Polars
    rows, cols = run_ingest()
    print(f"Ingesta completada: {rows} filas, {cols} columnas")

    # Paso 2: transformación con dbt
    dbt_status = run_dbt()
    print(dbt_status)

if __name__ == "__main__":
    pipeline()

