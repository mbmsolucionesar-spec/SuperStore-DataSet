# SuperStore-DataSet
Unidad III - Prueba Final BigData

-----------
Integrantes
----------

- José Flores
- Bastián Fernández
- Miguel Chura
- Erick Mamani
- Willian Yucra

-----------------------
Modelo Multidimensional
-----------------------

El proyecto implementa un modelo multidimensional basado en un esquema estrella
(Star Schema), siguiendo la metodología de Kimball.

Fact Table
----------
fct_sales_summary

Contiene las principales métricas de negocio obtenidas a partir de las órdenes
de venta del Superstore Sales Dataset.

Medidas (Measures)
------------------
- order_count: cantidad de órdenes.
- total_sales: ventas totales.
- total_profit: ganancia total.
- total_quantity: cantidad de productos vendidos.

Dimensiones (Dimensions)
------------------------
- Tiempo (order_date): análisis por día, mes y año.
- Región (region): comparación geográfica de las ventas.
- Producto: categoría y subcategoría.
- Cliente: segmentación de clientes.

Consultas OLAP
--------------
El modelo permite realizar consultas como:

- Ventas totales por región y año.
- Ganancias por categoría de producto.
- Evolución mensual de las ventas.
- Cantidad de órdenes por período.

Este esquema estrella fue implementado mediante dbt Core sobre DuckDB y sirve
como base para los dashboards desarrollados en Plotly Dash.

----------------------------------------------------
SuperStore-DataSet - Guía de instalación y ejecución
----------------------------------------------------

1. Clonar el repositorio
   git clone git@github.com:mbmsolucionesar-spec/SuperStore-DataSet.git
   cd SuperStore-DataSet

2. Crear entorno virtual
   python3 -m venv .venv

3. Activar entorno virtual
   source .venv/bin/activate   (Linux/Mac)
   .\.venv\Scripts\activate    (Windows PowerShell)

4. Instalar dependencias
   pip install -r requirements.txt

5. Configuración de base de datos DuckDB
   - El archivo de datos se encuentra en data/superstore_dashboard.duckdb
   - Los scripts de ingesta y coordenadas están en la carpeta flows/

6. Levantar el dashboard
   python3 dashboard/app.py

7. Acceder al dashboard
   Abrir el navegador en http://127.0.0.1:8050/

8. Uso de Prefect
   - Los pipelines ETL se definen en flows/
   - Para ejecutar un flow: prefect deployment run <nombre_del_flow>
   - El servidor de Prefect se levanta con docker-compose up

9. Actualizar dependencias
   pip freeze > requirements.txt

10. Comandos útiles de Git
   - Ver estado: git status
   - Subir cambios: git add .
                     git commit -m "mensaje"
                     git push origin main
   - Traer cambios remotos: git pull origin main --rebase
