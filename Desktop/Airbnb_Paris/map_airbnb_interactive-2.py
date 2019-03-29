# import dash components
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import pandas for handle data
import pandas as pd

import os
# import library for graph
import plotly.graph_objs as go

# API of mapbox
mapbox_access_token = 'pk.eyJ1IjoibWlja2FtaWNrYSIsImEiOiJjanRyZXF6b3UwamdvNDRtcmwzeW9oZnh0In0.cfEb9qNJq7wDxWP-aQOHZw'

# Where is the data
DATA_DIR = 'airbnb-paris/'

# css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load data
listings_df = pd.read_csv(os.path.join(DATA_DIR,'listings.csv'),
                          usecols = ['id', 'price', 'longitude', 'latitude', 'bathrooms', 'bedrooms','availability_365'])

# clean data
def correction(x):
    ''' Columns value corrections '''
    if type(x)==str:
        x=x.replace('$','')
        x=x.replace(',','')
        x=float(x)
    return (x)
listings_df['price'] = listings_df['price'].apply(correction)

# application Dash
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# layout of the application
app.layout = html.Div([
    html.Div([html.H1(children = 'Web application Dash : airbnb listings in Paris', style = {'textAlign': 'center'})
    ]),
    html.Div([
        html.Div([
            html.H3(
                children = 'Choose variable: '
            ),
            # multi input
            dcc.Dropdown(
                id = 'color-column',
                options = [{'label': i, 'value': i} for i in ['price', 'bathrooms', 'bedrooms','availability_365']],
                value = 'price'
            )
        ]),
        html.Div([
            html.H3(
                children = 'Choose the limitation: '
            ),
            # choose the float input
            dcc.Input(
                id = 'top',
                type = 'number',
                value = 400
            )
        ]),
        # put the graph in the application
        dcc.Graph(id ='map')
    ])
])
# define the inputs and the output
@app.callback(
    Output('map', 'figure'),
    [Input('color-column', 'value'),
    Input('top', 'value')]
)
def update_map(color_col, top):
    # filter the datasets
    df = listings_df[listings_df[color_col] < top]
    return {
        'data' : [
        # plot the map with specific variable
            go.Scattermapbox(
                lat=df['latitude'],
                lon=df['longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=3,
                    color = df[color_col],
                    colorscale='Viridis',
                    showscale=True
                ))],
        'layout' : go.Layout(
            height = 800,
            autosize=True,
            hovermode='closest',
            mapbox=go.layout.Mapbox(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=48.86,
                    lon=2.35
                ),
                pitch=0,
                zoom=11,
            ),

        )
}

# run the application
if __name__ == '__main__':
    # debug = True -> refresh automatically
    app.run_server(debug=True)
