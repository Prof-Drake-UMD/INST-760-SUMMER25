import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load data
df = pd.read_csv("student_spending.csv")

# Categories to analyze
spend_cols = [
    'tuition', 'housing', 'food', 'transportation', 'books_supplies', 'entertainment',
    'personal_care', 'technology', 'health_wellness', 'miscellaneous'
]

# Create app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.H1("Student Spending Dashboard", className="my-4 text-center"),

    dbc.Row([
        dbc.Col([
            html.Label("Filter by Year"),
            dcc.Dropdown(
                options=[{'label': yr, 'value': yr} for yr in sorted(df['year_in_school'].unique())],
                value=None, placeholder="Select Year",
                id='year-filter'
            ),
        ], width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="total-spend"), width=6),
        dbc.Col(dcc.Graph(id="spend-frequency"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="per-student-costs"), width=6),
        dbc.Col(dcc.Graph(id="spending-by-year"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="value-per-dollar"), width=12),
    ]),
], fluid=True)

# Callbacks
@app.callback(
    Output("total-spend", "figure"),
    Output("spend-frequency", "figure"),
    Output("per-student-costs", "figure"),
    Output("spending-by-year", "figure"),
    Output("value-per-dollar", "figure"),
    Input("year-filter", "value")
)
def update_charts(selected_year):
    # Filter by year if selected
    filtered = df if not selected_year else df[df["year_in_school"] == selected_year]

    # Total Spend
    total_spend = filtered[spend_cols].sum().sort_values(ascending=False)
    fig1 = px.bar(
        x=total_spend.index, y=total_spend.values,
        title="Where the Money Goes",
        labels={'x': 'Category', 'y': 'Total Spend ($)'}
    )

    # Frequency
    freq = (filtered[spend_cols] > 0).sum().sort_values(ascending=False)
    fig2 = px.bar(
        x=freq.index, y=freq.values,
        title="Everyday Needs vs. One-Time Buys",
        labels={'x': 'Category', 'y': 'Number of Students Spending'}
    )

    # Per-Student Box Plot
    melted = filtered.melt(
        id_vars=['year_in_school'], 
        value_vars=spend_cols, 
        var_name='Category', 
        value_name='Amount'
    )
    fig3 = px.box(
        melted, x='Category', y='Amount',
        title="Biggest Per-Student Costs"
    )

    # Spending by Year
    by_year = df.groupby("year_in_school")[spend_cols].mean().T
    by_year = by_year.reset_index().melt(id_vars="index", var_name="Year", value_name="Average Spend ($)")
    fig4 = px.bar(
        by_year, x="index", y="Average Spend ($)", color="Year", barmode="group",
        title="Who Spends Differently?",
        labels={"index": "Category"}
    )

    # Value per Dollar (Bubble)
    avg_spend = filtered[spend_cols].mean()
    num_students = (filtered[spend_cols] > 0).sum()
    fig5 = px.scatter(
        x=avg_spend, y=num_students, size=avg_spend,
        color=avg_spend.index,
        labels={'x': 'Average Spend per Student ($)', 'y': 'Number of Students Spending'},
        title="What’s Worth It? - Value per Dollar"
    )

    return fig1, fig2, fig3, fig4, fig5

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

