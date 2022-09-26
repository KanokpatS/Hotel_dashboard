from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
pd.options.mode.chained_assignment = None

def preprocess(df:pd.DataFrame) -> pd.DataFrame:
    """
    Clean hotel data
    :param df: Hotel dataframe
    :return: Hotel dataframe
    """
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['rating'] = df['rating'].astype(float)
    df['price'] = df['price'].astype(float)
    df['review'] = df['review'].astype(int)
    df['facilities'] = df['facilities1']
    return df

def create_feature_facilities(df:pd.DataFrame) -> pd.DataFrame:
    """
    Create feature facilities
    :param df: Hotel dataframe
    :return: Hotel dataframe with feature facilities
    """
    all_facilities_list = list()
    for i in range(len(df)):
        facilities1 = df.facilities1[i]
        facilities2 = df.facilities2[i]
        facilities3 = df.facilities3[i]
        facilities4 = df.facilities4[i]
        facilities = [facilities1, facilities2, facilities3, facilities4]
        all_facilities_list.append(facilities1)
        all_facilities_list.append(facilities2)
        all_facilities_list.append(facilities3)
        all_facilities_list.append(facilities4)
        df['facilities'][i] = facilities
    df = df.drop(columns=['facilities1', 'facilities2', 'facilities3', 'facilities4'])
    for fac in list(set(all_facilities_list)):
        df[fac] = 0
    for i in range(len(df)):
        for fac in df['facilities'][i]:
            df[fac][i] = 1
    df['Wi-Fi'] = df['Wi-Fi'] + df['Free Wi-Fi']
    df['Breakfast'] = df['Breakfast'] + df['Free breakfast']
    df = df.drop(columns=['Free Wi-Fi', 'Free breakfast'])
    return df

def find_average_value(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find average value of hotel group by predict class
    :param df:
    :return: Aggregate dataframe
    """
    df_summary = df.groupby(['predict'])\
        .agg(rating=('rating', 'mean'), price=('price', 'mean'), review=('review', 'mean'))
    df_summary = df_summary.reset_index()
    return df_summary

# Prepare hotel data
df = pd.read_excel('data/hotel_data.xlsx')
df = preprocess(df)
df = create_feature_facilities(df)

# Load model prediction data
result = pd.read_excel('data/result.xlsx')

# Plot bar graph from model prediction data
fig_review = px.bar(result, x='predict', y='review')

def plot_map(df:pd.DataFrame) -> pd.DataFrame:
    """
    Plot scatter map with hotel position
    :param df: Hottel dataframee
    :return: Scattr map
    """
    fig = px.scatter_mapbox(df, lat=df.latitude, lon=df.longitude, hover_name="name", hover_data=["price"],
                            color=df.predict, size=df.rating, size_max=10,
                            zoom=9, width=500, center={"lat": 7.965, "lon": 98.346}
                            )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def serve_layout() -> html.Div:
    return html.Div([
        html.Div([
            html.H1('Hotel Dashboard'),
            html.P('Summary of hotel in Phuket'),
            html.Img(src='assets/logo.jpg'),
            html.Label('Star', className='dropdown-labels'),
            dcc.Dropdown(id='star-dropdown', className='dropdown', multi=True,
                         options=[{'label': i, 'value': i} for i in df['star'].unique()],
                         value=['1-star hotel', '2-star hotel', '3-star hotel', '4-star hotel', '5-star hotel']),
            html.Label('Price Range', className='dropdown-labels'),
            dcc.RangeSlider(
                marks={
                0: {'label': '0', 'style': {'color':'white'}},
                1000: {'label': '1000', 'style': {'color':'white'}},
                2000: {'label': '2000', 'style': {'color':'white'}},
                3000: {'label': '3000', 'style': {'color':'white'}},
                4000: {'label': '4000', 'style': {'color':'white'}},
                5000: {'label': '5000', 'style': {'color':'white'}},
                6000: {'label': '6000', 'style': {'color': 'white'}},
                7000: {'label': '7000', 'style': {'color': 'white'}},
                8000: {'label': '8000', 'style': {'color': 'white'}},
                9000: {'label': '9000', 'style': {'color': 'white'}},
            },
            step=1000,
            min=0,
            max=9000, value=[1000, 7000], id='price_slider', className='n-slider'),
            html.Label('Rating Range', className='dropdown-labels'),
            dcc.RangeSlider(
                marks={
                0: {'label': '0', 'style': {'color':'white'}},
                1: {'label': '1', 'style': {'color':'white'}},
                2: {'label': '2', 'style': {'color':'white'}},
                3: {'label': '3', 'style': {'color':'white'}},
                4: {'label': '4', 'style': {'color':'white'}},
                5: {'label': '5', 'style': {'color':'white'}}
            },
                step=1,
                min=0,
                max=5, value=[0, 5], id='rating_slider', className='n-slider'),
            # html.Button(id='update-button', children="Apply Model", n_clicks=0)
        ], id='left-container'),
        html.Div([
            html.Div([
                dcc.Graph(id='map',
                          clickData={'points': [{'hover_text': 'Kalima Resort'}]}
                          ),
                html.Div([
                    html.Label('Hotel information (Click dot on map)', className='other-labels'),
                    html.Div(id='_name', className='result-labels'),
                    html.Div(id='_star', className='result-labels'),
                    html.Div(id='_price', className='result-labels'),
                    html.Div(id='_rating', className='result-labels'),
                    ], id='table-side1')
            ], id='visualisation'),
            html.Div([
                html.Div([
                    dcc.Dropdown(['rating', 'review', 'price'], 'price', id='bar-dropdown'),
                    dcc.Graph(id='price-bar'),
                ], id='data-extract1'),
                html.Div([
                    dcc.Dropdown(['star'], 'star', id='scatter-dropdown'),
                    dcc.Graph(id='star-plot', figure=fig_review),
                ], id='data-extract2')
            ], id='data-extract')
        ], id='right-container')
    ], id='container')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = serve_layout

@app.callback(
    Output('_name', 'children'),
    Output('_star', 'children'),
    Output('_price', 'children'),
    Output('_rating', 'children'),
    Input('map', 'clickData')
)
def display_click_data(clickData):
    name = clickData["points"][0]['hovertext']
    hotel_data = df[df.name == name]
    star = hotel_data.iloc[0, 6]
    price = hotel_data.iloc[0, 7]
    rating = hotel_data.iloc[0, 4]
    return f'Hotel name: {name}', f'Star: {star}', f'Price: {price} Baht', f'Rating: {rating}'

@app.callback(
    Output('map', 'figure'),
    Input('star-dropdown', 'value'),
    Input('price_slider', 'value'),
    Input('rating_slider', 'value')
)
def update_map(star_value, price_range, rating_range):
    new_df = result.copy()
    if len(star_value) > 0:
        new_df = new_df[new_df['star'].isin(star_value)]
    new_df = new_df[new_df.price >= price_range[0]]
    new_df = new_df[new_df.price <= price_range[1]]
    new_df = new_df[new_df.rating >= rating_range[0]]
    new_df = new_df[new_df.rating <= rating_range[1]]
    fig = plot_map(new_df)
    return fig

@app.callback(
    Output('price-bar', 'figure'),
    Input('bar-dropdown', 'value')
)
def update_bar(y_axis):
    agg_result_df = result.copy()
    agg_result_df = agg_result_df[['predict', 'rating', 'price', 'review']]
    agg_result_df = find_average_value(agg_result_df)
    fig = px.bar(agg_result_df, x='predict', y=y_axis)
    return fig

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)