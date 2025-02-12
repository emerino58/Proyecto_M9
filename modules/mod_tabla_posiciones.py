import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px

# Cargar datos
df = pd.read_excel("data/tabla_puntajes_futbol.xlsx")
df.columns = df.columns.str.strip()  

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

    html.Hr(style={'border': '1px solid #ddd'}),  # 🔹 Separador visual

    # 📌 Tabla de posiciones
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in df.columns],
        style_table={'overflowX': 'auto', 'margin-bottom': '20px'},
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': '#007BFF', 'color': 'white', 'fontWeight': 'bold'}
    ),

    html.Hr(style={'border': '1px solid #ddd'}),  # 🔹 Separador visual

    # 📌 NUEVO: Título de "Comparativa de Métricas"
    html.H3("Comparativa de Métricas", className="text-center", style={"margin-top": "20px"}),

    # 🔹 Menú desplegable para seleccionar métrica
    html.Div([
        html.Label("Selecciona una métrica para graficar:", style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='metric-selector',
            options=[{"label": original, "value": abreviado} for original, abreviado in column_mapping.items()],
            value="PTS",
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
    ], style={'padding': '10px', 'border': '2px solid #ccc', 'border-radius': '10px', 'background-color': '#f2f2f2'}),

    html.Hr(style={'border': '1px solid #ddd'}),  # 🔹 Separador visual

    # 🔹 Gráfico de barras de la métrica seleccionada
    dcc.Graph(id="bar-chart"),

])

# 🔹 Callback para actualizar el gráfico con colores más intensos
@callback(
    Output("bar-chart", "figure"),
    Input("metric-selector", "value")
)
def update_chart(selected_metric):
    colors = px.colors.qualitative.Bold  # 📌 Colores más intensos y vibrantes
    fig = px.bar(df, x="Equipo", y=selected_metric, title=f"Comparación de {inverse_column_mapping[selected_metric]}",
                 color="Equipo", color_discrete_sequence=colors)

    fig.update_layout(
        xaxis_title="Equipo",
        yaxis_title=inverse_column_mapping[selected_metric],  # 📌 Mostrar nombre original en eje Y
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig
