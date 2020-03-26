import pandas as pd
import numpy as np
import dash
import flask
import joblib
import math
import dash_core_components as dcc
import dash_html_components as html
import time
from dash.dependencies import Input, Output
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'figure':'#D3D3D3',
    'header':'#33F9FF',
    'red':'#8B0000'}
def serve_layout():

    # send initial layout if there is flask request context
    if flask.has_request_context():
        return layout_index

    # otherwise send every element to dash validator to prevent callback exceptions
    return html.Div([
        layout_index,
        layout_tab_1])
layout_index = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Reset', value='tab-1',style={'width':'50%','height':'40%'})

  
    ]),
    html.Div(id='tabs-content')])

df=pd.DataFrame({'index':0},index=[0])
app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
layout_tab_1=html.Div(id='main',style={'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RMS_Titanic_3.jpg/1024px-RMS_Titanic_3.jpg)'},children=[
    html.H1('Welcome to the Titanic, the Unsinkable Ship. Before we can let you board, we will need to ask you a few questions.',
            style={'textAlign': 'center',
                'color':  '#8B0000',
                'fontSize':50,
                'backgroundColor': colors['figure']}),
    html.Div(id='age',children=[
            html.H1('First, can you tell us how old you are?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Input(id='age_drop',placeholder='Enter Age',min=0,max=110,type='number',style={'width':'30%','fontSize':20},debounce=True)
    ],style={'textAlign': 'center'}),
    html.Div(id='gen_wrap',children=[
        html.Div(id='gender',children=[
            html.H2('Next, please tell us your gender.',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Dropdown(id='gender_drop',options=[{'label': 'Male', 'value': 0},
                                                   {'label': 'Female', 'value': 1},
                                                   {'label': 'Select Gender', 'value': 2}],value=2,style={'width':'30%','display':'inline-block','fontSize':20})
        ],style={'display':'none'})
    ]),
    html.Div(id='class_wrap',children=[
        html.Div(id='class',children=[
            html.H2('What class of travel have you booked?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Dropdown(id='class_drop',options=[{'label': '1st', 'value': 1},
                                                  {'label': '2nd', 'value': 2},
                                                  {'label': '3rd', 'value': 3},
                                                  {'label':'Select Class','value':4}],value=4,style={'width':'30%','display':'inline-block','fontSize':20})
        ],style={'display':'none'})
    ]),
    html.Div(id='embark_wrap',children=[
        html.Div(id='embark',children=[
            html.H2('What port are you boarding from?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Dropdown(id='em_drop',options=[{'label':'Southampton','value':0},
                                               {'label':'Cherbourg','value':1},
                                               {'label':'Queenstown','value':2},
                                               {'label':'Select Boarding Port','value':3}],value=3,style={'width':'30%','display':'inline-block','fontSize':20})
        ],style={'display':'none'})
    ]),
    html.Div(id='sp_wrap',children=[
        html.Div(id='sp',children=[
            html.H2('Are you travelling with your partner?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Dropdown(id='spouse',options=[{'label':'Yes','value':1},
                                              {'label':'No','value':0},                          
                                              {'label':'Yes or No','value':2} ],value=2,style={'width':'30%','display':'inline-block','fontSize':20})
        ],style={'display':'none'})
    ]),
    html.Div(id='sibs_wrap',children=[
        html.Div(id='sibs',children=[
            html.H2('How many brothers or sisters are travelling with you (if any)?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Input(id='sib',type='number',placeholder='Enter number of siblings',min=0,max=7,style={'width':'30%','display':'inline-block','fontSize':20},debounce=True)
        ],style={'display':'none'})
    ]),
    html.Div(id='pars_wrap',children=[
        html.Div(id='pars',children=[
            html.H2('Nearly finished, how many of your parents are travelling with you (if any)?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Input(id='par',type='number',placeholder='Enter number of parents',min=0,max=2,style={'width':'30%','display':'inline-block','fontSize':20},debounce=True)
        ],style={'display':'none'})
    ]),
    html.Div(id='chs_wrap',children=[
        html.Div(id='chs',children=[
            html.H2('Last Question, are you bringing your children? If so, how many?',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']}),
            dcc.Input(id='ch',type='number',placeholder='Enter number of children',min=0,max=7,style={'width':'30%','display':'inline-block','fontSize':20},debounce=True)
        ],style={'display':'none'})
    ]),
    html.Div(id='loading_wrap',children=[
        html.Div(id='loading',children=[
            html.H2('One minute as we prepare your ticket',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']})
        ],style={'display':'none'})
    ]),
    html.Br(),
    html.Div(id='loading2_wrap',children=[
        html.Div(id='loading2',children=[
            html.H2('Thank you and enjoy your journey',style={'textAlign': 'center','fontSize':20,'color':  '#8B0000','backgroundColor': colors['figure']})
        ],style={'display':'none'})
    ]),
    html.Div(id='outcome'
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br()
    
    
])
app.layout = serve_layout
#callback index
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return layout_tab_1
@app.callback([Output('gender','style'),
               Output('age','style')],
             [Input('age_drop','value')])
def gender_reveal(value):
    if value is not None:
        df['Age']=int(value)
        return {'display':True,'textAlign':'center','color':  '#8B0000'}, {'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('class','style'),
               Output('gen_wrap','style')],    
             [Input('gender_drop','value')])
def class_reveal(val):
    if val!=2:
        if val==0:
            df['gender']=1
        else:
            df['gender']=0
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('embark','style'),
               Output('class_wrap','style')],
             [Input('class_drop','value')])
def embark_reveal(val):
    if val!=4:
        if val==2:
            df['2nd']=1
            df['3rd']=0
        elif val==3:
            df['2nd']=0
            df['3rd']=1
        else:
            df['2nd']=0
            df['3rd']=0
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('sp','style'),
               Output('embark_wrap','style')],
             [Input('em_drop','value')])
def sp_reveal(val):
    if val!=3:
        if val==0:
            df['S']=1
            df['Q']=0
        elif val==2:
            df['S']=0
            df['Q']=1
        else:
            df['S']=0
            df['Q']=0
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('sibs','style'),
               Output('sp_wrap','style')],
             [Input('spouse','value')])
def sibs_reveal(val):
    if val!=2:
        if val==1:
            df['partner']=1
        else:
            df['partner']=0
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('pars','style'),
               Output('sibs_wrap','style')],
             [Input('sib','value')])
def pars_reveal(val):
    if val>-1:
        df['sibs']=int(val)
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('chs','style'),
               Output('pars_wrap','style')],
             [Input('par','value')])
def chs_reveal(val):
    if val>-1:
        df['par']=int(val)
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('loading','style'),
               Output('chs_wrap','style')],
             [Input('ch','value')])
def l_reveal(val):
    if val>-1:
        df['chil']=int(val)
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('loading2','style'),
               Output('loading_wrap','style')],
             [Input('ch','value')])
def l2_reveal(val):
    if val>-1:
        time.sleep(5)
        return {'display':True,'textAlign':'center','color':  '#8B0000'},{'display':'none'}
    else:
        return {'display':'none'},{'display':True,'textAlign': 'center'}
@app.callback([Output('main','style'),
               Output('loading2_wrap','style')],
             [Input('ch','value')])
def disp_reveal(val):
    if val>-1:
        time.sleep(8)
        return {'background-image':'url(https://upload.wikimedia.org/wikipedia/commons/6/6e/St%C3%B6wer_Titanic.jpg)'},{'display':'none'}
    else:
        return {'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RMS_Titanic_3.jpg/1024px-RMS_Titanic_3.jpg)'},{'display':True,'textAlign': 'center'}
@app.callback(Output('outcome','children'),
             [Input('ch','value')])
def out_reveal(val):
    if val>-1:
        time.sleep(8)
        df['parch']=df['par']+df['chil']
        df['sibsq']=df['partner']+df['sibs']
        ndf=df[['Age','sibsq','parch','2nd','3rd','Q','S','gender']]
        titanic=joblib.load('titanic.jlib')
        chance=round(titanic.predict_proba(ndf)[0][1],2)*100
        
        children=[html.H1('Of course, the Titanic never completed its maiden voyage',style={'textAlign':'center','color':  '#00FFFF','backgroundColor': '#000000'}),
                  html.Br(),
                  html.H1('Over 1500 people sadly lost their lives in one of the greatest maritime disasters of the 20th century',style={'textAlign':'center','color':  '#00FFFF','backgroundColor': '#000000'}),
                  html.Br(),
                  html.Br(),
                  html.H1('Based on your responses you would have had a ' + str(chance) +'% chance of surviving the disaster',style={'textAlign':'center','color':  '#00FFFF','backgroundColor': '#000000'}),
                  html.Br(),
                  html.H1("Below is a breakdown of some of the factors that would have affected someone's chances of survival",style={'textAlign':'center','color':  '#00FFFF','backgroundColor': '#000000'}),
                  html.Div(children=[
                      dcc.Graph(figure=go.Figure(data= go.Pie(title='Proportion of deaths by Gender',
                                 
                                  labels=['Male','Female'],
                                  values=[0.849,0.151],
                                  marker= {'colors': [
                                           'rgb(0, 204, 0)',  
                                           'rgb(255,255,0)']},
                                  textposition='inside'
                                 ),
                     layout={'paper_bgcolor':'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)',
                             'font':{'color':colors['text']}}
                     ),style={'display': 'inline-block', 
                              'width': '49%','height':'49%'
                                  }),
                      dcc.Graph(figure=go.Figure(data= go.Pie(title='Proportion of deaths by Class',
                                 
                                  labels=['1st','2nd','3rd'],
                                  values=[0.151,0.212,0.637],
                                  marker= {'colors': [
                                                 'rgb(0, 204, 0)',  
                                                 'rgb(215,11,11)', 
                                                 'rgb(255,255,0)']},
                                 textposition='inside'
                                 ),
                     layout={'paper_bgcolor':'rgba(0,0,0,0)',
                            "plot_bgcolor":'rgba(0,0,0,0)',
                             'font':{'color':colors['text']}}
                     ),style={'display': 'inline-block', 
                              'width': '49%','height':'49%'
                                  }
                    ),
                      dcc.Graph(figure={'data': [
                                {'x': ['0-10','11-20','21-30','31-40','41-50','51-60','61+'], 'y': [59,62,36,44,39,40,19], 'type': 'bar', 'name': 'Age'},
                                
                            ],
                            'layout': {
                                'title':'Chance of Survival by Age',
                                'paper_bgcolor':'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)',
                                'font': {
                                'color': colors['text']
                            }
                        }
                                  
                    },style={'display': 'inline-block', 
                             'width': '49%','height':'49%'
                                  }
                               ),
                      dcc.Graph(figure={'data': [
                                {'x': ['Southampton','Cherbourg','Queenstown'], 'y': [36,61,29], 'type': 'bar', 'name': 'Port'},
                                
                            ],
                            'layout': {
                                'title':'Chance of Survival per port',
                                'paper_bgcolor':'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)',
                                'font': {
                                'color': colors['text']
                            }
                        }
                                  
                    },style={'display': 'inline-block', 
                             'width': '49%','height':'49%'
                                  })
                      
                  ])
                                 
                 ]
        return children
    else:
        return {'display':'none'}


application=app.server
if __name__ == '__main__':
    application.run(debug=False,port=8080)