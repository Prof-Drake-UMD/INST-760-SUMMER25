import dash
import dash_bootstrap_components as dbc
from dash import dcc,html,Input,Output
import plotly.express as px
import pandas as pd

ccard= pd.read_csv('Credit_Data_updated1.csv')

ccard["Number of Cards owned per person"]=ccard["Number of Cards owned per person"].astype(str)

num_records=len(ccard)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Financial Behavior Dashboard"),width=15,className="text-center my-5")

    ]),
    dbc.Row([
        dbc.Col(html.Div(f"Total Customer Records:{num_records}",className="text-center my-3 top-text"),
                width=7)
    ],className="mb-5"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Financial Behavior", className="card-title"),
                    dcc.Dropdown(
                        id="gender-filter1",
                        options=[{"label":gender,"value":gender} for gender in ccard["Gender"].unique()],
                        value=None,
                        placeholder="Select a Gender"
                    ),
                    dcc.Graph(id="scattergraph1")
                ])
            ])
        ],width=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Creditcard Demographics-Ethnicity", className="card-title"),
                    dcc.Dropdown(
                        id="ethnicity-filter",
                        options=[{"label":ethnicity,"value":ethnicity} for ethnicity in ccard["Ethnicity"].unique()],
                        value=None,
                        placeholder="Select one Ethnicity"
                    ),
                    dcc.Graph(id="linegraph2")

                ])
            ])
        ],width=7)
    ]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Creditcard Demographics-Gender", className="card-title"),
                dcc.Dropdown(
                        id="gender-filter2",
                        options=[{"label":gender,"value":gender} for gender in ccard["Gender"].unique()],
                        value=None,
                        placeholder="Select a Gender"
                    ),
                dcc.Graph(id="scattergraph3")
            ])
        ])
    ],width=12)
]),
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Creditcard Demographics-Education Status", className="card-title"),
                dcc.Dropdown(
                        id="gender-filter",
                        options=[{"label":gender,"value":gender} for gender in ccard["Gender"].unique()],
                        value=None,
                        placeholder="Select a Gender"
                    ),
                dcc.Slider(
                    id="Education-slider",
                    min=ccard["Number of years of Education"].min(),
                    max=ccard["Number of years of Education"].max(),
                    value=ccard["Number of years of Education"].median(),
                    marks={int(value): f"{int(value):,}" for value in ccard["Number of years of Education"].quantile([
                        0,0.25,0.5,0.75,1]).values},
                    step=1
                                
                    

                ),
                    dcc.Graph(id="scattergraph4")
            ])
        ])
    ],width=12)
]),


dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Creditcard Demographics-Marital Status & Ethnicity", className="card-title"),
                dcc.RadioItems(
                    id="chart-type",
                    options=[{"label":"Line-Ethnicity",'value':'line'},
                             {"label":"Bar-Ethnicity",'value':'bar'}],
                    value='line',
                    inline=True,
                    className='mb-4'

                ),
                dcc.Dropdown(
                    id='condition-filter',
                    options=[{'label':condition,'value':condition} for condition in ccard["Married"].unique()],
                    value=None,
                    placeholder="Select a Marital Status"
                ),
                dcc.Graph(
                    id="creditcard-demo"
                )
            ])
        ])
    ], width=12)
])



],fluid=True)

#Callback

@app.callback(
    Output('scattergraph1','figure'),
    Input('gender-filter1','value')
)

def update_distribution(selected_gender):
    if selected_gender:
        filtered_df1=ccard[ccard["Gender"]==selected_gender]
    else:
        filtered_df1 =ccard

    if filtered_df1.empty:
        return {}
    
    fig1 = px.scatter(
        filtered_df1,
        x="Credit Limit(individual credit card account)",
        y="Current Balance in credit card account",
        color="Gender",
        title="Customer's financial behavior"
        
    )
    return fig1

@app.callback(
    Output("linegraph2",'figure'),
    Input('ethnicity-filter','value')
)
def update_financialbehaviorethnicity(selected_ethnicity):
    if selected_ethnicity:
        filtered_df2=ccard[ccard["Ethnicity"]==selected_ethnicity]
    else:
        filtered_df2=ccard

    if filtered_df2.empty:
        return {}

    fig2 = px.bar(
                filtered_df2,
                x="Number of Cards owned per person",
                y="Credit Rating",
                color="Ethnicity",
                title="Financial Behavior-Ethnicity",
                color_discrete_sequence=(px.colors.qualitative.Set2)
                )
    return fig2    

@app.callback(
    Output("scattergraph3",'figure'),
    Input("gender-filter2",'value')
)

def update_financialbehaviornumberofcards(selected_gender):
    filtered_df3=ccard[ccard["Gender"]==selected_gender] 
    if selected_gender:
        filtered_df3=ccard[ccard["Gender"]==selected_gender]
    else:
        filtered_df3 =ccard

    if filtered_df3.empty:
        return {}
    
    fig3=px.scatter(
        filtered_df3,
        x="Credit Limit(individual credit card account)",
        y="Current Balance in credit card account",
        color="Student",
        title="Financial Behavior-Employment Status",
        color_discrete_sequence=(px.colors.qualitative.Set2)
    )
    return fig3

@app.callback(
    Output("scattergraph4",'figure'),
    [Input('gender-filter','value'),
     Input('Education-slider','value')]
)
def update_financialbehavioreducation(selected_gender,slider_value):
    filtered_df=ccard[ccard["Gender"]==selected_gender]
    if selected_gender:
        filtered_df=ccard[ccard["Gender"]==selected_gender]
    else:
        filtered_df =ccard

    if filtered_df.empty:
        return {}



    filtered_df=filtered_df[filtered_df['Number of years of Education']<= slider_value]

    fig4= px.scatter(filtered_df,
            x="Credit Limit(individual credit card account)",
            y="Current Balance in credit card account",
            title="Financial Behavior Gender and Years of Education")
    return fig4

@app.callback(
    Output('creditcard-demo','figure'),
    [Input('chart-type','value'),
    Input('condition-filter','value')]
)

def update_financialstatus(chart_type,selected_condition):
    filtered_df=ccard[ccard["Married"]==selected_condition]if selected_condition else ccard
    finance_df = filtered_df.groupby("Ethnicity").size().reset_index(name="Count")

    if chart_type == "line":
        fig = px.line(finance_df,
                      x="Ethnicity",
                      y= "Count",
                      title= "Financial behavior")
    else:
        fig = px.bar(finance_df,
                      x="Ethnicity",
                      y= "Count",
                      title= "Financial behavior")
        
    return fig




if __name__=='__main__':
    app.run(debug=True)












