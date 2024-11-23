import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Sample data
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 20, 30, 40],
    'Extra': [15, 25, 35, 45]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(
    
    style={'font-family': 'Arial, sans-serif', 'margin': '20px'},
    children=[
        html.H1("Dynamic Graph Generator ", style={'text-align': 'center', 'color': '#333'}),
        html.H2("explore graphs that you can use as a data analisys .... ", style={'text-align': 'center', 'color': '#333'}),

        html.Div(
            style={'margin-bottom': '20px'},
            children=[
                html.Label("Choose a Graph Type:", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='graph-type',
                    options=[
                        {'label': 'Line Plot', 'value': 'line'},
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Scatter Plot', 'value': 'scatter'},
                        {'label': 'Histogram', 'value': 'histogram'},
                        {'label': '3D Scatter Plot', 'value': '3d-scatter'},
                        {'label': '3D Line Plot', 'value': '3d-line'},
                        {'label': 'Pie Chart', 'value': 'pie'},
                        {'label': 'Box Plot', 'value': 'box'},
                        {'label': 'Heatmap', 'value': 'heatmap'},
                        {'label': 'Bubble Chart', 'value': 'bubble'},
                        {'label': 'Density Contour Plot', 'value': 'density-contour'},
                        {'label': 'Area Chart', 'value': 'area'},
                        {'label': 'Polar Chart', 'value': 'polar'},
                        {'label': 'Funnel Chart', 'value': 'funnel'},
                        {'label': 'Sunburst Chart', 'value': 'sunburst'},
                        {'label': 'Treemap', 'value': 'treemap'},
                        {'label': 'Radar Chart', 'value': 'radar'}
                    ],
                    placeholder="Select a graph type",
                    style={'width': '50%'}
                )
            ]
        ),
        html.Div(
            style={'text-align': 'center', 'margin-bottom': '20px'},
            children=[
                html.Button("Save Generated File", id="save-btn", style={
                    'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                    'border': 'none', 'cursor': 'pointer', 'font-size': '16px'
                }),
                dcc.Download(id="download-file")
            ]
        ),
        dcc.Graph(id='graph-output', style={'border': '1px solid #ddd', 'padding': '10px'}),
    ]
)

# Callback for graph rendering
@app.callback(
    Output('graph-output', 'figure'),
    Input('graph-type', 'value')
)
def update_graph(graph_type):
    if not graph_type:
        return go.Figure()  # Empty figure
    if graph_type == 'line':
        return px.line(df, x='Category', y='Values', title='Line Plot')
    elif graph_type == 'bar':
        return px.bar(df, x='Category', y='Values', title='Bar Chart')
    elif graph_type == 'scatter':
        return px.scatter(df, x='Category', y='Values', size='Extra', color='Category', title='Scatter Plot')
    elif graph_type == 'histogram':
        return px.histogram(df, x='Values', title='Histogram')
    elif graph_type == '3d-scatter':
        return px.scatter_3d(df, x='Category', y='Values', z='Extra', color='Category', title='3D Scatter Plot')
    elif graph_type == '3d-line':
        fig = go.Figure(go.Scatter3d(x=df['Category'], y=df['Values'], z=df['Extra'], mode='lines'))
        fig.update_layout(title='3D Line Plot')
        return fig
    elif graph_type == 'pie':
        return px.pie(df, names='Category', values='Values', title='Pie Chart')
    elif graph_type == 'box':
        return px.box(df, x='Category', y='Values', title='Box Plot')
    elif graph_type == 'heatmap':
        return px.density_heatmap(df, x='Category', y='Values', title='Heatmap')
    elif graph_type == 'bubble':
        return px.scatter(df, x='Category', y='Values', size='Extra', color='Category', title='Bubble Chart')
    elif graph_type == 'density-contour':
        return px.density_contour(df, x='Category', y='Values', title='Density Contour Plot')
    elif graph_type == 'area':
        return px.area(df, x='Category', y='Values', title='Area Chart')
    elif graph_type == 'polar':
        return px.line_polar(df, r='Values', theta='Category', title='Polar Chart')
    elif graph_type == 'funnel':
        return px.funnel(df, x='Category', y='Values', title='Funnel Chart')
    elif graph_type == 'sunburst':
        return px.sunburst(df, path=['Category'], values='Values', title='Sunburst Chart')
    elif graph_type == 'treemap':
        return px.treemap(df, path=['Category'], values='Values', title='Treemap')
    elif graph_type == 'radar':
        fig = go.Figure()
        for col in df.columns[1:]:
            fig.add_trace(go.Scatterpolar(
                r=df[col],
                theta=df['Category'],
                fill='toself',
                name=col
            ))
        fig.update_layout(title='Radar Chart')
        return fig

# Callback to save the current graph as an image
@app.callback(
    Output("download-file", "data"),
    Input("save-btn", "n_clicks"),
    Input('graph-type', 'value'),
    prevent_initial_call=True
)
def save_graph(n_clicks, graph_type):
    if not graph_type:
        return None
    fig = update_graph(graph_type)
    return dcc.send_file(fig.to_image(format="png", engine="kaleido"))

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
