# app.py
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np

# ---------------- LOAD DATA ----------------
# Use the correct path to the CSV file
df = pd.read_csv("StudentsPerformance.csv")



df = df.dropna(subset=[
    "math score", "reading score", "writing score",
    "gender", "race/ethnicity", "test preparation course"
])

# Score bounds for sliders
M_MIN, M_MAX = int(df["math score"].min()), int(df["math score"].max())
R_MIN, R_MAX = int(df["reading score"].min()), int(df["reading score"].max())

# ---------------- APP ----------------
app = Dash(__name__)
app.title = "Project 2 — Interactive (Students Performance)"

symbol_map = {"female": "circle", "male": "square"}

app.layout = html.Div(
    style={"maxWidth": "1200px", "margin": "0 auto", "padding": "16px"},
    children=[
        html.H2("Multidimensional Student Performance — Interactive"),
        html.P("An interactive recreation of your Project 2 plot with filters and controls."),

        # Controls
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "12px"},
            children=[
                html.Div([
                    html.Label("Race/Ethnicity"),
                    dcc.Dropdown(
                        id="race-filter",
                        options=[{"label": r, "value": r} for r in sorted(df["race/ethnicity"].unique())],
                        value=sorted(df["race/ethnicity"].unique()),
                        multi=True,
                    ),
                ]),
                html.Div([
                    html.Label("Test Preparation"),
                    dcc.Checklist(
                        id="prep-filter",
                        options=[{"label": v, "value": v} for v in df["test preparation course"].unique()],
                        value=list(df["test preparation course"].unique()),
                        style={"marginTop": "6px"},
                    ),
                ]),
                html.Div([
                    html.Label("Gender"),
                    dcc.Checklist(
                        id="gender-filter",
                        options=[{"label": v.title(), "value": v} for v in df["gender"].unique()],
                        value=list(df["gender"].unique()),
                        style={"marginTop": "6px"},
                    ),
                ]),
            ],
        ),

        html.Div(style={"height": "12px"}),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "2fr 2fr 1fr", "gap": "12px"},
            children=[
                html.Div([
                    html.Label("Math score range"),
                    dcc.RangeSlider(
                        id="math-range",
                        min=M_MIN, max=M_MAX, step=1, value=[M_MIN, M_MAX],
                        marks={M_MIN: str(M_MIN), M_MAX: str(M_MAX)}
                    ),
                ]),
                html.Div([
                    html.Label("Reading score range"),
                    dcc.RangeSlider(
                        id="read-range",
                        min=R_MIN, max=R_MAX, step=1, value=[R_MIN, R_MAX],
                        marks={R_MIN: str(R_MIN), R_MAX: str(R_MAX)}
                    ),
                ]),
                html.Div([
                    html.Label("Point size (max)"),
                    dcc.Slider(
                        id="size-max",
                        min=80, max=400, step=10, value=300,
                        marks={80:"80", 200:"200", 300:"300", 400:"400"}
                    ),
                ]),
            ],
        ),

        html.Div(style={"height": "12px"}),

        dcc.Graph(id="facet-scatter", config={"displaylogo": False}),

        html.Div(
            "Tip: drag to zoom, double‑click to reset; click legend items to toggle groups; box/lasso select from the toolbar.",
            style={"fontSize": "12px", "color": "#666", "marginTop": "6px"}
        ),
    ],
)

@app.callback(
    Output("facet-scatter", "figure"),
    [
        Input("race-filter", "value"),
        Input("prep-filter", "value"),
        Input("gender-filter", "value"),
        Input("math-range", "value"),
        Input("read-range", "value"),
        Input("size-max", "value"),
    ],
)
def update_plot(races, preps, genders, math_rng, read_rng, size_max):
    # Filter
    m = df.copy()
    if races:
        m = m[m["race/ethnicity"].isin(races)]
    if preps:
        m = m[m["test preparation course"].isin(preps)]
    if genders:
        m = m[m["gender"].isin(genders)]
    if math_rng:
        m = m[(m["math score"] >= math_rng[0]) & (m["math score"] <= math_rng[1])]
    if read_rng:
        m = m[(m["reading score"] >= read_rng[0]) & (m["reading score"] <= read_rng[1])]

    if m.empty:
        return px.scatter(title="No data for the selected filters.")

    # Keep facet order tidy
    category_orders = {"race/ethnicity": sorted(m["race/ethnicity"].unique())}

    fig = px.scatter(
        m,
        x="math score",
        y="reading score",
        color="test preparation course",
        symbol="gender",
        symbol_map=symbol_map,
        size="writing score",
        size_max=size_max,   # interactive scaling
        facet_col="race/ethnicity",
        facet_col_wrap=3,
        category_orders=category_orders,
        hover_data={
            "math score": ":.0f",
            "reading score": ":.0f",
            "writing score": ":.0f",
            "gender": True,
            "test preparation course": True,
            "race/ethnicity": False,  # already shown in facet title
        },
        labels={
            "math score": "Math Score",
            "reading score": "Reading Score",
            "test preparation course": "Test Prep",
            "gender": "Gender",
        },
        title="Multidimensional Student Performance Analysis",
    )

    # Layout polish (mirrors your seaborn look, but interactive)
    fig.update_layout(
        margin=dict(l=10, r=10, t=60, b=10),
        legend_title_text="Test Prep",
    )
    # Lock axes to full 0–100 (common for these datasets), but keep zoomable
    fig.update_xaxes(range=[0, 100], matches=None)
    fig.update_yaxes(range=[0, 100], matches=None)

    return fig

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5500)


