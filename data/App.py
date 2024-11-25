from dash import Dash, dcc, html, Input, Output, State, ctx
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64
import seaborn as sns
import numpy as np
import os

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Intelligent Visualization App", style={'text-align': 'center'}),

    # File Upload Section
    html.Div([
        html.H4("Upload a File:"),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px auto'
            },
            multiple=False
        ),
        html.Div(id='file-name', style={'margin-top': '10px', 'font-weight': 'bold', 'color': 'green'}),
        dcc.Loading(id="loading", type="circle", children=[html.Div(id="loading-message")]),
    ]),

    # Graph Type Selector
    html.Div([
        html.H4("Select Graph Type:"),
        dcc.Dropdown(
            id='graph-type',
            options=[
                {'label': 'Line Plot', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Histogram', 'value': 'histogram'},
                {'label': 'Heatmap', 'value': 'heatmap'},
                {'label': 'Pie Chart', 'value': 'pie'}
            ],
            placeholder="Choose a graph type...",
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    # Graph Suggestions Section
    html.Div(id='graph-suggestions', style={'margin': '20px', 'text-align': 'center', 'color': 'red'}),

    # Graph Output Section
    html.Div([
        html.H4("Generated Graph:"),
        dcc.Graph(id='output-graph'),
    ]),

    # Live Graph Section
    html.Div([
        html.H4("Live Graph Visualization:"),
        html.Div(id='live-graph-output')
    ])
])

# Helper Function: Decode Uploaded File
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if filename.endswith('.csv'):
        return pd.read_csv(BytesIO(decoded))
    elif filename.endswith('.xlsx'):
        return pd.read_excel(BytesIO(decoded))
    elif filename.endswith('.json'):
        return pd.read_json(BytesIO(decoded))
    return None

# Callback to display the file name
@app.callback(
    Output('file-name', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def display_file_name(contents, filename):
    if contents:
        return f"File Selected: {filename}"
    return "No file selected."

# Callback for Graph Generation with Loading Logic
@app.callback(
    [Output('output-graph', 'figure'),
     Output('graph-suggestions', 'children'),
     Output('loading-message', 'children')],
    Input('upload-data', 'contents'),
    Input('graph-type', 'value'),
    State('upload-data', 'filename')
)
def update_graph(contents, graph_type, filename):
    if not contents or not graph_type:
        return {}, "", "Select a graph type to display."

    # Show loading message
    loading_message = "Processing your file and generating graph..."

    # Parse File
    df = parse_contents(contents, filename)
    if df is None:
        return {}, "Unsupported file type. Please upload a CSV, Excel, or JSON file.", ""

    # Generate Graph
    try:
        if graph_type == 'line':
            fig = px.line(df, x=df.columns[0], y=df.columns[1:])
        elif graph_type == 'bar':
            fig = px.bar(df, x=df.columns[0], y=df.columns[1:])
        elif graph_type == 'scatter':
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
        elif graph_type == 'histogram':
            fig = px.histogram(df, x=df.columns[0])
        elif graph_type == 'heatmap':
            corr = df.corr()
            fig = px.imshow(corr, text_auto=True, color_continuous_scale='viridis')
        elif graph_type == 'pie':
            fig = px.pie(df, names=df.columns[0], values=df.columns[1])
        else:
            fig = {}
        return fig, "", ""  # Clear loading message
    except Exception as e:
        suggestions = f"Graph '{graph_type}' cannot be generated. Try Line Plot, Bar Chart, or Histogram."
        return {}, suggestions, ""

# Live Graph Callback (Matplotlib Example)
@app.callback(
    Output('live-graph-output', 'children'),
    Input('graph-type', 'value')
)
def live_visualization(graph_type):
    if graph_type == 'line':
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.figure()
        plt.plot(x, y)
        plt.title("Live Line Plot")
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        return html.Img(src=f'data:image/png;base64,{encoded_image}')
    return ""


# Main Function for Deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)
