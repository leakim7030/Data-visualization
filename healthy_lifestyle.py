def init_dashboard(flask_server, route):
    import dash
    from dash import dcc, html, Input, Output
    import plotly.express as px
    import pandas as pd

    # It's better to use an absolute path for the CSV file when deploying to PythonAnywhere.
    data_path = '/home/mikknu17/Data-visualization/healthy_lifestyle_city_2021.csv'
    healthy_lifestyle_df = pd.read_csv(data_path)

    healthy_lifestyle_df['Sunshine hours(City)'] = pd.to_numeric(
        healthy_lifestyle_df['Sunshine hours(City)'], errors='coerce'
    )

    healthy_lifestyle_df['Obesity levels(Country)'] = healthy_lifestyle_df['Obesity levels(Country)'].str.rstrip(
        '%'
    ).astype('float') / 100.0

    # Initialize Dash with the Flask server and the route you want the app to be accessible at.
    app = dash.Dash(__name__, server=flask_server, url_base_pathname=route)

    # Define the layout of the Dash app
    app.layout = html.Div([
        html.H1("Healthy Lifestyle Metrics"),
        html.P("Select a Primary Metric:"),
        dcc.Dropdown(
            id='primary-metric-dropdown',
            options=[
                {'label': 'Happiness Levels', 'value': 'Happiness levels(Country)'},
                # ... the rest of your options
            ],
            value='Happiness levels(Country)'
        ),
        html.P("Select a Secondary Metric:"),
        dcc.Dropdown(
            id='secondary-metric-dropdown',
            options=[
                # ... the same options
            ],
            value='Outdoor activities(City)'
        ),
        dcc.Graph(id='metrics-scatter-plot')
    ])

    # Define the callback for the Dash app
    @app.callback(
        Output('metrics-scatter-plot', 'figure'),
        [Input('primary-metric-dropdown', 'value'),
         Input('secondary-metric-dropdown', 'value')]
    )
    def update_figure(primary_metric, secondary_metric):
        if primary_metric != secondary_metric:
            fig = px.scatter(
                healthy_lifestyle_df,
                x=primary_metric,
                y=secondary_metric,
                size=primary_metric,  # Ensure this column contains numeric data
                color='City',
                hover_name='City',
                title=f"{primary_metric} vs. {secondary_metric}"
            )
        else:
            fig = dash.no_update  # It's better to use dash.no_update here

        return fig

    # Return the Dash app instance
    return app