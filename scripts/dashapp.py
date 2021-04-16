import dash
import dash_auth
import dash_bootstrap_components as dbc
from decouple import config


app = dash.Dash(
    meta_tags=[{
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0, \
            maximum-scale=1.2, minimum-scale=0.5,'
    }],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

if config('PROFILE', default='int') == 'PROD':
    auth = dash_auth.BasicAuth(
        app,
        {
            config('ADMIN_USERNAME'): config('ADMIN_PASSWORD')
        }
    )
