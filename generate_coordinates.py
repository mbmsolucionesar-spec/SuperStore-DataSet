import duckdb
import pandas as pd
from geopy.geocoders import Nominatim
import time

# 1. Conexión a DuckDB en data/raw
con = duckdb.connect("data/superstore_dashboard.duckdb", read_only=True)

# 2. Obtener lista única de países desde la tabla raw_superstore
df = con.execute('SELECT DISTINCT "Country/Region" AS Country FROM raw_superstore').fetchdf()
con.close()

# 3. Inicializar geolocalizador
geolocator = Nominatim(user_agent="superstore-mapper")

coords = []
for country in df["Country"]:
    try:
        location = geolocator.geocode(country)
        if location:
            coords.append({
                "Country": country,
                "Lat": location.latitude,
                "Lon": location.longitude
            })
        time.sleep(1)  # pausa para no saturar el servicio
    except Exception as e:
        print(f"Error con {country}: {e}")

# 4. Crear DataFrame y guardar CSV en raíz
coords_df = pd.DataFrame(coords)
coords_df.to_csv("countries_coordinates.csv", index=False)

print("Archivo countries_coordinates.csv generado con éxito")
print(coords_df.head())
