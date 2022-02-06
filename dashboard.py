# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from game import play_multiple_games

app = dash.Dash(__name__)
app.css.append_css({'external_url': '/assets/dashboard.css'})
app.server.static_folder = 'external_stylesheets'

colors = {
    'background': '#3B313C',
    'text': '#F2EFF2',
}

textSize = 64

winners = play_multiple_games(10)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Players": [f"Player {x+1}" for x in range(len(winners))],
    "Wins": winners
})

fig = px.bar(df, x="Players", y="Wins")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    font_size=32
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Luck Game Thing',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontSize': textSize
        }
    ),

    html.Div(children='Adam what is the name for this lol?', style={
        'textAlign': 'center',
        'color': colors['text'],
        'fontSize': textSize
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)