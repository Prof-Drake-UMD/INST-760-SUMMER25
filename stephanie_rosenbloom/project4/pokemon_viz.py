import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load and preprocess data
df = pd.read_csv("Pokemon.csv")
df = df.dropna()
df['Legendary'] = df['Legendary'].astype(bool)

# Add alpha transparency based on Generation
gen_min, gen_max = df['Generation'].min(), df['Generation'].max()
df['alpha'] = 0.4 + 0.6 * (1 - (df['Generation'] - gen_min) / (gen_max - gen_min))

# Identify top 5 total Pokémon
df['Top5'] = df['Total'].rank(method='min', ascending=False) <= 5

# Add status column for shape mapping
def status_category(row):
    if row['Top5']:
        return 'Top 5'
    elif row['Legendary']:
        return 'Legendary'
    else:
        return 'Normal'

df['status'] = df.apply(status_category, axis=1)

# Create color map for Types
types = sorted(df['Type 1'].unique())
colors = px.colors.qualitative.Plotly
type_color_map = {t: colors[i % len(colors)] for i, t in enumerate(types)}

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    # Header
    html.H1("Pokémon Battle Stats Dashboard", 
            style={
                'textAlign': 'center',
                'marginBottom': '30px',
                'color': '#1e3a8a',
                'fontFamily': 'Arial, sans-serif'
            }),

    # Controls container - properly aligned
    html.Div([
        # Type filter section
        html.Div([
            html.Label("Filter by Type:", 
                      style={
                          'fontWeight': 'bold',
                          'marginBottom': '15px',
                          'display': 'block',
                          'color': '#1e3a8a'
                      }),
            dcc.Dropdown(
                options=[{'label': 'All Types', 'value': 'all'}] + 
                        [{'label': t, 'value': t} for t in types],
                value='all',
                id='type-filter',
                clearable=False,
                style={'marginBottom': '0', 'marginTop': '8px'}
            ),
        ], style={
            'flex': '0 0 280px',
            'minWidth': '280px',
            'padding': '20px',
            'backgroundColor': '#f0f8ff',
            'borderRadius': '8px',
            'border': '2px solid #1e3a8a'
        }),

        # Checklist section
        html.Div([
            html.Label("Display Options:", 
                      style={
                          'fontWeight': 'bold',
                          'marginBottom': '15px',
                          'display': 'block',
                          'color': '#1e3a8a'
                      }),
            dcc.Checklist(
                id='legendary-toggle',
                options=[
                    {'label': ' Show Legendary Pokémon', 'value': 'legendary'},
                    {'label': ' Show Top 5 Strongest Pokémon', 'value': 'top5'}
                ],
                value=['legendary', 'top5'],
                style={'lineHeight': '1.8', 'marginTop': '8px'}
            ),
        ], style={
            'flex': '1',
            'padding': '20px',
            'backgroundColor': '#f0f8ff',
            'borderRadius': '8px',
            'border': '2px solid #1e3a8a'
        }),
    ], style={
        'marginBottom': '20px',
        'width': '100%',
        'display': 'flex',
        'gap': '20px',
        'alignItems': 'flex-start'
    }),

    # Legend explanation - better aligned
    html.Div([
        html.P("● Normal   ★ Legendary   ■ Top 5 Strongest", 
               style={
                   'fontSize': '16px',
                   'fontStyle': 'italic',
                   'color': '#1e3a8a',
                   'textAlign': 'center',
                   'margin': '0',
                   'padding': '12px',
                   'backgroundColor': '#f0f8ff',
                   'borderRadius': '6px',
                   'border': '2px solid #1e3a8a'
               })
    ], style={'marginBottom': '20px'}),

    # Graph container
    html.Div([
        dcc.Graph(id='pokemon-scatter', style={'height': '700px'})
    ], style={
        'backgroundColor': 'white',
        'borderRadius': '8px',
        'border': '2px solid #1e3a8a',
        'padding': '10px'
    }),

], style={
    'padding': '30px',
    'maxWidth': '1200px',
    'margin': '0 auto',
    'backgroundColor': '#ffffff',
    'fontFamily': 'Arial, sans-serif'
})


@app.callback(
    Output('pokemon-scatter', 'figure'),
    Input('type-filter', 'value'),
    Input('legendary-toggle', 'value')
)
def update_graph(selected_type, toggle_vals):
    filtered_df = df.copy()

    if selected_type != 'all':
        filtered_df = filtered_df[filtered_df['Type 1'] == selected_type]

    if 'legendary' not in toggle_vals:
        filtered_df = filtered_df[~filtered_df['Legendary']]
    if 'top5' not in toggle_vals:
        filtered_df = filtered_df[~filtered_df['Top5']]

    # Symbol map for shapes
    symbol_map = {
        'Normal': 'circle',
        'Legendary': 'star',
        'Top 5': 'square'
    }

    fig = px.scatter(
        filtered_df,
        x='Attack',
        y='Defense',
        color='Type 1',
        size='Speed',
        symbol='status',
        symbol_map=symbol_map,
        color_discrete_map=type_color_map,
        hover_name='Name',
        opacity=filtered_df['alpha'],
        labels={'Attack': 'Attack', 'Defense': 'Defense'},
        title="Pokémon Battle Stats by Type, Speed, and Generation"
    )

    fig.update_traces(opacity=0.7)

    # Clean legend so colors aren't duplicated due to different symbols
    seen = set()
    for trace in fig.data:
        type_name = trace.name.split(",")[0]
        if type_name in seen:
            trace.showlegend = False
        else:
            trace.name = type_name
            seen.add(type_name)

        trace.hovertemplate = (
            "<b>%{hovertext}</b><br>" +
            "Attack: %{x}<br>" +
            "Defense: %{y}<br>" +
            "Speed: %{marker.size}<br>" +
            "Type: " + trace.name +
            "<extra></extra>"
        )

    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        legend_title_text='Pokémon Type',
        width=1100,
        height=700,
        margin=dict(l=80, r=80, t=100, b=80),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linewidth=1, linecolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linewidth=1, linecolor='lightgray'),  
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)