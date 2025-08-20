from __future__ import annotations
import os
import pandas as pd
from typing import List, Tuple
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

base_path = os.path.join(os.path.dirname(__file__), "sp500")
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG'] 

# Load and Clean Data 
stock_data = []
for ticker in tickers:
    file_path = os.path.join(base_path, f"{ticker}.csv")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.replace('# ', '', regex=False)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    df.rename(columns={'Date': 'date'}, inplace=True)
    df['ticker'] = ticker
    stock_data.append(df)

# Combine and Pivot 
df_all = pd.concat(stock_data)
pivot_df = df_all.pivot(index='date', columns='ticker', values='Close')
AVAILABLE_TICKERS = list(pivot_df.columns) if not pivot_df.empty else tickers

# Time Slices
slides = {
    "Pre‑COVID (2015–2019)": ("2015-01-01", "2019-12-31"),
    "COVID Crash (Jan–Mar 2020)": ("2020-01-01", "2020-03-31"),
    "Recovery (Apr 2020–Dec 2021)": ("2020-04-01", "2021-12-31"),
    "Post‑COVID (2022–2023)": ("2022-01-01", "2023-12-31"),
}
growth_start = "2020-01-02"
growth_end = "2021-12-31"

def make_line_slice(pivot: pd.DataFrame, tickers: List[str], start: str, end: str) -> go.Figure:
    if pivot.empty:
        return go.Figure().update_layout(title="No data found. Check your sp500/ CSV files.")
    df = pivot.loc[start:end, tickers].dropna(how="all")
    if df.empty:
        return go.Figure().update_layout(title="No data in this date range.")
    fig = go.Figure()
    for col in df.columns:
        fig.add_traces(
            go.Scatter(
                x=df.index,
                y=df[col],
                mode="lines",
                name=col,
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Close= $%{y:.2f}<extra>%{fullData.name}</extra>",
            )
        )
    fig.update_layout(
        margin=dict(l=30, r=20, t=50, b=40),
        legend_title="Ticker",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Close ($)",
        template="plotly_white",
    )
    return fig


def make_growth_bar(pivot: pd.DataFrame, tickers: List[str], start: str, end: str, ascending: bool) -> Tuple[go.Figure, pd.DataFrame]:
    if pivot.empty:
        return go.Figure().update_layout(title="No data to compare."), pd.DataFrame(columns=["ticker", "growth_%"])    
    df = pivot[tickers].dropna(how="all")
    v0 = df.loc[df.index >= start].iloc[0]
    v1 = df.loc[df.index <= end].iloc[-1]
    growth = ((v1 - v0) / v0 * 100.0).dropna()
    table = growth.rename("growth_%").reset_index().rename(columns={"index": "ticker"}).sort_values("growth_%", ascending=ascending)
    fig = go.Figure(go.Bar(x=table["growth_%"], y=table["ticker"], orientation="h", hovertemplate="%{y}: %{x:.2f}%<extra></extra>"))
    fig.update_layout(margin=dict(l=60, r=20, t=50, b=40), template="plotly_white", xaxis_title=f"Growth % ({start} → {end})", yaxis_title="")
    return fig, table

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Interactive Tech Stocks Story Narrative"

sidebar = dbc.Card([
    html.H3("Filters & Controls", className="mb-2"),
    html.Label("Select tickers"),
    dcc.Dropdown(
        id="dd-tickers",
        options=[{"label": t, "value": t} for t in AVAILABLE_TICKERS],
        value=AVAILABLE_TICKERS,
        multi=True,
        clearable=False,
    ),
    html.Hr(),
    html.Label("Sort bars (Growth Comparison)"),
    dcc.Dropdown(
        id="dd-sort",
        options=[{"label": "Ascending", "value": "asc"}, {"label": "Descending", "value": "desc"}],
        value="desc",
        clearable=False,
    ),
    html.Hr(),
    html.Label("Toggle Slides"),
    dbc.Checklist(
        id="chk-sections",
        options=[
            {"label": "Slide 1: Pre‑COVID ", "value": "s1"},
            {"label": "Slide 2: COVID Crash ", "value": "s2"},
            {"label": "Slide 3: Recovery ", "value": "s3"},
            {"label": "Slide 4: Growth Comparison ", "value": "s4"},
            {"label": "Slide 5: Post‑COVID ", "value": "s5"},
        ],
        value=["s1", "s2", "s3", "s4", "s5"],
        className="mt-1",
    ),
], body=True, className="shadow-sm")

content = html.Div([
    html.H2("Tech Stocks: From Rise to Reset ", className="mb-1"),
    html.P("Interactive Narrative: Click, toggle, hover and sort. Explore the story your way.", className="text-muted"),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader("Slide 1 — The Rise of Tech Before the Storm (2015–2019)"), dbc.CardBody(dcc.Graph(id="fig-pre", config={"displaylogo": False}))], className="mb-3 shadow-sm"), md=12, id="card-s1")]),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader("Slide 2 — March 2020: The COVID Cliff (Jan–Mar 2020)"), dbc.CardBody(dcc.Graph(id="fig-crash", config={"displaylogo": False}))], className="mb-3 shadow-sm"), md=12, id="card-s2")]),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader("Slide 3 — Tech Bounces Back (Apr 2020–Dec 2021)"), dbc.CardBody(dcc.Graph(id="fig-recovery", config={"displaylogo": False}))], className="mb-3 shadow-sm"), md=12, id="card-s3")]),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader("Slide 4 — Not All Growth Was Equal (fixed period: Jan 2020 → Dec 2021)"), dbc.CardBody([dcc.Graph(id="fig-growth", config={"displaylogo": False}), html.Hr(), html.H6("Growth table (sortable)"), dash_table.DataTable(id="tbl-growth", style_as_list_view=True, sort_action="native", columns=[{"name": "Ticker", "id": "ticker"}, {"name": "Growth %", "id": "growth_%", "type": "numeric", "format": {"specifier": ".2f"}}], data=[], style_table={"overflowX": "auto"}, style_cell={"padding": "6px"})])], className="mb-3 shadow-sm"), md=12, id="card-s4")]),
    dbc.Row([dbc.Col(dbc.Card([dbc.CardHeader("Slide 5 — Post‑COVID: Stabilization or New Regime? (2022–2023)"), dbc.CardBody(dcc.Graph(id="fig-post", config={"displaylogo": False}))], className="mb-4 shadow-sm"), md=12, id="card-s5")]),
], className="px-2 px-md-3")

app.layout = dbc.Container([
    dbc.Row([dbc.Col(sidebar, md=3, sm=12), dbc.Col(content, md=9, sm=12)], className="gy-3 my-2"),
])

@callback(
    Output("fig-pre", "figure"),
    Output("fig-crash", "figure"),
    Output("fig-recovery", "figure"),
    Output("fig-post", "figure"),
    Input("dd-tickers", "value"),
)
def update_line_charts(tickers):
    selected = tickers or AVAILABLE_TICKERS
    pre = make_line_slice(pivot_df, selected, *slides["Pre‑COVID (2015–2019)"])
    crash = make_line_slice(pivot_df, selected, *slides["COVID Crash (Jan–Mar 2020)"])
    recov = make_line_slice(pivot_df, selected, *slides["Recovery (Apr 2020–Dec 2021)"])
    post = make_line_slice(pivot_df, selected, *slides["Post‑COVID (2022–2023)"])
    pre.update_layout(title="The Rise of Tech Before the Storm")
    crash.update_layout(title="March 2020: The COVID Cliff")
    recov.update_layout(title="Tech Bounces Back — Harder and Faster")
    post.update_layout(title="Have Tech Stocks Stabilized Post‑Pandemic?")
    return pre, crash, recov, post


@callback(
    Output("fig-growth", "figure"),
    Output("tbl-growth", "data"),
    Input("dd-tickers", "value"),
    Input("dd-sort", "value"),
)
def update_growth(tickers, sort_dir):
    selected = tickers or AVAILABLE_TICKERS
    ascending = (sort_dir == "asc")
    fig, table = make_growth_bar(pivot_df, selected, growth_start, growth_end, ascending)
    return fig, table.to_dict("records")


@callback(
    Output("card-s1", "style"),
    Output("card-s2", "style"),
    Output("card-s3", "style"),
    Output("card-s4", "style"),
    Output("card-s5", "style"),
    Input("chk-sections", "value"),
)
def toggle_sections(visible_keys: List[str]):
    visible = set(visible_keys or [])
    def sty(key):
        return {"display": "block"} if key in visible else {"display": "none"}
    return sty("s1"), sty("s2"), sty("s3"), sty("s4"), sty("s5")


if __name__ == "__main__":
    app.run(debug=True)
