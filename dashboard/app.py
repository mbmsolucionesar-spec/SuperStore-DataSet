import os
import duckdb
import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go

# Conexión a DuckDB
con = duckdb.connect("data/superstore_dashboard.duckdb", read_only=True)

# Ruta base (carpeta donde está app.py)
base_path = os.path.dirname(__file__)

# Conexión a DuckDB
db_path = os.path.join(base_path, "../data/superstore_dashboard.duckdb")
con = duckdb.connect(db_path, read_only=True)
>>>>>>> Miguel
df = con.execute("SELECT * FROM raw_superstore").fetchdf()
con.close()

# Parsear fechas y calcular días de envío
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

<<<<<<< HEAD
# Inicializar app Dash
app = dash.Dash(__name__, title="SuperStore Dashboard")

# Estilo claro para tarjetas KPI
=======
# Agrupar ventas por ciudad/estado/país
ventas_df = df.groupby(["City","State/Province","Country/Region"], as_index=False).agg({
    "Sales":"sum",
    "Profit":"sum",
    "Discount":"mean",
    "Delivery Days":"mean"
})

print("=== DEBUG ventas_df ORIGINAL ===")
print(ventas_df.head(10))

# 🔹 Mapear países
country_map = {
    "United States": "US",
    "Canada": "CA"
}
ventas_df = ventas_df.rename(columns={"State/Province":"State","Country/Region":"Country"})
ventas_df["Country"] = ventas_df["Country"].map(country_map)

# 🔹 Mapear estados (ejemplo parcial, puedes ampliar con todos los estados)
state_map = {
    "California": "CA", "Texas": "TX", "New Mexico": "NM", "Virginia": "VA",
    "Pennsylvania": "PA", "Ohio": "OH", "South Dakota": "SD", "Illinois": "IL",
    "Georgia": "GA", "Kentucky": "KY", "Michigan": "MI", "Minnesota": "MN",
    "Wisconsin": "WI", "Florida": "FL", "Massachusetts": "MA", "New York": "NY",
    "Washington": "WA", "Colorado": "CO", "Oregon": "OR", "Arizona": "AZ"
}
ventas_df["State"] = ventas_df["State"].map(state_map)

print("=== DEBUG ventas_df MAPEADO ===")
print(ventas_df.head(10))

# Cargar coordenadas desde GeoNames
geo_path = os.path.join(base_path, "../data/geonames_cities.txt")
coords_df = pd.read_csv(geo_path, sep="\t", header=None, low_memory=False)

coords_df.columns = [
    "geonameid","name","asciiname","alternatenames","lat","lon",
    "feature_class","feature_code","country_code","cc2","admin1_code",
    "admin2_code","admin3_code","admin4_code","population","elevation",
    "dem","timezone","modification_date"
]

print("=== DEBUG coords_df ===")
print(coords_df.head(10))

# Filtrar por países relevantes
coords_df = coords_df[coords_df["country_code"].isin(["US","CA"])]

# Eliminar duplicados
coords_df = coords_df.drop_duplicates(subset=["name","admin1_code","country_code"])

# Merge
ventas_geo = ventas_df.merge(
    coords_df,
    left_on=["City","State","Country"],
    right_on=["name","admin1_code","country_code"],
    how="left"
)

print("=== DEBUG MERGE RESULT ===")
print("Filas en ventas_geo:", len(ventas_geo))
print(ventas_geo[["City","State","Country","lat","lon"]].head(20))

# Asegurar lat/lon numéricos
ventas_geo["lat"] = pd.to_numeric(ventas_geo["lat"], errors="coerce")
ventas_geo["lon"] = pd.to_numeric(ventas_geo["lon"], errors="coerce")

print("=== DEBUG COORDS ===")
print("Lat min/max:", ventas_geo["lat"].min(), ventas_geo["lat"].max())
print("Lon min/max:", ventas_geo["lon"].min(), ventas_geo["lon"].max())

# Inicializar app Dash
app = dash.Dash(__name__, title="SuperStore Dashboard")

# Estilo tarjetas KPI
>>>>>>> Miguel
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
<<<<<<< HEAD
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
=======
# Layout del dashboard
app.layout = html.Div([
    html.H1("SuperStore Dashboard", style={"textAlign": "center"}),

    # Selector de rango de fechas
    dcc.DatePickerRange(
        id="date-range",
        start_date=df["Order Date"].min(),
        end_date=df["Order Date"].max(),
        display_format="YYYY-MM-DD",
        style={"margin": "20px auto", "display": "block"}
    ),

    # KPIs principales
    html.Div(id="kpi-row", style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "20px"
    }),

    # Gauges estilo progress ring
    html.Div(id="gauge-row", style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "20px"
    }),

    # Gráficas principales
    html.Div([
        dcc.Graph(id="time-series", style={"flex": "1"}),
        dcc.Graph(id="category-sales", style={"flex": "1"})
    ], style={"display": "flex", "marginBottom": "20px"}),

    html.Div([
        dcc.Graph(id="segment-sales", style={"flex": "1"}),
        dcc.Graph(id="region-sales", style={"flex": "1"})
    ], style={"display": "flex", "marginBottom": "20px"}),

    html.Div([
        dcc.Graph(id="discount-profit", style={"flex": "1"}),
        dcc.Graph(id="map-sales", style={"flex": "1"})
    ], style={"display": "flex", "marginBottom": "20px"}),

    # Tabla de últimas órdenes
    html.Div([
        html.H3("Últimas Órdenes"),
        dash_table.DataTable(
            id="orders-table",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "5px"},
            style_header={"backgroundColor": "#f5f5f5", "fontWeight": "bold"}
        )
    ], style={"marginTop": "20px"})
])
>>>>>>> Miguel
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
<<<<<<< HEAD
    if start_date is None or end_date is None:
        filtered = df.copy()
    else:
        mask = (df["Order Date"] >= pd.to_datetime(start_date)) & (df["Order Date"] <= pd.to_datetime(end_date))
        filtered = df.loc[mask]
=======
    print("=== DEBUG CALLBACK ===")
    print("Start date:", start_date, "End date:", end_date)

    # Filtrar por rango de fechas
    if start_date and end_date:
        mask = (df["Order Date"] >= pd.to_datetime(start_date)) & (df["Order Date"] <= pd.to_datetime(end_date))
        filtered = df.loc[mask]
    else:
        filtered = df.copy()

    print("Filas en filtered:", len(filtered))
>>>>>>> Miguel

    # KPIs
    margin = (filtered["Profit"].sum() / filtered["Sales"].sum()) * 100 if filtered["Sales"].sum() > 0 else 0
    avg_delivery = filtered["Delivery Days"].mean()

    kpis = [
<<<<<<< HEAD
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

=======
        html.Div([html.H3(f"${filtered['Sales'].sum():,.0f}"), html.P("Ventas Totales")], style=card_style),
        html.Div([html.H3(f"${filtered['Profit'].sum():,.0f}"), html.P("Ganancia Total")], style=card_style),
        html.Div([html.H3(f"{margin:.2f}%"), html.P("Margen %")], style=card_style),
        html.Div([html.H3(f"{avg_delivery:.1f} días"), html.P("Promedio Envío")], style=card_style),
    ]

    # 🔹 Gauges estilo progress ring
    gauges = [
        html.Div([
            dcc.Graph(
                figure=px.pie(
                    values=[margin, 100 - margin],
                    names=["", ""],
                    hole=0.7,
                    color_discrete_sequence=["#1f77b4", "#e0e0e0"]
                ).update_traces(textinfo="none").update_layout(
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    annotations=[dict(text=f"{margin:.1f}%", x=0.5, y=0.5,
                                      font_size=16, showarrow=False)]
                ),
                style={"height": "160px"}
            ),
            html.P("Margen %", style={"textAlign": "center", "fontWeight": "bold"})
        ], style={"flex": "1", "maxWidth": "200px", "backgroundColor": "#ffffff",
                  "borderRadius": "10px", "padding": "10px",
                  "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"}
        ),

        html.Div([
            dcc.Graph(
                figure=px.pie(
                    values=[avg_delivery, max(avg_delivery*2, 1) - avg_delivery],
                    names=["", ""],
                    hole=0.7,
                    color_discrete_sequence=["#ff7f0e", "#e0e0e0"]
                ).update_traces(textinfo="none").update_layout(
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    annotations=[dict(text=f"{avg_delivery:.1f}", x=0.5, y=0.5,
                                      font_size=16, showarrow=False)]
                ),
                style={"height": "160px"}
            ),
            html.P("Días de Envío", style={"textAlign": "center", "fontWeight": "bold"})
        ], style={"flex": "1", "maxWidth": "200px", "backgroundColor": "#ffffff",
                  "borderRadius": "10px", "padding": "10px",
                  "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"}
        ),

        html.Div([
            dcc.Graph(
                figure=px.pie(
                    values=[filtered['Discount'].mean()*100,
                            100 - filtered['Discount'].mean()*100],
                    names=["", ""],
                    hole=0.7,
                    color_discrete_sequence=["#17becf", "#e0e0e0"]
                ).update_traces(textinfo="none").update_layout(
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    annotations=[dict(text=f"{filtered['Discount'].mean()*100:.1f}%",
                                      x=0.5, y=0.5, font_size=16, showarrow=False)]
                ),
                style={"height": "160px"}
            ),
            html.P("Descuento %", style={"textAlign": "center", "fontWeight": "bold"})
        ], style={"flex": "1", "maxWidth": "200px", "backgroundColor": "#ffffff",
                  "borderRadius": "10px", "padding": "10px",
                  "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"}
        )
    ]

    # Gráficas principales
    time_fig = px.line(filtered.groupby(pd.Grouper(key="Order Date", freq="MS")).agg({"Sales": "sum"}).reset_index(),
                       x="Order Date", y="Sales", title="Ventas en el tiempo")
    cat_fig = px.bar(filtered.groupby("Category", as_index=False).agg({"Sales": "sum"}), x="Category", y="Sales", title="Ventas por categoría")
    seg_fig = px.pie(filtered, names="Segment", values="Sales", title="Ventas por segmento")
    reg_fig = px.bar(filtered.groupby("Region", as_index=False).agg({"Sales": "sum"}), x="Region", y="Sales", title="Ventas por región")
    scatter_fig = px.scatter(filtered, x="Discount", y="Profit", size="Sales", color="Category", title="Descuentos vs Ganancia")

    # Mapa de calor dinámico
    if len(ventas_geo) > 0 and ventas_geo["Sales"].max() > 0:
        ventas_geo["Sales_norm"] = ventas_geo["Sales"] / ventas_geo["Sales"].max()
    else:
        ventas_geo["Sales_norm"] = []

    map_fig = go.Figure(go.Densitymapbox(
        lat=ventas_geo["lat"],
        lon=ventas_geo["lon"],
        z=ventas_geo["Sales_norm"],
        radius=50,
        colorscale="Viridis",
        showscale=True,
        hovertext=ventas_geo["City"] + ", " + ventas_geo["State"]
    ))
    map_fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=ventas_geo["lat"].mean() if len(ventas_geo)>0 else 37,
                        lon=ventas_geo["lon"].mean() if len(ventas_geo)>0 else -95),
            zoom=2
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

>>>>>>> Miguel
    # Tabla últimas órdenes
    last_orders = filtered.sort_values("Order Date", ascending=False).head(10)
    table_data = last_orders[["Order ID", "Product Name", "Order Date", "Sales", "Profit"]].to_dict("records")
    table_columns = [{"name": i, "id": i} for i in ["Order ID", "Product Name", "Order Date", "Sales", "Profit"]]

    return time_fig, cat_fig, seg_fig, reg_fig, scatter_fig, map_fig, kpis, gauges, table_data, table_columns


if __name__ == "__main__":
<<<<<<< HEAD
=======
    print("=== DEBUG APP START ===")
>>>>>>> Miguel
    app.run(debug=True, host="0.0.0.0", port=8050)
