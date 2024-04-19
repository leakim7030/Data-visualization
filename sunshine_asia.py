def init_dashboard(flask_server, route='/sunshine/'):
    import dash
    from dash import dcc, html, Input, Output
    import plotly.express as px
    import pandas as pd
    import plotly.graph_objects as go

    data_path = '/home/mikknu17/Data-visualization/Sunshine in Asian cities.csv'

    sunshine_df = pd.read_csv(data_path)
    sunshine_df_long = sunshine_df.melt(id_vars='City', var_name='Month', value_name='Sunshine Hours')
    sorted_cities = sorted(sunshine_df['City'].unique())
    app = dash.Dash(__name__, server=flask_server, url_base_pathname=route)
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Div([
            html.H1("Sunshine in Asian Cities Dashboard"),
            html.Div([
                dcc.Checklist(
                    id='select-all-check',
                    options=[{'label': ' Select/Deselect All Cities, scroll to select one by one', 'value': 'all'}],
                    value=['all'],
                    inline=True
                ),
                dcc.Dropdown(
                    id='city-selector',
                    options=[{'label': city, 'value': city} for city in sorted_cities],
                    value=sorted_cities,
                    multi=True,
                    style={'height': '100px', 'overflowY': 'auto'}
                ),
                dcc.Dropdown(
                    id='month-selector',
                    options=[{'label': month, 'value': month} for month in sunshine_df.columns[1:]],
                    value=[sunshine_df.columns[1]],
                    multi=True
                ),
                dcc.Dropdown(
                    id='sorting-selector',
                    options=[
                        {'label': 'Most to Least Sunshine(Heatmap)', 'value': 'desc'},
                        {'label': 'Least to Most Sunshine(Heatmap)', 'value': 'asc'}
                    ],
                    value='desc',
                    clearable=False
                )
            ], style={'padding': '20px'}),
        ], style={'background': '#EFEFEF', 'padding': '10px'}),

        html.Div([
            dcc.Graph(id='line-chart', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='bar-chart', style={'width': '50%', 'display': 'inline-block'})
        ]),

        html.Div([
            dcc.Graph(id='heatmap', style={'width': '100%'})
        ], style={'padding': '10px'})
    ])

    @app.callback(
        Output('city-selector', 'value'),
        [Input('select-all-check', 'value')],
        prevent_initial_call=True
    )
    def update_selector(selected_values):
        if 'all' in selected_values:
            return sorted_cities
        return []

    @app.callback(
        Output('line-chart', 'figure'),
        [Input('city-selector', 'value'), Input('month-selector', 'value')]
    )
    def update_line_chart(selected_cities, selected_months):
        if not selected_cities or not selected_months:
            return go.Figure()
        filtered_data = sunshine_df_long[(sunshine_df_long['City'].isin(selected_cities)) & (sunshine_df_long['Month'].isin(selected_months))]
        fig = px.line(filtered_data, x='Month', y='Sunshine Hours', color='City', title="Monthly Sunshine Hours Trends (Best used with fewer cities)")
        return fig

    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('city-selector', 'value')]
    )
    def update_bar_chart(selected_cities):
        if not selected_cities:
            return go.Figure()
        filtered_data = sunshine_df_long[sunshine_df_long['City'].isin(selected_cities)]
        total_sunshine = filtered_data.groupby('City')['Sunshine Hours'].sum().reset_index()
        total_sunshine = total_sunshine.sort_values(by='Sunshine Hours', ascending=False)
        fig = px.bar(total_sunshine, x='City', y='Sunshine Hours', color='City', title="Total Annual Sunshine Hours")
        return fig

    @app.callback(
        Output('heatmap', 'figure'),
        [Input('city-selector', 'value'), Input('month-selector', 'value'), Input('sorting-selector', 'value')]
    )
    def update_heatmap(selected_cities, selected_months, sorting_order):
        if not selected_cities or not selected_months:
            return go.Figure()
        filtered_data = sunshine_df_long[(sunshine_df_long['City'].isin(selected_cities)) & (sunshine_df_long['Month'].isin(selected_months))]
        city_averages = filtered_data.groupby('City')['Sunshine Hours'].mean().reset_index()
        city_averages = city_averages.sort_values(by='Sunshine Hours', ascending=(sorting_order == 'asc'))
        sorted_cities = city_averages['City'].tolist()
        filtered_data = filtered_data[filtered_data['City'].isin(sorted_cities)]
        fig = px.density_heatmap(filtered_data, x='Month', y='City', z='Sunshine Hours', category_orders={'City': sorted_cities}, title="Total Sunshine Hours per Month (Hover over to see values and all cities)")
        return fig

    return app
