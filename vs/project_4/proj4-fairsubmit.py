import dash
import dash_bootstrap_components as dbc
from dash import dcc,Input, Output,html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


credit_card= pd.read_csv('Credit_Data_updated.csv')
credit_card["Number of Cards owned per person"]=credit_card["Number of Cards owned per person"].astype(str)





app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Income vs Credit Rating"), width=15, class_name='test1')
    ]),
    dcc.Dropdown(
        id="gender-filter",
        options=[{"label":gender,"value":gender} for gender in credit_card["Gender"].unique()],
        value=None,
        placeholder="Select a Gender"
    ),
    dbc.Row([
        dcc.Graph(id="incomevscreditrating")
    ])
    
    ])


#Create call back
@app.callback(
    Output('incomevscreditrating','figure'),
    Input('gender-filter','value')
)

def update_distribution(selected_gender):
    if selected_gender:
        filtered_df = credit_card[credit_card["Gender"]==selected_gender]
    else:
        filtered_df = credit_card
    
    if filtered_df.empty:
        return{}
    
    fig1=px.scatter(
        filtered_df,
        x='Annual Income(in thousands of dollars)',
        y='Credit Rating',
        color='Number of Cards owned per person',
        symbol='Gender',
        title='Income Distritbution by # of cards and Gender',
        symbol_sequence=["square","diamond"]
        
    )
    
    return fig1




  
if __name__=='__main__':
    app.run(debug=True)