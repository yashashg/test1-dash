from flask_login import LoginManager, login_user, current_user
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import csv
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import pandas as pd

login = LoginManager()


def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
        #Calling CSV files from location
    df = pd.read_csv("files/Rating.csv", index_col=None)
    df2 = pd.read_csv("files/LabeledData.csv", index_col=None)
    #--------------------------------------------------------------------->
    #Pre-Calculations for visualization
    Total_rating = len(df)
    Total_response = len(df2)

    #calculating NPS score
    Promoters = df['Promoter'].sum()
    Passive = df['Passive'].sum()
    Detractors = df['Detractor'].sum()

    NPS_score = ((Promoters - Detractors)/Total_rating)*1/100
    NPS = round(NPS_score, 2)


    #calculating CSAT score
    Positive_rating = df2['Positive'].sum()
    Total_Detractors = (Promoters/Total_response)*100
    Total_Passive = (Passive/Total_response)*100
    Total_Promoters = (Promoters/Total_response)*100
    CSAT_score = (Positive_rating/Total_response)*100
    CSAT = round(CSAT_score, 2)

    #Average Rating
    Rating = (df['Rating'].sum())/Total_rating
    Avg_Rating = round(Rating, 2)


    #average interaction duration
    Total_duration = df['Duration'].sum()
    Duration = Total_duration/Total_rating
    Avg_duration = round(Duration, 2)

    #CSS links
    bootstarps = "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
    integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
    crossorigin="anonymous"
    font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
    meta_tags = [{"name": "viewport", "content": "width=device-width"}]
    external_stylesheets = [meta_tags, font_awesome, bootstarps, integrity, crossorigin]
    #CSS Elements
    # 1. Colors
    Red = "rgba(237, 124, 119, 1)"
    Yellow = "rgba(240, 192, 65, 1)"
    Green = "rgba(139, 204, 69, 1)"
    colors = [Red, Yellow, Green]
 

    def server_layout():                
        return html.Div([
    html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 3", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ],
            brand="Main Insights",
            brand_href="#",
            color="black",
            dark=True,
            className='navbar'
        )
    ]),

    html.Div([

    #DropDown
         html.Div([
          html.Div([
              html.Div([
                  html.Div([
                      #html.H4('Month:'),
                      # dcc.DatePickerRange(
                      #     id='date-picker', min_date_allowed=df['Date'],max_date_allowed=date(2017, 9, 19),
                      # ),
                     dcc.Dropdown(df.month.unique(), id='month-picker'),
                  ], className='card-body'),
              ], className='card')
          ], className='col-md-4')
      ], className='row'),


        #card1
        html.Div([
          html.Div([
              html.Div([
                  html.Div([
                      html.H2(Total_response),
                      html.Hr(),
                      html.P('Responses'),
                  ], className='small-card-body'),

              ], className='small-card'),
        ], className='col-md-4'),

              #card2
            html.Div([
              html.Div([
                  html.Div([
                      html.H2(Avg_duration),
                      html.Hr(),
                      html.P('Average Interaction Time'),
                  ], className='small-card-body'),

              ], className='small-card'),
           ], className='col-md-4'),

              #card3
           html.Div([
              html.Div([
                  html.Div([
                   html.H2(Avg_Rating),
                      html.Hr(),
                      html.P('Average Rating'),
                  ], className='small-card-body'),

              ], className='small-card'),
          ], className='col-md-4'),
         ], className='row'),




        #box2
         html.Div([
             html.Div([
                html.H6('Net Promoter Score'),
                html.Div([
                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.H2(NPS),
                        html.Br(),
                        html.Hr(style={"borderWidth":"0.1vh", "width" : "25%", "borderColor":"black"}),
                        html.H5('NPS'),
                        #html.P('Compared to ' + month + '-' + month),

                    ], className='product-details'),

                    html.Div([
                        dcc.Graph('bar-graph1'),
                    ], className='product-image'),
                ], className='nps-card'),
            ], className='col'),
         ], className='row'),

#box 3

        html.Div([
             html.Div([
                html.H6('Customer Satisfaction Score'),
                html.Div([
                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.H2(CSAT),
                        html.Br(),
                        html.Hr(style={"borderWidth":"0.1vh", "width" : "25%", "borderColor":"black"}),
                        html.H5('CSAT'),
                        #html.P('Compared to ' + month + '-' + month),

                    ], className='product-details'),

                    html.Div([
                        dcc.Graph('bar-graph2'),
                    ], className='product-image'),
                ], className='nps-card'),
             ], className='col'),
        ], className='row'),

#gauge part
         html.Div([
          html.Div([
              html.H6('How likely are you to recommend us to your friends and family?* '),
              html.P("Total Responses: " + str(Total_response)),
              html.Div([
                  html.Div([
                      html.Div([

                          html.Div([
                               html.Div([
                                  html.H5("Detractors"),
                                   html.P(str(Detractors) + "%" + " (" + str(Detractors) + ")")
                               ], className='card-body'),

                               html.Div([
                                  html.H5("Passives"),
                                  html.P(str(Passive) + "%" + " (" + str(Passive) + ")")
                               ], className='card-body'),

                               html.Div([
                                  html.H5("Promoters"),
                                  html.P(str(Promoters) + "%" + " (" + str(Promoters) + ")")
                               ], className='card-body'),

                               html.Div([
                                  html.H5("NPS Score"),
                                  html.P(str(NPS))
                               ], className='card-body'),
                          ], className='row'),
                      ], className='p'),


                      dcc.Graph(id='gauge-graph')
                  ], className='card-body'),
              ], className='card')
          ], className='col')
      ], className='row'),


#bar graph1
html.Div([
          html.Div([
              html.Div([
                  html.Div([
                      html.H5('Monthly NPS Score')
                  ], className='card-header'),

                  html.Div([
                      html.Div([

                          dcc.Tabs([
                              dcc.Tab(label='NPS', children=[

                                  html.Div([
                                      html.P('Bar graph depicts monthly NPS score.'),
                                  ], className='p'),
                                  dcc.Graph(id='bar-graph3'),
                              ]),


                              dcc.Tab(label='CSAT', children=[
                                   html.Div([
                                      html.P('Bar Graph depicts monthly CSAT score'),
                                  ], className='p'),
                                  dcc.Graph(id='bar-graph14')
                              ]),
                          ]),
                      ]),

                      html.Div([
                          html.Div([
                             html.Div([
                                 html.H5('Responses by Day and Time '),
                             ]),

                          ], className='p'),

                           dcc.Graph(id='line-graph')
                      ]),
                  ], className='card-body'),
              ], className='card')
          ], className='col')
      ], className='row'),
#bar graph2


#bar graph3



    ], className='container'),
])

    dash_app.layout = server_layout

    @dash_app.callback(Output('bar-graph1', 'figure'),
              [Input('month-picker', 'value')])
    def update_bar(selected_month):
        if current_user.is_authenticated:
            print("bargraph1")
            df = pd.read_csv("files/Rating.csv", index_col=None)
            df2 = pd.read_csv("files/LabeledData.csv", index_col=None)
        filtered_df = df[df['month'] == selected_month]

        spaces = ' '* 3
        NPS_para = ['Detractors', 'Passive', 'Promoters']
        new_NPS_para = [label+spaces for label in NPS_para]

        traces = []
        traces.append(go.Bar(x=[Detractors, Passive, Promoters], y=new_NPS_para, orientation='h', marker_color=colors))

        return {'data': traces,
                'layout': go.Layout(paper_bgcolor='rgba(255, 255, 255, 0.90)',
                                    plot_bgcolor='rgba(255, 255, 255, 0.90)',
                                    width=350,
                                    height=350,
                                    )}

    @dash_app.callback(Output('bar-graph2', 'figure'),
              [Input('month-picker', 'value')])         
    def update_bar(selected_month):
        filtered_df = df2['month'] == selected_month
        spaces = ' ' * 3
        CSAT_para = ['Positive', 'Negative', 'Neutral']
        new_CSAT_para = [label + spaces for label in CSAT_para]
        Positive = df2.loc[filtered_df, 'Positive'].sum()
        Negative = df2.loc[filtered_df, 'Negative'].sum()
        Neutral = df2.loc[filtered_df, 'Neutral'].sum()

        traces = []
        traces.append(go.Bar(x=[Negative, Neutral, Positive], y=new_CSAT_para, orientation='h', marker_color=colors))
        return {'data': traces,
                'layout': go.Layout(#title='CSAT Score',
                                    paper_bgcolor='rgba(255, 255, 255, 0.90)',
                                    plot_bgcolor='rgba(255, 255, 255, 0.90)',
                                    width=350,
                                    height=350,
                                    )}


    @dash_app.callback(Output('gauge-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_bar(selected_month):
        filtered_df = df['month'] == selected_month
        traces = []
        traces.append(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = 70,
        mode = "gauge+number+delta",
        title = {'text': "NPS"},
        delta = {'reference': 50},
        gauge = {'axis': {'range': [None, 100]},
                'steps' : [ #color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                    {'range': [NPS, Promoters], 'color': "lightgray"},
                    {'range': [Promoters, Passive], 'color': "gray"}],
                'threshold' : {'line': {'color': Red, 'width': 4}, 'thickness': 0.75, 'value': NPS}}))
        return {'data': traces,
                'layout': go.Layout(#width=350,
                                    #height=350,
                                    )}

    @dash_app.callback(Output('line-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df['month'] == selected_month

        x = df.loc[filtered_df, 'Day']
        y = df.loc[filtered_df, 'Time']

        fig = go.Figure(data=go.Scatter(x=y, y=x, mode='markers'))
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
        )

        return fig

    return dash_app

