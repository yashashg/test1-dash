from flask_login import LoginManager, login_user, current_user
from pydoc import classname
import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import csv
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import pandas as pd
from io import BytesIO
import base64
from os import path
from flask_login import login_required
from apps import login_manager


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt




def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    #Calling CSV files from location
    df = pd.read_csv("files/FrequentWords.csv", index_col=0)



    #--------------------------------------------------------------------->
    #Pre-Calculations for visualization

    #table
    cols = ["All Count", "All"]
    selected_cols = df.loc[:, cols]

    #wordcloud
    #--------------------------------------------------------------------->
    #CSS links
    bootstarps = "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
    integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
    crossorigin="anonymous"
    font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
    meta_tags = [{"name": "viewport", "content": "width=device-width"}]
    external_stylesheets = [meta_tags, font_awesome, bootstarps, integrity, crossorigin]

    #----------------------------------------------------------------------->

    #Color Palette
    colors = {'bg': '#111111', 'text': '#7FDBFF'}
    green1 = 'rgba(20, 59, 32, 1)'
    green2 = "rgba(152, 210, 172, 1)"
    Green = "rgba(139, 204, 69, 1)"

    red1= "rgba(120, 20, 20, 1)"
    red2 = "rgba(189, 52, 52, 1)"
    Red = "rgba(237, 124, 119, 1)"

    Yellow = "rgba(240, 192, 65, 1)"

    colors = [Red, Yellow, Green]
    #----------------------------------------------------------------------->


    def server_layout():                
        return html.Div([
  html.Nav([
         html.Div([
            html.Div([
                html.A([
                    html.Div([
                        html.I([],className='feather icon-trending-up')
                    ],className= 'b-bg'),
                    html.Span(["Thrifty AI"],className='b-title')
                ], href = '/dash/', className='b-brand')
            ], className='navbar-brand header-logo'),

            html.Div([
                html.Ul([
                    html.Li([
                        html.Label('Dashboard') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Insights"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/dash/')
                    ],className = 'nav-item active'),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Performance"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page2/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Sentiments"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page3/')
                    ],className = 'nav-item '),
                    html.Li([
                        html.Label('AI Human') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Embedded Link"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/embedded.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Configuration"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/configuration')
                    ],className = 'nav-item '),
                     html.Li([
                        html.Label('More Resources') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Profile Page"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/profile.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Support"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-power')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Logout"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/logout')
                    ],className = 'nav-item '),


                ],className = 'nav pcoded-inner-navbar')  

            ],className = 'navbar-content scroll-div')
        ],className = 'navbar-wrapper')
    ],className = 'pcoded-navbar'),
    
    html.Header([
        html.Div([
            html.A([
                html.Span([])
            ],className='mobile-menu',id='mobile-collapse1',href='javascript:'),
            html.A([
                html.Div([
                    html.I([],className='feather icon-trending-up'),
                ],className='b-bg'),
                 html.Span(["Datta Able"],className='b-title')
            ],className='b-brand', href='/')

        ],className='m-header'),

        html.A([
                html.I([],className='feather icon-more-horizontal')
        ],className='mobile-menu', id='mobile-header', href='javascript:'),
        html.Div([
            html.Ul([
                html.Li([
                    html.A([
                        html.I([],className='feather icon-maximize')
                    ],href='javascript:',className='full-screen')
                ])

            ],className='navbar-nav mr-auto'),

             html.Ul([
                html.Li([
                   html.Label([
                    html.I([],className='icon feather icon-sun', id='theme-indicator'),
                    dcc.Input(
                        id="theme-switch",
                        type='checkbox',
                        className='d-none'
                    )
                   ])
                ]),
                html.Li([
                    html.Div([
                        html.A([
                            html.I([],className='icon feather icon-settings')
                        ],className='dropdown-toggle',href='javascript:'),
                        html.Div([  
                            html.Div([
                                html.A([
                                    html.I([],className='feather icon-log-out'),
                                ],className='dud-logout',href='/auth-signin.html')
                                ],className='pro-head'),
                            html.Ul([
                                html.Li([
                                    html.A([
                                        html.I([],className='feather icon-settings' ),
                                        "Settings"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-user' ),
                                        "Profile"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-lock' ),
                                        "Logout"
                                    ],className='dropdown-item',href='/profile.html')
                                ])
                            ],className='pro-body')
                        ],className='dropdown-menu dropdown-menu-right profile-notification')

                    ],className='dropdown drp-user')
                ])

            ],className='navbar-nav ml-auto')

            

            

        ], className='collapse navbar-collapse')

    ],className='navbar pcoded-header navbar-expand-lg navbar-light'),

  
    html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([

#DropDown
         html.Div([
          html.Div([
              html.Div([
                  html.Div([
                      #html.H4('Month:'),
                     dcc.Dropdown(df.month.unique(), id='month-picker'),
                  ], className='card-body'),
              ], className='card')
          ], className='col-md-4')
      ], className='row'),


        #wordcloud
        html.Div([
          html.Div([
              html.H2('Word Cloud'),
              html.Div([
                           dcc.Graph('Word-graph'),
                      ]),

          ], className='col')
      ], className='row'),

        #top positive negative words
         html.Div([
          html.Div([
              html.Div([
                    html.Div([
                          dcc.Graph('grapH2'),
                    ], className='card-body'),

                    html.Div([
                           dcc.Graph('graph'),
                    ], className='card-body'),

              ], className='row')
          ], className='col')
      ], className='row'),

        #table with all word count
      html.Div([
          html.Div([
              html.H2('Word Cloud Count '),
              html.Div([
                  html.Div([
                      dash_table.DataTable(id='computed-table', columns=[
                          {'name': i, 'id': i} for i in selected_cols],
                                           data=df.to_dict('rows'),
                                           style_table={'overflowX': 'auto'},
                                        style_cell={
                                           'minWidth': '400px',
                                            'overflow': 'hidden',
                                            'textAlign': 'center',
                                        },


                                           style_header={
                                               'backgroundColor': 'rgb(230, 230, 230)',
                                               'color': 'black'
                                           },
                                           style_data={
                                               'backgroundColor': 'rgb(255, 255, 255)',
                                               'color': 'black'
                                           },),
                      dbc.Alert(id='tbl_out'),
                  ]),

              ], className='row')
          ], className='col')
      ], className='row'),

    ],className='container'),

                  ],className='page-wrapper')
                ],className='main-body')
            ],className='pcoded-inner-content')
        ],className='pcoded-content')
    ],className='pcoded-wrapper')
    ],className='pcoded-main-container ')
])


    dash_app.layout = server_layout

    @dash_app.callback(Output('graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_negative(selected_month):
        filtered_df = df[df['month'] == selected_month]
        spaces = ' ' * 2
        Top_neg = df['Top Negative']
        neg_labels = [label + spaces for label in Top_neg]
        traces = []
        traces.append(go.Bar(
            x = df['Negative Count'],
            y = neg_labels,
            orientation='h',
            marker_color="Red",

        ))
        return {'data': traces,
                'layout': go.Layout(title='Negative Keywords',
                                    width=350,
                                    #height=350,
                                    
                                    )}

    @dash_app.callback(Output('grapH2', 'figure'),
                [Input('month-picker', 'value')])
    def update_positive(selected_month):
        filtered_df = df[df['month'] == selected_month]
        spaces = ' ' * 2
        Top_pos = df['Top Positive']
        pos_labels = [label + spaces for label in Top_pos]
        traces = []
        traces.append(go.Bar(
            x = df['Positive Count'],
            y = pos_labels,
            orientation='h',
            marker_color="Green",


        ))
        return {'data': traces,
                'layout': go.Layout(title='Positive Keywords',
                                    width=275,
                                    # height=350,
                                    )}


    @dash_app.callback(Output('grapH2', 'figure'),
                [Input('month-picker', 'value')])
    def update_positive(selected_month):
        filtered_df = df[df['month'] == selected_month]
        spaces = ' ' * 2
        Top_pos = df['Top Positive']
        pos_labels = [label + spaces for label in Top_pos]
        traces = []
        traces.append(go.Bar(
            x = df['Positive Count'],
            y = pos_labels,
            orientation='h',
            marker_color="Green",


        ))


    @dash_app.callback(Output('Word-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_positive(selected_month):
        filtered_df = df[df['month'] == selected_month]


        comment_words = ''

        for i in df.All:
            i = str(i)
            separate = i.split()
            for j in range(len(separate)):
                separate[j] = separate[j].lower()
            comment_words += " ".join(separate) + " "

        final_wordcloud = WordCloud(width=1500, height=800,
                                    background_color='white',
                                    min_font_size=5).generate(comment_words)

        fig_wordcloud = px.imshow(final_wordcloud, template='ggplot2',
                                title="Word CLoud")
        fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        fig_wordcloud.update_xaxes(visible=False)
        fig_wordcloud.update_yaxes(visible=False)

        return fig_wordcloud


    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app



def page2(flask_app):
    page2 = dash.Dash(server=flask_app, name="Dashboard_2", url_base_pathname="/page2/")
    #Calling CSV files from location
   
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



    #Month option loop for dropdown menu
    # month_options = []
    # for month in df['month'].unique():
    #     month_options.append({'label':str(month)})
    #
    # month_labelled_csv = []
    # for month in df2['month'].unique():
    #     month_labelled_csv.append({'label':str(month)})
    #
    #


    #----------------------------------------------------------------------->




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


    def page2_layout():                
        return html.Div([
  html.Nav([
         html.Div([
            html.Div([
                html.A([
                    html.Div([
                        html.I([],className='feather icon-trending-up')
                    ],className= 'b-bg'),
                    html.Span(["Thrifty AI"],className='b-title')
                ], href = '/dash/', className='b-brand')
            ], className='navbar-brand header-logo'),

            html.Div([
                html.Ul([
                    html.Li([
                        html.Label('Dashboard') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Insights"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/dash/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Performance"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page2/')
                    ],className = 'nav-item active'),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Sentiments"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page3/')
                    ],className = 'nav-item '),
                    html.Li([
                        html.Label('AI Human') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Embedded Link"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/embedded.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Configuration"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/configuration.html')
                    ],className = 'nav-item '),
                     html.Li([
                        html.Label('More Resources') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Profile Page"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/profile.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Support"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-power')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Logout"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/logout')
                    ],className = 'nav-item '),


                ],className = 'nav pcoded-inner-navbar')  

            ],className = 'navbar-content scroll-div')
        ],className = 'navbar-wrapper')
    ],className = 'pcoded-navbar'),
    
    html.Header([
        html.Div([
            html.A([
                html.Span([])
            ],className='mobile-menu',id='mobile-collapse1',href='javascript:'),
            html.A([
                html.Div([
                    html.I([],className='feather icon-trending-up'),
                ],className='b-bg'),
                 html.Span(["Datta Able"],className='b-title')
            ],className='b-brand', href='/')

        ],className='m-header'),

        html.A([
                html.I([],className='feather icon-more-horizontal')
        ],className='mobile-menu', id='mobile-header', href='javascript:'),
        html.Div([
            html.Ul([
                html.Li([
                    html.A([
                        html.I([],className='feather icon-maximize')
                    ],href='javascript:',className='full-screen')
                ])

            ],className='navbar-nav mr-auto'),

             html.Ul([
                html.Li([
                   html.Label([
                    html.I([],className='icon feather icon-sun', id='theme-indicator'),
                    dcc.Input(
                        id="theme-switch",
                        type='checkbox',
                        className='d-none'
                    )
                   ])
                ]),
                html.Li([
                    html.Div([
                        html.A([
                            html.I([],className='icon feather icon-settings')
                        ],className='dropdown-toggle',href='javascript:'),
                        html.Div([  
                            html.Div([
                                html.A([
                                    html.I([],className='feather icon-log-out'),
                                ],className='dud-logout',href='/auth-signin.html')
                                ],className='pro-head'),
                            html.Ul([
                                html.Li([
                                    html.A([
                                        html.I([],className='feather icon-settings' ),
                                        "Settings"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-user' ),
                                        "Profile"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-lock' ),
                                        "Logout"
                                    ],className='dropdown-item',href='/profile.html')
                                ])
                            ],className='pro-body')
                        ],className='dropdown-menu dropdown-menu-right profile-notification')

                    ],className='dropdown drp-user')
                ])

            ],className='navbar-nav ml-auto')

            

            

        ], className='collapse navbar-collapse')

    ],className='navbar pcoded-header navbar-expand-lg navbar-light'),

   html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
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
                html.H2('Net Promoter Score'),
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
                html.H2('Customer Satisfaction Score'),
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
                        dcc.Graph('bar-grapH2'),
                    ], className='product-image'),
                ], className='nps-card'),
             ], className='col'),
        ], className='row'),

#gauge part
         html.Div([
          html.Div([
              html.H2('How likely are you to recommend us to your friends and family?* '),
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
#bar grapH2


#bar graph3
    ], className='container'),
    
                  ],className='page-wrapper')
                ],className='main-body')
            ],className='pcoded-inner-content')
        ],className='pcoded-content')
    ],className='pcoded-wrapper')
    ],className='pcoded-main-container ')
])
    page2.layout = page2_layout

    @page2.callback(Output('bar-graph1', 'figure'),
              [Input('month-picker', 'value')])
    def update_bar(selected_month):
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



    @page2.callback(Output('bar-grapH2', 'figure'),
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



    @page2.callback(Output('gauge-graph', 'figure'),
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

    @page2.callback(Output('line-graph', 'figure'),
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
    for view_function in page2.server.view_functions:
        if view_function.startswith(page2.config.url_base_pathname):
            page2.server.view_functions[view_function] = login_required(
                page2.server.view_functions[view_function]
            )



    return page2




def page3(flask_app):
    page3 = dash.Dash(server=flask_app, name="Dashboard_2", url_base_pathname="/page3/")
    df2 = pd.read_csv("files/SentimentTime.csv", index_col=None)
    df3 = pd.read_csv("files/LabeledData.csv", index_col=None)
    #--------------------------------------------------------------------->
    #Pre-Calculations for visualization

    #--------------------------------------------------------------------->


    #Month option loop for dropdown menu
    # month_options = []
    # for month in df['month'].unique():
    #     month_options.append({'label':str(month)})
    #
    # month_labelled_csv = []
    # for month in df2['month'].unique():
    #     month_labelled_csv.append({'label':str(month)})
    #
    #
    #----------------------------------------------------------------------->

    #CSS links
    bootstarps = "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
    integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
    crossorigin="anonymous"
    font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
    meta_tags = [{"name": "viewport", "content": "width=device-width"}]
    external_stylesheets = [meta_tags, font_awesome, bootstarps, integrity, crossorigin]
    #----------------------------------------------------------------------->

    #Color Palette
    colors = {'bg': '#111111', 'text': '#7FDBFF'}
    green1 = 'rgba(20, 59, 32, 1)'
    green2 = "rgba(152, 210, 172, 1)"
    Green = "rgba(139, 204, 69, 1)"

    red1= "rgba(120, 20, 20, 1)"
    red2 = "rgba(189, 52, 52, 1)"
    Red = "rgba(237, 124, 119, 1)"

    Yellow = "rgba(240, 192, 65, 1)"

    colors = [Red, Yellow, Green]




    def page3_layout():                
        return html.Div([
  html.Nav([
         html.Div([
            html.Div([
                html.A([
                    html.Div([
                        html.I([],className='feather icon-trending-up')
                    ],className= 'b-bg'),
                    html.Span(["Thrifty AI"],className='b-title')
                ], href = '/dash/', className='b-brand')
            ], className='navbar-brand header-logo'),

            html.Div([
                html.Ul([
                    html.Li([
                        html.Label('Dashboard') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Insights"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/dash/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Performance"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page2/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Sentiments"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/page3/')
                    ],className = 'nav-item active'),
                    html.Li([
                        html.Label('AI Human') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Embedded Link"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/embedded.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Configuration"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/configuration.html')
                    ],className = 'nav-item '),
                     html.Li([
                        html.Label('More Resources') 
                    ],className = 'nav-item pcoded-menu-caption'),
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Profile Page"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/profile.html')
                    ],className = 'nav-item '), 
                    html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-home')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Support"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/')
                    ],className = 'nav-item '),
                     html.Li([
                      html.A([
                        html.Span([
                            html.I([],className='feather icon-power')
                        ],className='pcoded-micon'),
                        html.Span([
                            "Logout"
                        ],className='pcoded-mtext-micon')
                      ], className= 'nav-link' ,href='/logout')
                    ],className = 'nav-item '),


                ],className = 'nav pcoded-inner-navbar')  

            ],className = 'navbar-content scroll-div')
        ],className = 'navbar-wrapper')
    ],className = 'pcoded-navbar'),
    
    html.Header([
        html.Div([
            html.A([
                html.Span([])
            ],className='mobile-menu',id='mobile-collapse1',href='javascript:'),
            html.A([
                html.Div([
                    html.I([],className='feather icon-trending-up'),
                ],className='b-bg'),
                 html.Span(["Datta Able"],className='b-title')
            ],className='b-brand', href='/')

        ],className='m-header'),

        html.A([
                html.I([],className='feather icon-more-horizontal')
        ],className='mobile-menu', id='mobile-header', href='javascript:'),
        html.Div([
            html.Ul([
                html.Li([
                    html.A([
                        html.I([],className='feather icon-maximize')
                    ],href='javascript:',className='full-screen')
                ])

            ],className='navbar-nav mr-auto'),

             html.Ul([
                html.Li([
                   html.Label([
                    html.I([],className='icon feather icon-sun', id='theme-indicator'),
                    dcc.Input(
                        id="theme-switch",
                        type='checkbox',
                        className='d-none'
                    )
                   ])
                ]),
                html.Li([
                    html.Div([
                        html.A([
                            html.I([],className='icon feather icon-settings')
                        ],className='dropdown-toggle',href='javascript:'),
                        html.Div([  
                            html.Div([
                                html.A([
                                    html.I([],className='feather icon-log-out'),
                                ],className='dud-logout',href='/auth-signin.html')
                                ],className='pro-head'),
                            html.Ul([
                                html.Li([
                                    html.A([
                                        html.I([],className='feather icon-settings' ),
                                        "Settings"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-user' ),
                                        "Profile"
                                    ],className='dropdown-item',href='/profile.html'),
                                     html.A([
                                        html.I([],className='feather icon-lock' ),
                                        "Logout"
                                    ],className='dropdown-item',href='/profile.html')
                                ])
                            ],className='pro-body')
                        ],className='dropdown-menu dropdown-menu-right profile-notification')

                    ],className='dropdown drp-user')
                ])

            ],className='navbar-nav ml-auto')

            

            

        ], className='collapse navbar-collapse')

    ],className='navbar pcoded-header navbar-expand-lg navbar-light'),

   html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
        html.Div([
#DropDown
         html.Div([
          html.Div([
              html.Div([
                  html.Div([
                      #html.H4('Month:'),
                     dcc.Dropdown(df3.month.unique(), id='month-picker'),
                  ], className='card-body'),
              ], className='card')
          ], className='col-md-4')
      ], className='row'),



#Box1

      html.Div([
          html.Div([
              html.Div([
                    html.Div([
                          dcc.Graph('pie-graph'),
                    ], className='card-body'),

                    html.Div([
                           dcc.Graph('bar-graph'),
                    ], className='card-body'),

              ], className='row')
          ], className='col')
      ], className='row'),

#Positive sentences box

html.Div([
          html.Div([
              html.H2('Sample Positive Sentences '),
              html.Div([
                           dcc.Graph('pos-tree')
                      ]),

          ], className='col')
      ], className='row'),

#Negative sentences box

html.Div([
          html.Div([
              html.H2('Sample Negative Sentences '),
              html.Div([
                           dcc.Graph('neg-tree')
                      ]),

          ], className='col')
      ], className='row'),

#positive line graph over time

    html.Div([
          html.Div([
              html.H2('Positive Sentiment Over Time '),
              html.Div([

                           dcc.Graph(id='Positive-graph')
                      ]),

          ], className='col')
      ], className='row'),

#Negative line graph over time
html.Div([
          html.Div([
              html.H2('Negative Sentiment Over Time '),
              html.Div([

                           dcc.Graph(id='Negative-graph')
                      ]),

          ], className='col')
      ], className='row'),

#Rating line graph over time
html.Div([
          html.Div([
              html.H2('Rating Over Time '),
              html.Div([

                           dcc.Graph(id='Rating-graph')
                      ]),

          ], className='col')
      ], className='row'),

#line graph over time
    html.Div([
          html.Div([
              html.H2('Sentiment Over Time'),
              html.Div([

                           dcc.Graph(id='Line-graph')
                      ]),

          ], className='col')
      ], className='row'),

          html.Footer([
              html.H1('Dash'),
              html.Li('Pointer1'),
              html.Li('Pointer2')

          ]),
    ], className='container'),

],className='page-wrapper')
                ],className='main-body')
            ],className='pcoded-inner-content')
        ],className='pcoded-content')
    ],className='pcoded-wrapper')
    ],className='pcoded-main-container ')
])


    page3.layout = page3_layout

    
        
    @page3.callback(Output('pie-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_pie(selected_month):
        filtered_df = df3['month'] == selected_month

        Total_Pos = df3.loc[filtered_df, 'Positive'].sum()
        Total_Neg = df3.loc[filtered_df, 'Negative'].sum()
        Total_Neu = df3.loc[filtered_df, 'Neutral'].sum()

        labels = ['Negative', 'Neutral', 'Positive']
        values = [ Total_Neg, Total_Neu, Total_Pos]

        traces = []
        traces.append(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        return {'data': traces,
                'layout': go.Layout(title='Polarity Distribution',
                                    width=350,
                                    height=350,
                                    )}

    @page3.callback(Output('bar-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_bar(selected_month):
        filtered_df = df3['month'] == selected_month

        Total_Pos = df3.loc[filtered_df, 'Positive'].sum()
        Total_Neg = df3.loc[filtered_df, 'Negative'].sum()
        Total_Neu = df3.loc[filtered_df, 'Neutral'].sum()

        spaces = ' ' * 3
        labels = ['Negative', 'Neutral', 'Positive']
        values = [ Total_Neg, Total_Neu, Total_Pos]
        new_labels = [label + spaces for label in labels]

        traces = []
        traces.append(go.Bar(x=values,y=new_labels, orientation='h', marker_color=colors))
        return {'data': traces,
                'layout': go.Layout(title='Polarity Graph',
                                    #width=350,
                                    height=350,
                                    )}


    @page3.callback(Output('Line-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df2[df2['month'] == selected_month]
        mon = df2['month']
        x = df2['positive']
        y = df2['negative']
        z = df2['neutral']

        fig = go.Figure()
        trace1 = go.Scatter(x=mon, y=y,
                            mode='lines+markers',
                            name='neg',
                            line=dict(color=Red),
                            stackgroup='one')
        trace2 = go.Scatter(x=mon, y=z,
                            mode='lines+markers', name='neu', line=dict(color=Yellow),
                            stackgroup='one')
        trace3 = go.Scatter(x=mon, y=x,
                                mode='lines+markers',
                                name='Pos',
                                line=dict(color=Green),
                            stackgroup='one')

        traces = [trace3, trace2, trace1]
        return {'data': traces,
                'layout': go.Layout(#title='Sentiment Over Time'
        )}


    @page3.callback(Output('Positive-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df2[df2['month'] == selected_month]
        mon = df2['month']
        x = df2['positive']

        fig = go.Figure()
        trace1 = go.Scatter(x=mon, y=x, fill='tozeroy',
                                mode='lines+markers',
                                name='Pos',
                            line=dict(color=Green))

        traces = [trace1]
        return {'data': traces,
                'layout': go.Layout(#title='Sentiment Over Time'
        )}

    @page3.callback(Output('Negative-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df2[df2['month'] == selected_month]
        mon = df2['month']
        y = df2['negative']

        fig = go.Figure()

        trace2 = go.Scatter(x=mon, y=y, fill='tozeroy',
                                mode='lines+markers',
                                name='neg',
                            line=dict(color=Red))

        traces = [trace2]
        return {'data': traces,
                'layout': go.Layout(#title='Sentiment Over Time'
        )}

    @page3.callback(Output('Rating-graph', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df2[df2['month'] == selected_month]
        mon = df2['month']
        z = df2['neutral']

        fig = go.Figure()
        trace3 = go.Scatter(x=mon, y=z, fill='tozeroy',
                                mode='lines+markers', name='neu')
        traces = [trace3]
        return {'data': traces,
                'layout': go.Layout(#title='Sentiment Over Time'
        )}


    @page3.callback(Output('pos-tree', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df3['month'] == selected_month
        pos = df3.loc[filtered_df, 'Positive']
        text = df3.loc[filtered_df, 'text']

        Positive_tree = px.treemap(df3, path=[text], values=pos,

                                template='plotly_white',
                                color_discrete_sequence=[green1, green2, Green],

                                )
        Positive_tree.update_layout(
            margin=dict(t=50, l=25, r=25, b=25)
        )

        return Positive_tree

    @page3.callback(Output('neg-tree', 'figure'),
                [Input('month-picker', 'value')])
    def update_line(selected_month):
        filtered_df = df3['month'] == selected_month
        neg = df3.loc[filtered_df, 'Negative']
        text = df3.loc[filtered_df, 'text']

        Negative_tree = px.treemap(df3, path=[text], values=neg,

                                template='plotly_white',
                                color_discrete_sequence=[red1, red2, Red],

                                )
        Negative_tree.update_layout(
            margin=dict(t=50, l=25, r=25, b=25)
        )

        return Negative_tree

    for view_function in page3.server.view_functions:
        if view_function.startswith(page3.config.url_base_pathname):
            page3.server.view_functions[view_function] = login_required(
                page3.server.view_functions[view_function]
            )


    return page3
