import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ctx
import os

# Importar módulos de la aplicación
from modules import login, mod_tabla_posiciones, mod_estadisticas, mod_antropometria

# Inicializar la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Render y Gunicorn necesitan esta variable

# 📌 Estructura Inicial de la Aplicación (Solo Login)
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", storage_type="session"),  # Guardar sesión del usuario
    html.Div(id="page-content")  # 📌 Aquí se mostrará Login o el Dashboard según la sesión
])

# 📌 Callback para manejar la autenticación
@app.callback(
    Output("url", "pathname"),
    Output("session-store", "data"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    State("session-store", "data"),
    prevent_initial_call=True
)
def handle_authentication(login_clicks, username, password, session_data):
    triggered_id = ctx.triggered_id or ""

    if triggered_id == "login-button":  # 🏆 Inicio de sesión
        valid_users = {"Admin": "admin"}  

        if username in valid_users and valid_users[username] == password:
            return "/home", {"logged_in": True}  
        else:
            return dash.no_update, {"logged_in": False}  

    return dash.no_update, dash.no_update  

# 📌 Callback para mostrar Login o Dashboard según la sesión
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("session-store", "data")
)
def display_page(pathname, session_data):
    if not session_data or not session_data.get("logged_in", False):
        return login.layout

    sidebar = html.Div([
        html.H2("Menú", className="text-center"),
        html.Hr(),
        dcc.Link("🏆 Tabla de Posiciones", href="/tabla-posiciones", className="menu-link"),
        dcc.Link("📊 Estadísticas de Jugadores", href="/estadisticas", className="menu-link"),
        dcc.Link("⚕️ Datos Antropométricos", href="/antropometria", className="menu-link"),
        dcc.Link("❌ Cerrar Sesión", href="/logout", className="menu-link-exit")
    ], className="sidebar")

    content = html.Div()

    if pathname == "/tabla-posiciones":
        content.children = mod_tabla_posiciones.layout
    elif pathname == "/estadisticas":
        content.children = mod_estadisticas.layout
    elif pathname == "/antropometria":
        content.children = mod_antropometria.layout
    elif pathname == "/logout":
        return login.layout  
    else:
        content.children = html.H3("Bienvenido al Dashboard", className="text-center")

    return html.Div([sidebar, content])

# 📌 Configurar la ejecución en Render con el puerto correcto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Render asigna el puerto automáticamente
    app.run_server(host="0.0.0.0", port=port, debug=False)

