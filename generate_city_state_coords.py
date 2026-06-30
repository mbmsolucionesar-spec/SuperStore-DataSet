import duckdb
import pandas as pd
from geopy.geocoders import Nominatim
import time

# 1. Conexión a DuckDB
con = duckdb.connect("data/superstore_dashboard.duckdb", read_only=True)

# 2. Obtener lista única de ciudades, estados y países
df = con.execute('SELECT DISTINCT City, "State/Province" AS State, "Country/Region" AS Country FROM raw_superstore').fetchdf()
con.close()

# 3. Inicializar geolocalizador
geolocator = Nominatim(user_agent="superstore-mapper")

coords = []
for _, row in df.iterrows():
    query = f"{row['City']}, {row['State']}, {row['Country']}"
    try:
        location = geolocator.geocode(query)
        if location:
            coords.append({
                "City": row["City"],
                "State": row["State"],
                "Country": row["Country"],
                "Lat": location.latitude,
                "Lon": location.longitude
            })
        time.sleep(1)  # pausa para no saturar el servicio
    except Exception as e:
        print(f"Error con {query}: {e}")

# 4. Crear DataFrame y guardar CSV
coords_df = pd.DataFrame(coords)
coords_df.to_csv("city_state_coordinates.csv", index=False)

print("Archivo city_state_coordinates.csv generado con éxito")
print(coords_df.head())
