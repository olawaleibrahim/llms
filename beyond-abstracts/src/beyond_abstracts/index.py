from . import model as model
from . import app as home_app
import base64
import glob as glob
import os
import dash
import dash_bootstrap_components as dbc
from dash import callback, no_update, dcc, html, Input, Output, State
import flask
import pandas as pd
import plotly.graph_objects as go
from waitress import serve

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["WORLD_SIZE"] = "1"


server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE,
                          dbc.themes.MATERIA, dbc.icons.FONT_AWESOME],
    server=server
)


index_page = home_app.content

app.title = "beyond Abstracts"
app_states = html.Div([
    dcc.Store(id='node-questions', data=[]),
])


app.layout = dbc.Row([
    app_states,
    dcc.Location(id='url', refresh=False),
    dbc.Col([
        dbc.Row([

        ])
    ], width=12, id='page-content'),
])


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(['Orange', 'Blue', 'Red'], 'Orange', id='page-2-radios'),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    print("pathname", pathname)
    if pathname == '/home':
        return index_page
    elif pathname == "/page2":
        return page_2_layout
    else:
        return index_page


UPLOAD_DIR = "/home/olawale/Desktop/PROJECTS/llms/beyond-abstracts/data/upload/"


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIR, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def get_model_prompt_keywords(query_engine, prompt):
    rag_response = query_engine.query(prompt).response
    keywords_prompt = "Respond without any suffix answer, only listing the keywords in this: " + prompt
    keywords = (query_engine.query(keywords_prompt).response).split(",")
    return rag_response, prompt, keywords


@app.callback(
    Output('llm-rag-output', 'children'),
    Output('prompt-area', 'value'),
    Output("keywords", "options"),
    Output("keywords", "value"),
    State('prompt-area', 'value'),
    Input('llm-rag-output', 'children'),
    Input('explain-button', 'n_clicks'),
    Input('upload-file', 'contents'),
    Input('cytoscape', 'tapNodeData'),
    Input('simplify', 'value'),
    State('upload-file', 'filename'),
    State('node-questions', 'data'),
    prevent_initial_call=True)
def prompt_model(prompt_value, rag_output, prompt_click, file_content, prompt_node, simplify, filename, promptList):

    ctx = dash.callback_context
    print("cxxxxxxx triggerreddddddddddd", ctx.triggered[0]["prop_id"])
    query_engine = model.create_query_engine(UPLOAD_DIR)

    if simplify:
        simplified_prompt_value = "Explain like I'm five: " + rag_output
        return query_engine.query(simplified_prompt_value).response, prompt_value, [], None

    if "cytoscape" in ctx.triggered[0]["prop_id"] and prompt_node:
        prompt_no = int(prompt_node["id"].split("_")[-1])
        prompt_value = promptList[prompt_no]
        rag_response, prompt, keywords = get_model_prompt_keywords(
            query_engine, prompt_value)
        return rag_response, prompt, keywords, keywords[0]  # , promptList

    elif "explain-button" in ctx.triggered[0]["prop_id"]:
        if not prompt_node:
            prompt_node = 1
            prompt_no = 1
        else:
            prompt_no = int(prompt_node["id"].split("_")[-1])
        print("promptList", promptList)
        prompt_value = promptList[prompt_no]
        rag_response, prompt, keywords = get_model_prompt_keywords(
            query_engine, prompt_value)
        return rag_response, prompt, keywords, keywords[0]  # , promptList

    else:
        return no_update


@app.callback(
    Output('node-questions', 'data'),
    Input('submit-button', 'n_clicks'),
    Input('upload-file', 'contents'),
    State('upload-file', 'filename'),
)
def save_uploaded_file(prompt_click, file_content, filename):

    ctx = dash.callback_context
    print("submit button", prompt_click)
    if filename and "upload-file" in ctx.triggered[0]["prop_id"]:
        save_file(filename, file_content)
        query_engine = model.create_query_engine(
            data_path=model.DIRECTORY_PATH)
        query_prompt = "Provide 10 prompts as new lines that explains this paper"
        response_text = query_engine.query(query_prompt).response
        print("initial response", response_text)
        response_text_formatted = response_text.split("\n")
        response_text_formatted = [line[3:]
                                   for line in response_text_formatted[1:]]
        return response_text_formatted


PORT = str(8066)

if __name__ == '__main__':
    print("start")
    serve(app.server, host='0.0.0.0', port=PORT,
          channel_timeout=500, threads=8)
