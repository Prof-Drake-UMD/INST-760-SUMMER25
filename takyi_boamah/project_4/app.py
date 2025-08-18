import math
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

df = pd.read_csv("Iris.csv")

df["petal_width_bin"] = pd.cut(
    df["PetalWidthCm"],
    bins=[0, 0.5, 1, 1.5, 2.5],
    labels=["Thin", "Medium", "Thick", "Very Thick"],
    include_lowest=True
)

species_list = sorted(df["Species"].unique())
bin_list = ["Thin", "Medium", "Thick", "Very Thick"]

def slider_marks(vmin, vmax, step=1.0, fmt="{:.0f}"):
    ticks = np.arange(math.floor(vmin), math.ceil(vmax) + 1e-9, step)
    return {float(t): fmt.format(t) for t in ticks}

def make_fig(data):
    fig = px.scatter(
        data,
        x="SepalLengthCm",
        y="SepalWidthCm",
        color="Species",
        symbol="petal_width_bin",
        size="PetalLengthCm",
        size_max=20,
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
            "SepalLengthCm": "Sepal Length (cm)",
            "SepalWidthCm": "Sepal Width (cm)",
            "petal_width_bin": "Petal Thickness",
            "PetalLengthCm": "Petal Length (cm)"
        },
        title="Iris Flower Characteristics by Species, Petal & Sepal Attributes"
    )
    fig.update_traces(marker=dict(line=dict(width=0.7, color="black")), opacity=0.85)
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20), plot_bgcolor="white")
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.1)")
    return fig

app = Dash(__name__)
app.title = "Iris Interactive Dashboard"

app.layout = html.Div(
    style={"display": "flex", "gap": "16px", "padding": "12px"},
    children=[
        # Controls
        html.Div(
            style={"minWidth": "260px"},
            children=[
                html.H3("Filters"),
                html.Label("Species"),
                dcc.Dropdown(
                    id="species",
                    options=[{"label": s, "value": s} for s in species_list],
                    value=species_list, multi=True, clearable=False
                ),
                html.Br(),
                html.Label("Petal Thickness (bins)"),
                dcc.Checklist(
                    id="bins",
                    options=[{"label": b, "value": b} for b in bin_list],
                    value=bin_list, inline=False
                ),
                html.Br(),
                html.Label("Sepal Length (cm)"),
                dcc.RangeSlider(
                    id="sl_range",
                    min=float(df["SepalLengthCm"].min()),
                    max=float(df["SepalLengthCm"].max()),
                    value=[float(df["SepalLengthCm"].min()), float(df["SepalLengthCm"].max())],
                    step=0.1,
                    marks=slider_marks(df["SepalLengthCm"].min(), df["SepalLengthCm"].max(), step=1.0),
                    updatemode="mouseup",
                    tooltip={"always_visible": False, "placement": "bottom"}
                ),
                html.Br(),
                html.Label("Petal Length (cm) — controls point size"),
                dcc.RangeSlider(
                    id="pl_range",
                    min=float(df["PetalLengthCm"].min()),
                    max=float(df["PetalLengthCm"].max()),
                    value=[float(df["PetalLengthCm"].min()), float(df["PetalLengthCm"].max())],
                    step=0.1,
                    marks=slider_marks(df["PetalLengthCm"].min(), df["PetalLengthCm"].max(), step=1.0),
                    updatemode="mouseup",
                    tooltip={"always_visible": False, "placement": "bottom"}
                ),
            ],
        ),
        # Plot
        html.Div(
            style={"flex": 1},
            children=[
                dcc.Graph(
                    id="plot",
                    figure=make_fig(df),
                    style={"height": "80vh"},
                    config={"displaylogo": False, "responsive": True}
                )
            ],
        ),
    ],
)

@callback(
    Output("plot", "figure"),
    Input("species", "value"),
    Input("bins", "value"),
    Input("sl_range", "value"),
    Input("pl_range", "value"),
)
def update_plot(species_sel, bins_sel, sl_rng, pl_rng):
    m = (
        df["Species"].isin(species_sel)
        & df["petal_width_bin"].astype(str).isin(bins_sel)
        & df["SepalLengthCm"].between(sl_rng[0], sl_rng[1])
        & df["PetalLengthCm"].between(pl_rng[0], pl_rng[1])
    )
    return make_fig(df[m])

if __name__ == "__main__":
    app.run(debug=True)
