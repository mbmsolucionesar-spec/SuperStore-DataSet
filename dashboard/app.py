import duckdb
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Conexión a DuckDB
con = duckdb.connect("../data/superstore_dashboard.duckdb", read_only=True)

# Cargar tabla sales_summary
df = con.execute("SELECT * FROM analytics.sales_summary").fetchdf()

# Inicializar app Dash
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("SuperStore Dashboard"),
    dcc.Dropdown(
        id="region-filter",
        options=[{"label": r, "value": r} for r in df["region"].unique()],
        value=df["region"].unique()[0]
    ),
    dcc.Graph(id="sales-graph")
])

# Callback para actualizar gráfico
@app.callback(
    dash.Output("sales-graph", "figure"),
    dash.Input("region-filter", "value")
)
def update_graph(region):
    filtered = df[df["region"] == region]
    fig = px.bar(filtered, x="category", y="total_sales",
                 title=f"Ventas por categoría en {region}")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
