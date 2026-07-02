# SuperStore-DataSet
Unidad III - Prueba Final BigData


=========================
INTEGRANTES
=========================

- José Flores
- Bastián Fernández
- Miguel Chura
- Erick Mamani
- Willian Yucra

=========================
MODELO MULTIDIMENSIONAL
=========================

El proyecto implementa un modelo multidimensional basado en un esquema estrella
(Star Schema), siguiendo la metodología de Kimball.

FACT TABLE
----------
fct_sales_summary

Contiene las principales métricas de negocio obtenidas a partir de las órdenes
de venta del Superstore Sales Dataset.

MEDIDAS (Measures)
------------------
- order_count: cantidad de órdenes.
- total_sales: ventas totales.
- total_profit: ganancia total.
- total_quantity: cantidad de productos vendidos.

DIMENSIONES (Dimensions)
------------------------
- Tiempo (order_date): análisis por día, mes y año.
- Región (region): comparación geográfica de las ventas.
- Producto: categoría y subcategoría.
- Cliente: segmentación de clientes.

CONSULTAS OLAP
--------------
El modelo permite realizar consultas como:

- Ventas totales por región y año.
- Ganancias por categoría de producto.
- Evolución mensual de las ventas.
- Cantidad de órdenes por período.

Este esquema estrella fue implementado mediante dbt Core sobre DuckDB y sirve
como base para los dashboards desarrollados en Plotly Dash.
