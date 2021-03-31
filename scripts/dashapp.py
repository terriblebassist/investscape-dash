import dash
import dash_auth
import dash_bootstrap_components as dbc
from decouple import config


app = dash.Dash(
    external_stylesheets=[dbc.themes.MATERIA],
    suppress_callback_exceptions=True
)
auth = dash_auth.BasicAuth(
    app,
    {
        config('ADMIN_USERNAME'): config('ADMIN_PASSWORD')
    }
)
