import glob as glob
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc, html
import flask
import pandas as pd
import random


server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE,
                          dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
    server=server
)


app.title = "Beyond Abstracts"
title = app.title


default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "mapData(size, 0, 100, 20, 60)",
            "height": "mapData(size, 0, 100, 20, 60)",
            "content": "data(label)",
            "font-size": "5%",
            "text-valign": "center",
            "text-halign": "center",
            "background-fill": "red",
            "background-gradient-stop-colors": 'data(background_color)',
            # "background-gradient-stop-positions": '0, 80, 90, 100',
            'color': 'data(color)',
        }
    },
    {
        'selector': 'edge',
        'style': {
            # "line-fill": "linear-gradient",
            "line-gradient-stop-colors": 'data(colors)',
            "line-gradient-stop-positions": "10, 20, 30, 40, 50, 60, 70, 80, 90",
            'width': 0.25,
            # 'curve-style': 'bezier',
            # 'source-endpoint': 'outside-to-node',
            # 'target-endpoint': 'outside-to-node'
        }
    }
]


nodeSize = 100
maxX = 250
maxY = 250
created_elements = []
no_nodes = 10
no_edges = no_nodes*4

for i in range(1, no_nodes+1):

    if i % 5 == 0:
        nodeSize /= 2
    if i > 10:
        nodeSize /= 2
    x = random.randint(0, maxX)
    y = random.randint(0, maxY)
    element = {'data': {'id': f'prompt_{i}', 'label': f'Prompt {i}',
                        'size': nodeSize}, 'position': {'x': x, 'y': y}}
    created_elements.append(element)
    created_elements.append(
        {'data': {'source': 'prompt_1', 'target': 'prompt_2', 'label': 'Node 1 to 2'}})

for i in range(1, no_edges+1):

    source = f"prompt_"+str(random.randint(1, no_nodes))
    target = f"prompt_"+str(random.randint(1, no_nodes))

    if source != target:
        created_elements.append(
            {'data': {'source': source, 'target': target, 'label': f'Prompt {source} to {target}'}})

print("lengthtttt", len(created_elements))


cyto_components = html.Div([
    cyto.Cytoscape(
        id="cytoscape",
        elements=created_elements,
        layout={'name': 'preset'},
        stylesheet=default_stylesheet
    )
], style={"width": "100%"})


main_content = dbc.Card(
    children=dbc.CardBody([
        dbc.Row([
            dbc.Col([], width=2),
            dbc.Col([cyto_components], width=8),
            dbc.Col([], width=2)
        ], style={"height": "70vh", "width": "100%"}),
        dbc.Row([
            dbc.Col([
                dcc.Upload([
                    'Drag and Drop or ',
                    html.A('Select a File')
                ], id="upload-file",
                    style={
                    'width': '100%',
                    'height': '100%',
                    'lineHeight': '100%',
                    'borderWidth': '100%',
                    'borderStyle': 'dashed',
                    'borderRadius': '1%',
                    'textAlign': 'center'
                }),
                dbc.Label("Keywords"),
                dcc.Dropdown([], id='keywords'),
                dcc.Textarea(
                    id='prompt-area',
                    value='Hey dude, what is this paper all about?',
                    style={'width': '100%', 'height': '50%'},
                ),
                daq.ToggleSwitch(
                    id='simplify',
                    label="simplify",
                    labelPosition="bottom",
                    value=False,
                    # disabled=True,
                    color="#403B3B",
                    style={"width": "20%", "float": "left"},
                    className="button",
                ),
                html.Button('Explain', id='explain-button', title="Prompt",
                            style={"width": "20%", "float": "right"}),
                html.Button('Submit', id='submit-button', title="Submit",
                            style={"width": "20%", "float": "right"}),
            ], width=9),
            dbc.Col([
                html.Div("hello", id='llm-rag-output',
                         style={'whiteSpace': 'pre-line'})
            ], width=3)
        ], style={"height": "20vh"})
    ]),
)


content = html.Div([html.H1(id='page-title', style={'padding-left': '1%', 'padding-top': '1%'}),
                    html.Div([html.Div([main_content], style={'padding': '1% !important', 'width': '100%'}),])],
                   className='app-content-div',
                   )


app.layout = html.Div(
    [
        # dcc.Store(id='timestamp', storage_type='memory', data=timestamp),
        dbc.Row([
            dbc.Col([
                html.Div(
                    [
                        dash.page_container,
                        main_content
                    ],
                    className="content",
                ),
            ], width=12)
        ],
            style={"background-color": "#07141F"})
    ])
