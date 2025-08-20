# variables
# x = percent_low_income
# y = avg_test_score_percent	
# color = school type (Public, Private, or Charter)
# size = funding_per_student_usd 
# facets = grade level (Elementary, Middle, or High)

"""
tested in Google Colab
"""

import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px

df = pd.read_csv('education_inequality_data.csv')

# before plotting, need to filter for only NY
df = df.query("state=='New York'")

# clean out empty rows
df = df.dropna()


# plot using plotly instead of seaborn
fig = px.scatter(
    data_frame=df,
    x="percent_low_income",
    y="avg_test_score_percent",
    color="school_type", # point color based on school type
    size="funding_per_student_usd", # point size based on funding level
    facet_col="grade_level", # facet based on grade level 
    title="The Impact of Student Household Income on Student Test Scores in New York",
    # hover data add school name
    hover_data=["school_name"],    
)

# for changing background color
buttons_bg_color = [ 
    {'label': 'White',
     'method': 'relayout',
     'args': [{'plot_bgcolor': 'white'}]},
    {'label': 'Light Gray',
     'method': 'relayout',
     'args': [{'plot_bgcolor': 'lightgray'}]},
    {'label': 'Black',
     'method': 'relayout',
     'args': [{'plot_bgcolor': 'black'}]}
    ]


fig.update_layout(
    # buttons 
    {'updatemenus': [{'type': "buttons",
                     'direction': 'down',
                     'x':1.2,
                     'y': 0.5,
                     'showactive': True,
                     'active': 0,
                     'buttons': buttons_bg_color}]},
    showlegend = True,
    legend_title_text = "School Types",
    legend=dict(
        x=1.0, y=0.9
    )
)

# adjust axes
fig.update_yaxes(range=[0, 100])
fig.show()
