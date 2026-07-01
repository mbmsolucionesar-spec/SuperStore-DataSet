import pandas as pd
import duckdb

# Columnas del archivo GeoNames cities5000
cols = [
    "geonameid","name","asciiname","alternatenames","lat","lon","feature_class","feature_code",
    "country_code","cc2","admin1_code","admin2_code","admin3_code","admin4_code","population",
    "elevation","dem","timezone","modification_date"
]

# 1. Leer archivo GeoNames
geo_df = pd.read_csv("data/geonames_cities.txt", sep="\t", names=cols, dtype=str)

# 2. Conexión a DuckDB y obtener ciudades/estados del SuperStore
con = duckdb.connect("data/superstore_dashboard.duckdb", read_only=True)
store_df = con.execute(
    'SELECT DISTINCT City, "State/Province" AS State, "Country/Region" AS Country FROM raw_superstore'
).fetchdf()
con.close()

# 3. Normalizar nombres para hacer merge
store_df["City_norm"] = store_df["City"].str.lower().str.strip()
geo_df["City_norm"] = geo_df["name"].str.lower().str.strip()

# 4. Hacer merge por ciudad
merged = store_df.merge(
    geo_df[["City_norm","lat","lon","country_code","admin1_code"]],
    on="City_norm", how="left"
)

# 5. Guardar coordenadas finales
coords_df = merged[["City","State","Country","lat","lon"]].dropna()
coords_df.rename(columns={"lat":"Lat","lon":"Lon"}, inplace=True)
coords_df.to_csv("city_state_coordinates.csv", index=False)

print(" Archivo city_state_coordinates.csv generado con éxito")
print(coords_df.head())
