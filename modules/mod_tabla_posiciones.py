import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px

# Cargar datos
df = pd.read_excel("data/tabla_puntajes_futbol.xlsx")
df.columns = df.columns.str.strip()  # Limpiar espacios en los nombres de columnas

# 🔹 Mapeo de nombres originales y abreviados
column_mapping = {
    "Partidos Ganados": "PG",
    "Partidos Empatados": "PE",
    "Partidos Perdidos": "PP",
    "Goles a Favor": "GF",
    "Goles en Contra": "GC",
    "Diferencia de Goles": "DG",
    "Puntos": "PTS",
    "% Rendimiento": "%REN"
}
inverse_column_mapping = {v: k for k, v in column_mapping.items()}
df = df.rename(columns=column_mapping)
df = df.sort_values("PTS", ascending=False)

# 🔹 Layout de la página
layout = html.Div([
    html.Img(src='/assets/logo.png', style={'width': '100px', 'display': 'block', 'margin': 'auto'}),
    html.H3("Tabla de Posiciones Sub-16 ZC", className="text-center"),

    html.Div(id="content-to-export-posiciones", children=[
        # 📌 Tabla de posiciones
        html.H4("Clasificación General"),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'auto', 'margin-bottom': '20px'},
            style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': '#007BFF', 'color': 'white', 'fontWeight': 'bold'}
        ),

        html.Hr(),

        # 📌 Gráfico de métricas seleccionadas
        html.H4("Comparativa de Métricas"),
        dcc.Dropdown(id='metric-selector',
                     options=[{"label": original, "value": abreviado} for original, abreviado in column_mapping.items()],
                     value="PTS", style={'width': '50%', 'margin-bottom': '20px'}),
        dcc.Graph(id="bar-chart")
    ]),

    html.Hr(),

    # 🔹 Botones para PDF e Impresión
    html.Div([
        html.Button("📄 Generar PDF", id="btn-pdf-posiciones", n_clicks=0, className="styled-button"),
        html.Button("🖨️ Imprimir Página", id="btn-print-posiciones", n_clicks=0, className="styled-button")
    ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px', 'margin-top': '20px'})
])

# 🔹 Callback para actualizar el gráfico de métricas
@callback(
    Output("bar-chart", "figure"),
    Input("metric-selector", "value")
)
def update_bar_chart(selected_metric):
    metric_name = inverse_column_mapping[selected_metric]  # Obtener el nombre original
    fig = px.bar(df, x="Equipo", y=selected_metric, title=f"Comparación de {metric_name} entre Equipos")
    return fig

