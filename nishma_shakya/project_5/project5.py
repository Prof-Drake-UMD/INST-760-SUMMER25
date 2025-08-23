"""
tested in google colab, had to install dash
"""

# imports
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from dash import Dash, dcc, html, Input, Output

# dataframe from csv
df = pd.read_csv("teen_phone_addiction_dataset.csv")

"""
Story: Students are becoming addiction to their phones
"""

# plots in plotly

# plot 1: stacked bar (time on social, time on education, time on games BY age groups)
# get the 3 columns
activity_columns = ['Time_on_Social_Media', 'Time_on_Gaming', 'Time_on_Education']
# group by age
df_age_activities = df.groupby('Age')[activity_columns].mean().reset_index()

# df_age_activities.head()

# create figure
fig1 = go.Figure()
# add traces fro each column/cat (bars)
fig1.add_trace(go.Bar(
    x=df_age_activities['Age'],
    y=df_age_activities['Time_on_Social_Media'],
    name='Social Media'
))
fig1.add_trace(go.Bar(
    x=df_age_activities['Age'],
    y=df_age_activities['Time_on_Gaming'],
    name='Gaming'
))
fig1.add_trace(go.Bar(
    x=df_age_activities['Age'],
    y=df_age_activities['Time_on_Education'],
    name='Education'
))
# update layout... barmode, title, labels, etc.
fig1.update_layout(
    barmode='stack',
    title='How Teens Spend Their Phone Time',
    xaxis_title='Age',
    yaxis_title='Average Hours per Day',
    legend_title='Activity Type',
    legend=dict(orientation='h', y=1.15, x=0.5)
)
# fig1.show()

# plot 2: scatter plot (more addicted = checking phone more) with linear regression line (to show trend)
fig2 = px.scatter(
    data_frame=df,
    x="Phone_Checks_Per_Day",
    y="Addiction_Level",
    opacity=0.4,
    trendline="ols",  # regression line
    trendline_color_override="red", # make it red
    labels={
        "Phone_Checks_Per_Day": "Number of Phone Checks Per Day",
        "Addiction_Level": "Addiction Level (scale 1-10)"
    },
    title="Addiction Level Increases with Phone Checks"
)

# fig2.show()

# plot 3: scatter plot (addiction affects sleep)
fig3 = px.scatter(
    data_frame=df,
    x="Addiction_Level",
    y="Sleep_Hours",
    opacity=0.4,
    trendline="ols",  # trendline
    trendline_color_override="red", # make it red
    labels={
        "Addiction_Level": "Addiction Level",
        "Sleep_Hours": "Average Sleep Time (hours)"
    },
    title="Higher Addiction Leads to Less Sleep"
)

# fig3.show()

# plot 4: box plot (addiction level vs education time)
# make it rounded so no decimals
df['Addiction_Level_Round'] = df['Addiction_Level'].round().astype(int)
fig4 = px.box(
    data_frame=df,
    x='Addiction_Level_Round',
    y='Apps_Used_Daily',
    labels={
        'Addiction_Level_Round': 'Addiction Level (rounded)',
        'Apps_Used_Daily': 'Number of Apps Used Daily'
    },
    title='Addiction Increases the Apps Used Daily'
)

# fig4.show()

# plot 5: scatter plot (more addicted = more phone use)
fig5 = px.scatter(
    data_frame=df,
    x="Addiction_Level",
    y="Daily_Usage_Hours",
    opacity=0.4,
    trendline="ols",  # trendline
    trendline_color_override="red",
    labels={
        "Addiction_Level": "Addiction Level (1-10)",
        "Daily_Usage_Hours": "Daily Phone Usage (hours)"
    },
    title="Higher Addiction Level Leads to More Daily Phone Usage"
)

# fig5.show()

# dashboard!!
app = Dash()

# for age dropdown
age_options = [{"label": str(a), "value": a} for a in sorted(df['Age'].unique())]

app.layout = [
    # overall div that contains everything
    html.Div(
        style={"background-color": "white", "display": "flex", "flex-direction": "column", "justifyContent": "space-between"},
        # going to use flexbox to make it easier for layout
        children=[
            # title
            html.H1("Teen Phone Addiction", style={"backgroundColor": "white", "padding": "10px"}),
            # grpah 1
            html.Div(
                style={"padding": "10px", "bottom-margin": "10px", "display": "flex", "flex-direction": "column"},
                children=[
                    # grpah 1
                    dcc.Graph(id="fig1", figure=fig1),
                    # dropdwon and label
                    html.Div(
                        style={"padding-left": "70px"},
                        children=[
                            # dropdown for age for grpah 1
                            html.Label("Select Age(s):"),
                            dcc.Dropdown(
                              id="age-dropdown", # to reference in callback
                              options=age_options,  # defined it above
                              value=[a["value"] for a in age_options],  # default = all ages
                              multi=True, # allow multiple options
                              style={"width": "80%", "min-width": "200px"}
                            ),
                        ]
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            # put grpah 2 and 3 in same row (scatter plots)
            html.Div(
                style={"display": "flex", "align-items": "center", "justifyContent": "space-between", "width": "100%"},
                children=[
                    dcc.Graph(id="fig2", figure=fig2, style={"width": "48%"}),
                    dcc.Graph(id="fig3", figure=fig3, style={"width": "48%"}),
                ]
            ),
            # grpah 4
            dcc.Graph(id="fig4", figure=fig4, style={"width": "80%"}),
            # grpah 5
            dcc.Graph(id="fig5", figure=fig5, style={"width": "80%"})
        ]
    ),
]

if __name__ == '__main__':
    app.run(debug=True)


# callback: click value in dropdown --> change figure (fig1)
@app.callback(
    Output("fig1", "figure"),
    Input("age-dropdown", "value")
)
# trigger function: get the ages that are selected in dropdown, and recreate figure based on that
def update_graphs(selected_ages):
    # filter df based on selected ages
    filtered_df = df[df["Age"].isin(selected_ages)]
    # recreate fig1 (just same code from aboce)
    activity_columns = ['Time_on_Social_Media', 'Time_on_Gaming', 'Time_on_Education']
    df_age_activities = filtered_df.groupby('Age')[activity_columns].mean().reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df_age_activities['Age'], y=df_age_activities['Time_on_Social_Media'], name='Social Media'))
    fig1.add_trace(go.Bar(x=df_age_activities['Age'], y=df_age_activities['Time_on_Gaming'], name='Gaming'))
    fig1.add_trace(go.Bar(x=df_age_activities['Age'], y=df_age_activities['Time_on_Education'], name='Education'))
    fig1.update_layout(barmode='stack', title='How Teens Spend Their Phone Time', xaxis_title='Age', yaxis_title='Average Hours per Day', legend_title='Activity Type', legend=dict(orientation='h', y=1.15, x=0.5))

    return fig1
