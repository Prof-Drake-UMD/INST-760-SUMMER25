import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Load and prepare data
df = pd.read_csv('2019.csv')

df.rename(columns={
    'Country or region': 'Country',
    'Score': 'Score',
    'GDP per capita': 'GDP per capita',
    'Social support': 'Social support',
    'Healthy life expectancy': 'Healthy life expectancy',
    'Freedom to make life choices': 'Freedom',
    'Generosity': 'Generosity',
    'Perceptions of corruption': 'Perceptions of corruption'
}, inplace=True)

# Define components and colors
core_factors = [
    'GDP per capita',
    'Social support', 
    'Healthy life expectancy',
    'Freedom',
    'Generosity',
    'Perceptions of corruption'
]

component_colors = {
    'GDP per capita': '#90AB86',
    'Social support': '#A1CEC5', 
    'Healthy life expectancy': '#F976D6',
    'Freedom': '#FAC390',
    'Generosity': '#4A9D93',
    'Perceptions of corruption': '#A1483D',
    'Residual': '#18605D',
    'Top Countries': '#4A9D93',
    'Others': '#A1483D'
}

# Calculate residual
df['Residual'] = df['Score'] - df[core_factors].sum(axis=1)
all_components = core_factors + ['Residual']

# Define component definitions for tooltips
component_definitions = {
    'GDP per capita': 'GDP per capita: Economic output per person - measures the standard of living and economic prosperity',
    'Social support': 'Social Support: Having someone to count on in times of need - reflects quality of social relationships',
    'Healthy life expectancy': 'Healthy Life Expectancy: Number of years a person can expect to live in good health',
    'Freedom': 'Freedom to Choose: Freedom to make life choices - satisfaction with freedom to choose what to do with your life',
    'Generosity': 'Generosity: Recent donations and charitable giving - reflects a culture of giving back',
    'Perceptions of corruption': 'Trust in Government: Perceived absence of corruption in government and business',
    'Residual': 'Unexplained Factors: Unexplained happiness - factors not captured by the other components'
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("World Happiness Report 2019", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '8px', 'fontSize': '2.2em', 'fontWeight': '600'}),
        html.P("What Makes a Nation Truly Happy? Discover the Factors That Create the World’s Happiest Societies",
               style={'textAlign': 'center', 'color': '#666', 'fontSize': '16px', 'maxWidth': '800px', 'margin': '0 auto', 'lineHeight': '1.4'})
    ], style={
        'background': 'white',
        'padding': '30px 20px',
        'marginBottom': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
    }),

    # ROW 1 SECTION HEADER
    html.Div([
        html.H2("Take a Broader Look", style={'textAlign': 'center', 'color': '#2c3e50', 'fontSize': '1.4em', 'marginBottom': '5px'}),
    ], style={'marginBottom': '20px'}),
    
    # ROW 1 FILTERS
    html.Div([
        html.Div([
            html.Label("Select a sample size", style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '14px'}),
            dcc.Dropdown(
                id='row1-top-n-dropdown',
                options=[
                    {'label': 'Top 5 Countries', 'value': 5},
                    {'label': 'Top 10 Countries', 'value': 10},
                    {'label': 'Top 15 Countries', 'value': 15},
                    {'label': 'Top 20 Countries', 'value': 20},
                    {'label': 'Top 30 Countries', 'value': 30}
                ],
                value=10,
                style={'width': '180px', 'fontSize': '14px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '15px', 'justifyContent': 'center'})
    ], style={
        'background': 'white',
        'padding': '15px',
        'marginBottom': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
    }),
    
    # ROW 1: Three panels
    html.Div([
        # GRAPH 1: Stacked Bar 
        html.Div([
            html.H3("Factors of Happiness", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '1.1em'}),
            dcc.Graph(id='stacked-bar-chart', style={'height': '550px'})
        ], style={
            'flex': '2',
            'background': 'white',
            'padding': '12px 5px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'marginRight': '10px'
        }),
        
        # COMPONENT TOGGLES
        html.Div([
            html.H4("Happiness Factors Filter", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '13px'}),
            html.P("Toggle happiness factors on/off", style={'textAlign': 'center', 'fontSize': '11px', 'color': '#666', 'marginBottom': '12px', 'lineHeight': '1.2'}),
            html.Div(id='component-toggles', style={'display': 'flex', 'flexDirection': 'column', 'gap': '3px'})
        ], style={
            'flex': '0.6',
            'background': 'white',
            'padding': '12px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'margin': '0 10px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'flex-start'
        }),
        
        # GRAPH 2: Scatter Plot
        html.Div([
            html.H3("Factor Correlation Analysis", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '1.1em'}),
            html.Div([
                html.Label("Factor vs Score:", style={'fontWeight': 'bold', 'marginBottom': '6px', 'display': 'block', 'fontSize': '13px'}),
                dcc.Dropdown(
                    id='scatter-component-dropdown',
                    options=[
                        {'label': 'View All Selected Factors', 'value': 'all'},
                        {'label': 'GDP vs Score', 'value': 'GDP per capita'},
                        {'label': 'Social Support vs Score', 'value': 'Social support'},
                        {'label': 'Life Expectancy vs Score', 'value': 'Healthy life expectancy'},
                        {'label': 'Freedom vs Score', 'value': 'Freedom'},
                        {'label': 'Generosity vs Score', 'value': 'Generosity'},
                        {'label': 'Corruption vs Score', 'value': 'Perceptions of corruption'}
                    ],
                    value='Social support',
                    style={'width': '100%', 'fontSize': '14px'}
                )
            ], style={'background': '#f8f9fa', 'padding': '8px', 'borderRadius': '8px', 'marginBottom': '8px'}),
            dcc.Graph(id='scatter-plot', style={'height': '550px'})
        ], style={
            'flex': '2',
            'background': 'white',
            'padding': '12px 5px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'marginLeft': '10px'
        })
    ], style={
        'display': 'flex',
        'gap': '0px',
        'marginBottom': '40px'
    }),

    # ROW 2 SECTION HEADER
    html.Div([
        html.H2("Take a Closer Look", style={'textAlign': 'center', 'color': '#2c3e50', 'fontSize': '1.4em', 'marginBottom': '5px'}),
    ], style={'marginBottom': '20px'}),
    
    # ROW 2 FILTERS
    html.Div([
        html.Div([
            html.Label("Select a country to see how it compares to global averages", style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '14px'}),
            dcc.Dropdown(
                id='country-dropdown',
                placeholder="Choose from top 30 countries...",
                style={'width': '280px', 'fontSize': '14px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '15px', 'justifyContent': 'center'})
    ], style={
        'background': 'white',
        'padding': '15px',
        'marginBottom': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
    }),
    
    # ROW 2: Three graphs
    html.Div([
        # Radar Chart
        html.Div([
            html.H3("Country Component Profile", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '1.1em'}),
            dcc.Graph(id='radar-chart', style={'height': '450px'})
        ], style={
            'flex': '1.2',
            'background': 'white',
            'padding': '12px 5px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'marginRight': '15px'
        }),
        
        # Country Data Chart
        html.Div([
            html.H3("Detailed Metrics", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '1.1em'}),
            html.Div(id='country-data-chart', style={'height': '430px', 'padding': '5px', 'overflowY': 'auto'})
        ], style={
            'flex': '0.8',
            'background': 'white',
            'padding': '12px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
            'marginRight': '15px'
        }),
        
        # Comparison Bar Chart
        html.Div([
            html.H3("Factor vs Averages", style={'textAlign': 'center', 'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '1.1em'}),
            html.Div([
                html.Label("Compare factor:", style={'fontWeight': 'bold', 'marginBottom': '6px', 'display': 'block', 'fontSize': '13px'}),
                dcc.Dropdown(
                    id='comparison-factor-dropdown',
                    options=[
                        {'label': 'Overall Happiness Score', 'value': 'Score'},
                        {'label': 'GDP per capita', 'value': 'GDP per capita'},
                        {'label': 'Social Support', 'value': 'Social support'},
                        {'label': 'Healthy Life Expectancy', 'value': 'Healthy life expectancy'},
                        {'label': 'Freedom', 'value': 'Freedom'},
                        {'label': 'Generosity', 'value': 'Generosity'},
                        {'label': 'Trust in Government', 'value': 'Perceptions of corruption'}
                    ],
                    value='Score',
                    style={'width': '100%', 'fontSize': '14px'}
                )
            ], style={'background': '#f8f9fa', 'padding': '8px', 'borderRadius': '8px', 'marginBottom': '8px'}),
            dcc.Graph(id='comparison-bar-chart', style={'height': '450px'})
        ], style={
            'flex': '1.2',
            'background': 'white',
            'padding': '12px 5px',
            'borderRadius': '12px',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
        })
    ], style={
        'display': 'flex',
        'gap': '0px',
        'marginBottom': '30px'
    }),
    
    # Store for component selection state
    dcc.Store(id='selected-components', data=all_components)
    
], style={
    'fontFamily': 'Helvetica',
    'margin': '0 auto',
    'maxWidth': '1600px',
    'padding': '20px',
    'backgroundColor': '#f5f5f5'
})

# Add CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
                font-family: Helvetica;
            }
            .toggle-button {
                display: inline-block;
                padding: 6px 12px;
                margin: 3px;
                border-radius: 15px;
                cursor: pointer;
                font-weight: bold;
                border: 2px solid;
                transition: all 0.3s ease;
                font-size: 12px;
                font-family: Helvetica;
            }
            .toggle-button:hover {
                opacity: 0.8;
                transform: scale(1.05);
            }
            .data-table {
                font-family: Helvetica;
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
                font-size: 14px;
                border: 2px solid #ddd;
            }
            .data-table td, .data-table th {
                border: 1px solid #ddd;
                padding: 12px 15px;
                text-align: left;
            }
            .data-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .data-table tr:hover {
                background-color: #f5f5f5;
            }
            .data-table th {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            .data-table td:first-child {
                font-weight: bold;
                background-color: #e8f5e8;
                color: #2c3e50;
            }
            .data-table td:last-child {
                text-align: center;
                font-weight: 600;
                color: #2c3e50;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to populate country dropdown with top 30 countries
@app.callback(
    Output('country-dropdown', 'options'),
    Input('row1-top-n-dropdown', 'value')
)
def update_country_dropdown(top_n):
    top_30_countries = df.nlargest(30, 'Score')
    return [{'label': f"#{i+1} {country}", 'value': country} 
            for i, country in enumerate(top_30_countries['Country'])]

# Callback to create component toggle buttons
@app.callback(
    Output('component-toggles', 'children'),
    Input('selected-components', 'data')
)
def create_component_toggles(selected_components):
    buttons = []
    for component in all_components:
        is_selected = component in selected_components
        button_style = {
            'backgroundColor': component_colors[component] if is_selected else 'white',
            'color': 'white' if is_selected else component_colors[component],
            'borderColor': component_colors[component]
        }
        
        definition = component_definitions.get(component, '')
        
        buttons.append(
            html.Button(
                component.replace('Perceptions of corruption', 'Corruption'),
                id={'type': 'component-toggle', 'index': component},
                className='toggle-button',
                style=button_style,
                title=definition
            )
        )
    
    return buttons

# Callback to handle component toggle
@app.callback(
    Output('selected-components', 'data'),
    [Input({'type': 'component-toggle', 'index': dash.ALL}, 'n_clicks')],
    [State('selected-components', 'data')]
)
def toggle_component(n_clicks, selected_components):
    ctx = callback_context
    if not ctx.triggered:
        return selected_components
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    component = eval(button_id)['index']
    
    if component in selected_components:
        selected_components.remove(component)
    else:
        selected_components.append(component)
    
    return selected_components

# Callback for ROW 1 - Stacked Bar Chart
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('row1-top-n-dropdown', 'value'),
     Input('selected-components', 'data')]
)
def update_stacked_bar_chart(top_n, selected_components):
    top_countries = df.nlargest(top_n, 'Score')
    
    fig = go.Figure()
    
    for component in selected_components:
        if component in top_countries.columns:
            fig.add_trace(go.Bar(
                name=component.replace('Perceptions of corruption', 'Corruption'),
                x=top_countries['Country'],
                y=top_countries[component],
                marker_color=component_colors[component]
            ))
    
    fig.update_layout(
        barmode='stack',
        title="",
        xaxis_title="Country",
        yaxis_title="Score Component Value",
        xaxis_tickangle=-45,
        height=550,
        margin=dict(t=60, b=80, l=80, r=60),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1,
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1,
            showgrid=True
        )
    )
    
    return fig

# Callback for ROW 1 - Scatter Plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('row1-top-n-dropdown', 'value'),
     Input('scatter-component-dropdown', 'value'),
     Input('selected-components', 'data')]
)
def update_scatter_plot(top_n, component, selected_components):
    top_countries = df.nlargest(top_n, 'Score')
    top_countries_list = top_countries['Country'].tolist()
    other_countries = df[~df['Country'].isin(top_countries_list)]
    
    fig = go.Figure()
    
    if component == 'all':
        for comp in selected_components:
            if comp in core_factors:
                fig.add_trace(go.Scatter(
                    x=top_countries[comp],
                    y=top_countries['Score'],
                    mode='markers',
                    name=comp.replace('Perceptions of corruption', 'Corruption'),
                    marker=dict(color=component_colors[comp], size=10, opacity=0.8),
                    text=top_countries['Country'],
                    hovertemplate='<b>%{text}</b><br>' + 
                                 f'{comp}: %{{x:.3f}}<br>' +
                                 'Happiness Score: %{y:.3f}<extra></extra>'
                ))
    else:
        fig.add_trace(go.Scatter(
            x=other_countries[component],
            y=other_countries['Score'],
            mode='markers',
            name='Other Countries',
            marker=dict(color=component_colors['Others'], size=6, opacity=0.4),
            text=other_countries['Country'],
            hovertemplate='<b>%{text}</b><br>' + 
                         f'{component}: %{{x:.3f}}<br>' +
                         'Happiness Score: %{y:.3f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=top_countries[component],
            y=top_countries['Score'],
            mode='markers',
            name=f'Top {top_n}',
            marker=dict(color=component_colors['Top Countries'], size=12),
            text=top_countries['Country'],
            hovertemplate='<b>%{text}</b><br>' + 
                         f'{component}: %{{x:.3f}}<br>' +
                         'Happiness Score: %{y:.3f}<extra></extra>'
        ))
        
        x_vals = df[component].dropna()
        y_vals = df['Score'][df[component].notna()]
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode='lines',
            name='Trend Line',
            line=dict(color='#FF6B6B', width=3, dash='dash'),
            hoverinfo='skip'
        ))
    
    title = f"Selected Factors vs Score (Top {top_n})" if component == 'all' else f"{component} vs Happiness Score"
    x_title = "Factor Values" if component == 'all' else component
    
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title="Happiness Score",
        height=550,
        hovermode='closest',
        margin=dict(t=80, b=100, l=80, r=60),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False if component == 'all' else True,
        legend=dict(
            orientation="h",
            yanchor="bottom", 
            y=-0.25,
            xanchor="center",
            x=0.5
        ) if component != 'all' else None,
        xaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1,
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1,
            showgrid=True
        )
    )
    
    return fig

# Callback for ROW 2 - Radar Chart
@app.callback(
    Output('radar-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_radar_chart(selected_country):
    if not selected_country:
        fig = go.Figure()
        fig.add_annotation(
            text="Select a country to see its profile",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=450,
            margin=dict(t=60, b=40, l=40, r=40),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig
    
    country_data = df[df['Country'] == selected_country].iloc[0]
    
    categories = [comp.replace('Perceptions of corruption', 'Corruption') for comp in core_factors]
    values = [country_data[comp] for comp in core_factors]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(108, 198, 164, 0.3)',
        line=dict(color=component_colors['Top Countries'], width=3),
        name=selected_country
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2] if values else [0, 2],
                gridcolor='#f0f0f0',
                gridwidth=1,
                tickangle=0,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                gridcolor='#f0f0f0',
                gridwidth=1,
                tickfont=dict(size=11)
            ),
            bgcolor='white'
        ),
        title=f"{selected_country}",
        height=450,
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# Callback for ROW 2 - Country Data Chart
@app.callback(
    Output('country-data-chart', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_data_chart(selected_country):
    if not selected_country:
        return html.Div([
            html.Div("Select a country to see detailed data", 
                   style={
                       'textAlign': 'center', 
                       'padding': '40px', 
                       'color': 'gray', 
                       'fontSize': '14px',
                       'border': '2px dashed #ddd',
                       'borderRadius': '8px',
                       'backgroundColor': '#f9f9f9'
                   })
        ])
    
    country_data = df[df['Country'] == selected_country].iloc[0]
    rank = df[df['Score'] >= country_data['Score']].shape[0]
    
    data_items = [
        {'label': 'Rank', 'value': f"#{rank}", 'color': '#e74c3c'},
        {'label': 'Score', 'value': f"{country_data['Score']:.3f}", 'color': '#2ecc71'},
        {'label': 'GDP', 'value': f"{country_data['GDP per capita']:.3f}", 'color': '#3498db'},
        {'label': 'Social', 'value': f"{country_data['Social support']:.3f}", 'color': '#9b59b6'},
        {'label': 'Health', 'value': f"{country_data['Healthy life expectancy']:.3f}", 'color': '#f39c12'},
        {'label': 'Freedom', 'value': f"{country_data['Freedom']:.3f}", 'color': '#1abc9c'},
        {'label': 'Generosity', 'value': f"{country_data['Generosity']:.3f}", 'color': '#e67e22'},
        {'label': 'Corruption', 'value': f"{country_data['Perceptions of corruption']:.3f}", 'color': '#95a5a6'}
    ]
    
    data_rows = []
    for item in data_items:
        data_rows.append(
            html.Div([
                html.Div(item['label'], style={
                    'fontWeight': 'bold',
                    'padding': '8px 10px',
                    'backgroundColor': '#f8f9fa',
                    'borderBottom': '1px solid #dee2e6',
                    'borderRight': '1px solid #dee2e6',
                    'width': '55%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'fontSize': '13px'
                }),
                html.Div(item['value'], style={
                    'padding': '8px 10px',
                    'backgroundColor': 'white',
                    'borderBottom': '1px solid #dee2e6',
                    'width': '45%',
                    'display': 'inline-block',
                    'textAlign': 'center',
                    'fontWeight': '600',
                    'color': item['color'],
                    'fontSize': '13px'
                })
            ], style={
                'border': '1px solid #dee2e6',
                'marginBottom': '1px',
                'borderRadius': '2px',
                'overflow': 'hidden'
            })
        )
    
    return html.Div([
        html.H4(f"{selected_country}", 
               style={
                   'textAlign': 'center', 
                   'marginBottom': '12px', 
                   'color': '#2c3e50',
                   'padding': '8px',
                   'backgroundColor': '#e8f4fd',
                   'border': '2px solid #3498db',
                   'borderRadius': '6px',
                   'fontSize': '16px'
               }),
        html.Div(data_rows, style={
            'border': '2px solid #dee2e6',
            'borderRadius': '6px',
            'overflow': 'hidden',
            'backgroundColor': 'white'
        })
    ])

# Callback for ROW 2 - Comparison Bar Chart
@app.callback(
    Output('comparison-bar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('comparison-factor-dropdown', 'value')]
)
def update_comparison_bar_chart(selected_country, selected_factor):
    if not selected_country:
        fig = go.Figure()
        fig.add_annotation(
            text="Select a country for comparison",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=450,
            margin=dict(t=60, b=60, l=60, r=40),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig
    
    country_data = df[df['Country'] == selected_country].iloc[0]
    global_avg = df[selected_factor].mean()
    top10_avg = df.nlargest(10, 'Score')[selected_factor].mean()
    bottom10_avg = df.nsmallest(10, 'Score')[selected_factor].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[selected_country, 'Global Avg', 'Top 10 Avg', 'Bottom 10 Avg'],
        y=[country_data[selected_factor], global_avg, top10_avg, bottom10_avg],
        marker_color=[component_colors['Top Countries'], 
                     component_colors['Others'], 
                     '#3498db',
                     '#e74c3c'],
        text=[f"{val:.3f}" for val in [country_data[selected_factor], global_avg, top10_avg, bottom10_avg]],
        textposition='auto'
    ))
    
    # Dynamic title based on selected factor
    factor_display = selected_factor if selected_factor == 'Score' else selected_factor
    
    fig.update_layout(
        title=f"{factor_display} Comparison",
        yaxis_title=factor_display,
        height=450,
        showlegend=False,
        margin=dict(t=60, b=60, l=60, r=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            gridwidth=1
        )
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)