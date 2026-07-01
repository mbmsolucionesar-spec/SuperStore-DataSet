import polars as pl
import duckdb

def ingest():
    # Leer CSV con Polars
    df = pl.read_csv("data/superstore.csv")

    # Conectar a DuckDB
    con = duckdb.connect("data/superstore.duckdb")

    # Guardar tabla
    con.execute("CREATE OR REPLACE TABLE raw_superstore AS SELECT * FROM df")
    con.close()

if __name__ == "__main__":
    ingest()
