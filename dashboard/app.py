import duckdb
import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go

# Conexión a DuckDB
con = duckdb.connect("data/superstore_dashboard.duckdb", read_only=True)
df = con.execute("SELECT * FROM raw_superstore").fetchdf()
con.close()

# Parsear fechas y calcular días de envío
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Inicializar app Dash
app = dash.Dash(__name__, title="SuperStore Dashboard")

# Estilo claro para tarjetas KPI
card_style = {
    "background": "#ffffff",
    "color": "#333",
    "borderRadius": "12px",
    "padding": "20px",
    "textAlign": "center",
    "flex": "1",
    "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
    "fontFamily": "Helvetica Neue, Arial, sans-serif"
}
app.layout = html.Div(
    style={"padding": "20px", "fontFamily": "Helvetica Neue, Arial, sans-serif",
           "backgroundColor": "#f5f7fa", "color": "#333"},
    children=[
        html.H1("SuperStore Dashboard", style={"textAlign": "center", "color": "#222"}),

        # Tarjeta calendario
        html.Div([
            html.Label("Selecciona rango de fechas:", style={"fontWeight": "bold", "color": "#333"}),
            dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=df["Order Date"].min(),
                max_date_allowed=df["Order Date"].max(),
                start_date=df["Order Date"].min(),
                end_date=df["Order Date"].max(),
                style={"backgroundColor": "#ffffff", "color": "#333", "padding": "8px",
                       "borderRadius": "6px", "border": "1px solid #ccc"}
            )
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjetas KPI
        html.Div(id="kpi-row", style={"display": "flex", "gap": "20px",
                                      "justifyContent": "center", "marginBottom": "30px"}),

        # Tarjetas Gauges
        html.Div(id="gauge-row", style={"display": "flex", "gap": "20px",
                                        "justifyContent": "center", "marginBottom": "30px"}),

        # Tarjeta Ventas en el tiempo
        html.Div([
            html.H3("Ventas en el tiempo", style={"color": "#222"}),
            html.P("Muestra cómo evolucionan las ventas mes a mes."),
            dcc.Graph(id="time-series")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Ventas por categoría
        html.Div([
            html.H3("Ventas por categoría", style={"color": "#222"}),
            html.P("Comparación de ingresos por cada categoría de producto."),
            dcc.Graph(id="category-sales")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Ventas por segmento
        html.Div([
            html.H3("Ventas por segmento", style={"color": "#222"}),
            html.P("Distribución de ventas según tipo de cliente."),
            dcc.Graph(id="segment-sales")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Ventas por región
        html.Div([
            html.H3("Ventas por región", style={"color": "#222"}),
            html.P("Comparación de ventas en distintas regiones."),
            dcc.Graph(id="region-sales")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Descuentos vs Ganancia
        html.Div([
            html.H3("Descuentos vs Ganancia", style={"color": "#222"}),
            html.P("Relación entre descuentos aplicados y ganancias obtenidas."),
            dcc.Graph(id="discount-profit")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Ventas por país
        html.Div([
            html.H3("Ventas por país", style={"color": "#222"}),
            html.P("Mapa geográfico con las ventas por país."),
            dcc.Graph(id="map-sales")
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"}),

        # Tarjeta Últimas Órdenes
        html.Div([
            html.H3("Últimas Órdenes", style={"color": "#222"}),
            html.P("Detalle de las últimas órdenes registradas."),
            dash_table.DataTable(
                id="orders-table",
                style_table={"overflowX": "auto", "backgroundColor": "#ffffff"},
                style_cell={"textAlign": "center", "color": "#333",
                            "backgroundColor": "#ffffff", "border": "1px solid #ddd",
                            "fontFamily": "Helvetica Neue, Arial, sans-serif"}
            )
        ], style={"backgroundColor": "#ffffff", "padding": "20px", "borderRadius": "12px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "marginBottom": "20px"})
    ]
)
@app.callback(
    [Output("time-series", "figure"),
     Output("category-sales", "figure"),
     Output("segment-sales", "figure"),
     Output("region-sales", "figure"),
     Output("discount-profit", "figure"),
     Output("map-sales", "figure"),
     Output("kpi-row", "children"),
     Output("gauge-row", "children"),
     Output("orders-table", "data"),
     Output("orders-table", "columns")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_dashboard(start_date, end_date):
    if start_date is None or end_date is None:
        filtered = df.copy()
    else:
        mask = (df["Order Date"] >= pd.to_datetime(start_date)) & (df["Order Date"] <= pd.to_datetime(end_date))
        filtered = df.loc[mask]

    # KPIs
    margin = (filtered["Profit"].sum() / filtered["Sales"].sum()) * 100 if filtered["Sales"].sum() > 0 else 0
    avg_delivery = filtered["Delivery Days"].mean()

    kpis = [
        html.Div([html.H3(f"${filtered['Sales'].sum():,.0f}", style={"color": "#222"}), html.P("Ventas Totales")], style=card_style),
        html.Div([html.H3(f"${filtered['Profit'].sum():,.0f}", style={"color": "#222"}), html.P("Ganancia Total")], style=card_style),
        html.Div([html.H3(f"{margin:.2f}%", style={"color": "#222"}), html.P("Margen de Ganancia")], style=card_style),
        html.Div([html.H3(f"{avg_delivery:.1f} días", style={"color": "#222"}), html.P("Tiempo Promedio de Envío")], style=card_style),
    ]

    # Gauges
    gauges = [
        dcc.Graph(figure=go.Figure(go.Indicator(
            mode="gauge+number",
            value=margin,
            title={"text": "Margen %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1f77b4"}}
        )).update_layout(paper_bgcolor="#f5f7fa", font={"color": "#333", "family": "Helvetica Neue"})),
        dcc.Graph(figure=go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_delivery,
            title={"text": "Días de Envío"},
            gauge={'axis': {'range': [0, max(avg_delivery*2, 1)]}, 'bar': {'color': "#2ca02c"}}
        )).update_layout(paper_bgcolor="#f5f7fa", font={"color": "#333", "family": "Helvetica Neue"})),
        dcc.Graph(figure=go.Figure(go.Indicator(
            mode="gauge+number",
            value=filtered['Discount'].mean()*100,
            title={"text": "Descuento %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#17becf"}}
        )).update_layout(paper_bgcolor="#f5f7fa", font={"color": "#333", "family": "Helvetica Neue"}))
    ]

    # Serie temporal
    grouped = (filtered.groupby(pd.Grouper(key="Order Date", freq="MS"))
               .agg({"Sales": "sum"}).reset_index())
    time_fig = px.line(grouped, x="Order Date", y="Sales", title="Ventas en el tiempo", template="plotly_white")

    # Categorías
    cat_fig = px.bar(filtered.groupby("Category", as_index=False).agg({"Sales": "sum"}),
                     x="Category", y="Sales", title="Ventas por categoría", template="plotly_white")

    # Segmentos (porcentajes afuera y tipografía moderna)
    seg_fig = px.pie(filtered, names="Segment", values="Sales", title="Ventas por segmento", template="plotly_white")
    seg_fig.update_traces(
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(color="#333", family="Helvetica Neue, Arial, sans-serif", size=14)
    )

    # Regiones
    reg_fig = px.bar(filtered.groupby("Region", as_index=False).agg({"Sales": "sum"}),
                     x="Region", y="Sales", title="Ventas por región", template="plotly_white")

    # Descuento vs Ganancia
    scatter_fig = px.scatter(filtered, x="Discount", y="Profit", size="Sales",
                             color="Category", title="Impacto de descuentos en ganancia", template="plotly_white")

    # Mapa
    map_fig = px.scatter_geo(filtered, locations="Country/Region", locationmode="country names",
                             size="Sales", color="Region", title="Ventas por país", template="plotly_white")

    # Tabla últimas órdenes
    last_orders = filtered.sort_values("Order Date", ascending=False).head(10)
    table_data = last_orders[["Order ID", "Product Name", "Order Date", "Sales", "Profit"]].to_dict("records")
    table_columns = [{"name": i, "id": i} for i in ["Order ID", "Product Name", "Order Date", "Sales", "Profit"]]

    return time_fig, cat_fig, seg_fig, reg_fig, scatter_fig, map_fig, kpis, gauges, table_data, table_columns


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
