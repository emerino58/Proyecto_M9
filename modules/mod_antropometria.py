import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback
import plotly.express as px

# Cargar datos antropométricos
df = pd.read_excel("data/Data_Antropometrica.xlsx")

# Layout del módulo
layout = html.Div([
    html.Img(src='/assets/logo.png', style={'width': '100px', 'display': 'block', 'margin': 'auto'}),
    html.H3("Datos Antropométricos de Jugadores", className="text-center"),

    html.H4("Comparación del Índice de Masa Corporal (IMC) entre Equipos"),
    html.Div([
        html.Label("Selecciona Equipo 1:", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='team1-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                     value=df["ID Equipo"].unique()[0], style={'width': '45%'}),  

        html.Label("Selecciona Equipo 2:", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='team2-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                     value=df["ID Equipo"].unique()[1], style={'width': '45%'}),  
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

    html.Div([
        dcc.Graph(id="team1-imc-graph", style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id="team2-imc-graph", style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Hr(style={'border': '1px solid #ddd'}),

    html.H4("Comparación de Variables Antropométricas entre Equipos"),
    html.Label("Selecciona una métrica:", style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{"label": col, "value": col} for col in ["IMC (kg/m2)", "Masa Adiposa (kg)", "Masa Muscular (kg)", 
                                                          "Masa Residual (kg)", "Masa Ósea (kg)", "Masa Piel (kg)", 
                                                          "Índice Músculo/Óseo (IMO)"]],
        value="IMC (kg/m2)",
        style={'width': '60%'}
    ),

    dcc.Graph(id="boxplot-metric"),
    
    html.Hr(style={'border': '1px solid #ddd'}),

    html.H4("Datos Antropométricos de Jugadores por Equipo"),
    html.Label("Selecciona un equipo:", style={'font-weight': 'bold'}),
    dcc.Dropdown(id='table-team-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                 value=df["ID Equipo"].unique()[0], style={'width': '60%'}),

    html.Div(id="player-table-container")  # 📌 Aquí se desplegará la tabla con los datos antropométricos
])

# 🔹 Callback para actualizar los gráficos de comparación de IMC
@callback(
    [Output("team1-imc-graph", "figure"), Output("team2-imc-graph", "figure")],
    [Input("team1-dropdown", "value"), Input("team2-dropdown", "value")]
)
def update_imc_graph(team1, team2):
    df_team1 = df[df["ID Equipo"] == team1]
    df_team2 = df[df["ID Equipo"] == team2]

    fig1 = px.line(df_team1, x="ID Jugador", y="IMC (kg/m2)", title=f"IMC - {team1}")
    fig2 = px.line(df_team2, x="ID Jugador", y="IMC (kg/m2)", title=f"IMC - {team2}")

    return fig1, fig2

# 🔹 Callback para generar el Boxplot de métricas antropométricas
@callback(
    Output("boxplot-metric", "figure"),
    Input("metric-dropdown", "value")
)
def update_boxplot(metric):
    fig = px.box(df, x="ID Equipo", y=metric, title=f"Comparación de {metric} entre Equipos")
    return fig

# 🔹 Callback para mostrar la tabla de datos antropométricos con scroll vertical
@callback(
    Output("player-table-container", "children"),
    Input("table-team-dropdown", "value")
)
def update_player_table(selected_team):
    filtered_df = df[df["ID Equipo"] == selected_team]

    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in df.columns],
        fixed_rows={'headers': True},  # 📌 Mantiene los encabezados visibles mientras se desplaza
        style_table={'overflowX': 'auto', 'width': '100%', 'maxHeight': '500px', 'overflowY': 'auto'},  # 📌 Activa el scroll vertical
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': '#007BFF', 'color': 'white', 'fontWeight': 'bold'}
    )
