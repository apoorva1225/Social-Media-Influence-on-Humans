import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
import plotly.express as px

import plotly.graph_objs as go

import flask
import pandas as pd
import time


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

data_df = pd.read_csv("final_Data.csv")

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


colors = {
    'background': '#ffffff',
    'text': '#000000'
}
size = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
        14, 15, 16, 17, 18, 19, 20]

app.layout = html.Div(style={'backgroundColor': colors['background'], 'margin': '20px', 'padding': '50px'}, children=[
    html.H1(
        children='Social Media and its influence on human life',
        style={
            'textAlign': 'center',
            'color': '#663399'
        }
    ),
    html.Div(children='Lets see some interesting relationship amongst internet addiction score, quality of life score and time spent on social media', style={
        'textAlign': 'center',
        'color': colors['text'],
        'marginBottom': '30px'
    }),

    html.Div(children='Demographics analysis on the survey audience', style={
        'color': colors['text'],
        'marginBottom': '10px'
    }),
    html.P("Select category here:"),
    dcc.Dropdown(
        id='names',
        value='Age',
        options=[{'value': x, 'label': x}
                 for x in ['Age', 'Social_media_time_in_hours', 'Education', 'Field', 'Settlement', 'New_vs_Old_user']],
        clearable=False
    ),
    dcc.Graph(id="pie-chart"),


    html.H3(children='Graph 1: Time spent on social media platform vs internet addiction vs quality of life vs Education',
            style={
                'color': 'black',
                'marginTop': '40px',
                'marginBottom': '10px'
            }
            ),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=data_df[data_df['Social_media_time_in_hours'] == i]['IAT'],
                    y=data_df[data_df['Social_media_time_in_hours'] == i]['QOL'],
                    text=data_df[data_df['Social_media_time_in_hours']
                                 == i]['Education'],
                    mode='markers',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in data_df.Social_media_time_in_hours.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'IAT'},
                yaxis={'title': 'QOL'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),


    html.H3(children='Graph 2: Category shaded with Internet Addiction score in ascending order',
            style={
                'color': 'black',
                'marginTop': '40px',
                'marginBottom': '10px'
            }
            ),

    html.P("Select category here:"),
    dcc.Dropdown(
        id='cat',
        value='Age',
        options=[{'value': x, 'label': x}
                 for x in ['Age', 'Social_media_time_in_hours', 'Education', 'Field', 'Settlement', 'New_vs_Old_user', 'QOL']],
        clearable=False
    ),
    dcc.Graph(id='new-chart'),


    html.H3(children='Graph 3: Comparing various category under New-Old user vs Settlement vs Time spent on social media',
            style={
                'color': 'black',
                'marginTop': '40px',
                'marginBottom': '10px'
            }
            ),
    html.P("Select comparison category here:"),
    dcc.Dropdown(
        id='option',
        value='Social_media_time_in_hours',
        options=[{'value': x, 'label': x}
                 for x in ['Age', 'Social_media_time_in_hours', 'Education', 'Field']],
        clearable=False
    ),
    dcc.Graph(id='facet-chart'),

    html.H3(children='Graph 4: Age vs time spent on social media',
            style={
                'color': 'black',
                'marginTop': '40px',
                'marginBottom': '10px'
            }
            ),
    html.P("Select age here:"),
    dcc.Dropdown(
        id='age',
        value='below 18',
        options=[{'value': x, 'label': x}
                 for x in ['below 18', '18-22', '23-25', '26-28', 'Above 28']],
        clearable=False
    ),
    dcc.Graph(id="Age-pie-chart"),


    html.H3(children='Graph 5: Time spent on social media platform vs internet addiction vs quality of life',
            style={
                'color': 'black',
                'marginTop': '40px',
                'marginBottom': '10px'
            }
            ),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': data_df.Social_media_time_in_hours, 'y': data_df.IAT,
                    'type': 'bar', 'name': 'IAT'},
                {'x': data_df.Social_media_time_in_hours, 'y': data_df.QOL,
                    'type': 'bar', 'name': 'QOL'},
            ],
            'layout': {
                'title': 'Comparison of Internet Addiction score (IAT) and Quality of life score (QOL) wrt Time spent on social media',
                'xaxis': {
                    'title': 'Time spent on social media (in hours)'
                },
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),


])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value")])
def generate_chart(names):
    fig = px.pie(data_df, names=names)
    return fig


@app.callback(
    Output("Age-pie-chart", "figure"),
    [Input("age", "value")])
def generate_age_chart(age):
    fig = px.pie(data_df[data_df['Age'] == age], names='New_vs_Old_user')
    return fig


@app.callback(
    Output("facet-chart", "figure"),
    [Input("option", "value")])
def generate_facet_chart(option):
    fig = px.bar(data_df, x=option, y="IAT", color="Age", barmode="group",
                 facet_row="Settlement", facet_col="New_vs_Old_user",
                 category_orders={"New_vs_Old_user": ['less than one year', '2 years ago', '3 years ago', '4 years ago or higher'],
                                  "Settlement": ['Urban', 'Rural']}
                 #   "Age": ['below 18', '18-22', '23-25', '26-28', 'Above 28']}
                 #  category_orders={"Field": ["Management", "Finance", "Arts, Psychology and Sociology", "Law", "Education Teaching", "Pharmacy", "Tourism management", "Fine Arts"],
                 #                   "Education": ['10th grade', '12th grade', 'Diploma', "Bachelor's Degree", "Master's Degree", "PhD Degree"]}
                 )
    return fig


@app.callback(
    Output("new-chart", "figure"),
    [Input("cat", "value")])
def generate_new_chart(cat):
    fig = px.bar(data_df, y=cat, x='index',
                 color='IAT',
                 labels={'QOL': 'Quality of life'}, height=400)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)