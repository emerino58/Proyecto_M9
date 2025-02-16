import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos
df = pd.read_excel("data/DataSets_Sub16.xlsx")

# 🔹 Tabla de distribución de jugadores por puesto
posiciones = df.pivot_table(index="ID Equipo", columns="Posición", aggfunc="size", fill_value=0).reset_index()

# Layout del módulo
layout = html.Div([
    html.Img(src='/assets/logo.png', style={'width': '100px', 'display': 'block', 'margin': 'auto'}),
    html.H3("Estadísticas de Jugadores", className="text-center"),

    html.Div(id="content-to-export-estadisticas", children=[

        # 📌 Tabla de distribución de jugadores por puesto
        html.H4("Distribución de Jugadores por Posición"),
        dash_table.DataTable(
            data=posiciones.to_dict('records'),
            columns=[{"name": col, "id": col} for col in posiciones.columns],
            style_table={'overflowX': 'auto', 'width': '100%', 'margin': 'auto'},
            style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': '#007BFF', 'color': 'white', 'fontWeight': 'bold'}
        ),

        html.Hr(),

        # 📊 Gráfico de distribución general de jugadores por edad
        html.H4("Distribución de Jugadores por Edad"),
        dcc.Graph(id="bar-age-distribution"),

        html.Hr(),

        # 📌 Comparación de minutos jugados entre dos equipos
        html.H4("Comparación de Minutos Jugados entre Equipos"),
        html.Div([
            dcc.Dropdown(id='team1-dropdown',
                         options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                         value=df["ID Equipo"].unique()[0], style={'width': '45%'}),

            dcc.Dropdown(id='team2-dropdown',
                         options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                         value=df["ID Equipo"].unique()[1], style={'width': '45%'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

        html.Div([
            dcc.Graph(id="team1-line-graph", style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id="team2-line-graph", style={'width': '48%', 'display': 'inline-block'})
        ]),

        html.Hr(),

        # 📌 Selección de jugador y gráfico radial de métricas individuales
        html.H4("Análisis Individual de Jugadores"),
        html.Div([
            dcc.Dropdown(id='team-selection',
                         options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                         placeholder="Selecciona un equipo", style={'width': '45%'}),
            dcc.Dropdown(id='player-selection',
                         placeholder="Selecciona un jugador", style={'width': '45%'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

        dcc.Graph(id="radar-player-stats")
    ]),

    html.Hr(),

    # 🔹 Botones para PDF e Impresión
    html.Div([
        html.Button("📄 Generar PDF", id="btn-pdf-estadisticas", n_clicks=0, className="styled-button"),
        html.Button("🖨️ Imprimir Página", id="btn-print-estadisticas", n_clicks=0, className="styled-button")
    ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px', 'margin-top': '20px'})
])

# 🔹 Callback para el gráfico de distribución de edades
@callback(
    Output("bar-age-distribution", "figure"),
    Input("team1-dropdown", "value")
)
def update_bar_chart(selected_team):
    df_filtered = df[df["ID Equipo"] == selected_team]
    fig = px.histogram(df_filtered, x="Edad (años.meses)", nbins=10,
                       title=f"Distribución de Edades - {selected_team}",
                       labels={"Edad (años.meses)": "Edad", "count": "Cantidad de Jugadores"},
                       color_discrete_sequence=["#007BFF"])
    return fig

# 🔹 Callback para gráficos de minutos jugados entre equipos
@callback(
    [Output("team1-line-graph", "figure"), Output("team2-line-graph", "figure")],
    [Input("team1-dropdown", "value"), Input("team2-dropdown", "value")]
)
def update_minutos_graph(team1, team2):
    df_team1 = df[df["ID Equipo"] == team1]
    df_team2 = df[df["ID Equipo"] == team2]

    fig1 = px.line(df_team1, x="ID Jugador", y="N° Minutos Jugados",
                   title=f"Minutos Jugados - {team1}", markers=True,
                   labels={"ID Jugador": "Jugador", "N° Minutos Jugados": "Minutos"},
                   color_discrete_sequence=["#28a745"])

    fig2 = px.line(df_team2, x="ID Jugador", y="N° Minutos Jugados",
                   title=f"Minutos Jugados - {team2}", markers=True,
                   labels={"ID Jugador": "Jugador", "N° Minutos Jugados": "Minutos"},
                   color_discrete_sequence=["#FF5733"])

    return fig1, fig2
