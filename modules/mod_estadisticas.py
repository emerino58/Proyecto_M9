import pandas as pd
from dash import dcc, html, dash_table, Input, Output, callback  # 🔹 Importación corregida
import plotly.express as px

# Cargar datos
df = pd.read_excel("data/DataSets_Sub16.xlsx")

# 🔹 Tabla de distribución de jugadores por puesto
posiciones = df.pivot_table(index="ID Equipo", columns="Posición", aggfunc="size", fill_value=0).reset_index()

# Layout del módulo
layout = html.Div([
    html.Img(src='/assets/logo.png', style={'width': '100px', 'display': 'block', 'margin': 'auto'}),
    html.H3("Estadísticas de Jugadores", className="text-center"),

    # 📌 Tabla de distribución de jugadores por puesto
    html.H4("Distribución de Jugadores por Posición"),
    html.Div([
        dash_table.DataTable(
            data=posiciones.to_dict('records'),
            columns=[{"name": col, "id": col} for col in posiciones.columns],
            style_table={'overflowX': 'auto', 'width': '100%', 'margin': 'auto'},  # 🔹 Mostrar tabla completa
            style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': '#007BFF', 'color': 'white', 'fontWeight': 'bold'}
        )
    ]),

    html.Hr(style={'border': '1px solid #ddd'}),

    # 📊 Gráfico de distribución de jugadores por edad
    html.H4("Distribución de Jugadores por Edad"),
    dcc.Graph(id="bar-age-distribution"),

    html.Hr(style={'border': '1px solid #ddd'}),

    # 🔄 Comparación de minutos jugados entre dos equipos
    html.H4("Comparación de Minutos Jugados por Jugador"),
    
    html.Div([
        html.Label("Selecciona Equipo 1:", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='team1-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                     value=df["ID Equipo"].unique()[0], style={'width': '45%'}),  

        html.Label("Selecciona Equipo 2:", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='team2-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                     value=df["ID Equipo"].unique()[1], style={'width': '45%'}),  
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

    html.Div([
        dcc.Graph(id="team1-line-graph", style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id="team2-line-graph", style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Hr(style={'border': '1px solid #ddd'}),

    # 📌 Selección de equipo y jugador para gráfico radial de barras
    html.H4("Rendimiento Individual del Jugador"),
    
    html.Label("Selecciona un equipo:", style={'font-weight': 'bold'}),
    dcc.Dropdown(id='team-dropdown', options=[{"label": team, "value": team} for team in df["ID Equipo"].unique()],
                 value=df["ID Equipo"].unique()[0], style={'width': '60%'}),  

    html.Label("Selecciona un jugador:", style={'font-weight': 'bold'}),
    dcc.Dropdown(id='player-dropdown', placeholder="Seleccione un jugador...",
                 style={'width': '60%'}),  

    dcc.Graph(id="radial-bar-chart")  # 📌 Gráfico Radial de Barras
])

# 🔹 Callback para el gráfico de distribución de edades agrupado
@callback(
    Output("bar-age-distribution", "figure"),
    Input("team1-dropdown", "value")  
)
def update_age_distribution(_):
    edad_counts = df["Edad (años.meses)"].value_counts().reset_index()
    edad_counts.columns = ["Edad (años.meses)", "Total de Jugadores"]
    
    fig = px.bar(edad_counts, x="Edad (años.meses)", y="Total de Jugadores",
                 title="Distribución de Jugadores por Edad", text_auto=True)
    return fig

# 🔹 Callback para actualizar los gráficos de comparación de minutos jugados
@callback(
    [Output("team1-line-graph", "figure"), Output("team2-line-graph", "figure")],
    [Input("team1-dropdown", "value"), Input("team2-dropdown", "value")]
)
def update_minutes_graph(team1, team2):
    df_team1 = df[df["ID Equipo"] == team1]
    df_team2 = df[df["ID Equipo"] == team2]

    fig1 = px.line(df_team1, x="ID Jugador", y="N° Minutos Jugados", title=f"Minutos Jugados - {team1}")
    fig2 = px.line(df_team2, x="ID Jugador", y="N° Minutos Jugados", title=f"Minutos Jugados - {team2}")

    return fig1, fig2

# 🔹 Callback para actualizar la lista de jugadores con nombres "Jugador 1, Jugador 2, ..."
@callback(
    [Output("player-dropdown", "options"),
     Output("player-dropdown", "value")],
    Input("team-dropdown", "value")
)
def update_player_list(selected_team):
    players = df[df["ID Equipo"] == selected_team]["ID Jugador"].unique()
    
    # 🔹 Convertir nombres de "Equipo_1_J1" a "Jugador 1", "Jugador 2", ...
    player_options = [{"label": f"Jugador {i+1}", "value": player} for i, player in enumerate(players)]
    
    if len(players) == 0:
        return [], None  # Si no hay jugadores, vacía la lista

    return player_options, players[0]  # Selecciona el primer jugador automáticamente

# 🔹 Callback para generar el Gráfico Radial de Barras con líneas más intensas
@callback(
    Output("radial-bar-chart", "figure"),
    [Input("team-dropdown", "value"),
     Input("player-dropdown", "value")]
)
def update_radial_chart(selected_team, selected_player):
    if not selected_player:
        return px.scatter(title="Seleccione un jugador para ver sus estadísticas")

    filtered_df = df[(df["ID Equipo"] == selected_team) & (df["ID Jugador"] == selected_player)]
    
    if filtered_df.empty:
        return px.scatter(title="No hay datos para el jugador seleccionado")

    player_data = filtered_df.iloc[0]

    categories = ["Tasa de Participación (%)", "% Pases efectivos", "% Acciones efectivas",
                  "% Duelos Ganados", "% Balones recuperados", "% Duelos Aéreos ganados",
                  "% de regates exitosos", "% de barridas exitosas"]

    values = [player_data[metric] for metric in categories]

    fig = px.bar_polar(
        r=values, theta=categories, title=f"Rendimiento de {selected_player}",
        color=categories
    )

    fig.update_layout(
        polar=dict(
            bgcolor="white",
            angularaxis=dict(gridcolor="black", gridwidth=1.5, linecolor="gray", linewidth=2),
            radialaxis=dict(gridcolor="black", gridwidth=2, linecolor="gray", linewidth=2)
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    return fig


