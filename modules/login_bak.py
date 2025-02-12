import dash
from dash import dcc, html, Input, Output, State, callback

# Layout del login con diseño mejorado
layout = html.Div([
    html.Div([
        html.Img(src='/assets/logo.png', style={'width': '100px', 'display': 'block', 'margin': 'auto'}),
        html.H2("Inicio de Sesión", style={'textAlign': 'center', 'margin-bottom': '20px'}),

        dcc.Input(id='username', type='text', placeholder="Usuario", 
                  style={'width': '90%', 'margin-bottom': '10px', 'padding': '10px', 'fontSize': '16px'}),
        
        dcc.Input(id='password', type='password', placeholder="Contraseña", 
                  style={'width': '90%', 'margin-bottom': '20px', 'padding': '10px', 'fontSize': '16px'}),

        html.Button("Ingresar", id="login-button", n_clicks=0, 
                    style={'width': '100%', 'padding': '10px', 'background-color': '#007BFF', 'color': 'white',
                           'border': 'none', 'cursor': 'pointer', 'fontSize': '16px'}),

        html.Div(id='login-output', style={'margin-top': '10px', 'textAlign': 'center', 'color': 'red'})
    ], 
    style={
        'width': '350px', 'padding': '30px', 'border': '2px solid #007BFF', 'border-radius': '10px',
        'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'background': 'white',
        'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'
    })
], style={'height': '100vh', 'background-color': '#f4f4f4'})

# Callback de autenticación
@callback(
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True
)
def authenticate(n_clicks, username, password):
    valid_users = {"Admin": "admin"}  # Simulación de base de datos

    if username in valid_users and valid_users[username] == password:
        return "✅ Acceso concedido. Redirigiendo..."
    else:
        return "❌ Usuario o contraseña incorrectos"
