import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

component_colors_all = {
    'GDP per capita': '#B8D1B2',
    'Social support': '#A7C7E7',
    'Healthy life expectancy': '#F6C6EA',
    'Freedom': '#F9E79F',
    'Generosity': '#C7CEEA',
    'Perceptions of corruption': '#D3D3D3',
    'Residual': '#B0B0B0',
    'Top 10': '#6DC6A4',
    'Others': 'gray'
}

sns.set_palette([component_colors_all['Top 10'], component_colors_all['Others']])

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

top10 = df.sort_values('Score', ascending=False).head(10).copy()
top10_countries = top10['Country'].tolist()

# SLIDE 1
plt.figure(figsize=(10,6), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

sns.barplot(x='Score', y='Country', data=top10, palette=[component_colors_all['Top 10']])

plt.title('Top 10 Happiest Countries (2019)', fontsize=16, pad=40)
plt.text(0.5, 1.06, 
         'These are the happiest countries in 2019 — but what factors influence happiness?',
         fontsize=12,
         ha='center',
         va='center',
         style='italic',
         color='dimgray',
         transform=plt.gca().transAxes)

plt.xlabel('Happiness Score (0–10)', fontsize=12, labelpad=20)
plt.ylabel('Country', fontsize=12, labelpad=20)

for i, (index, row) in enumerate(top10.iterrows()):
    plt.text(row['Score'] + 0.05,
             i,
             f'{row["Score"]:.2f}',
             va='center', fontsize=11)
plt.grid(False)

ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('slide1_top10.png')
plt.close()

# SLIDE 2
plt.figure(figsize=(8,6), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

top10_gen = top10['Generosity'].mean()
rest_gen = df[~df['Country'].isin(top10_countries)]['Generosity'].mean()

sns.barplot(
    x=['Top 10 Countries', 'Other Countries'],
    y=[top10_gen, rest_gen],
    palette=[component_colors_all['Top 10'], component_colors_all['Others']]
)

plt.title('Generosity in Top 10 vs Other Countries (2019)', fontsize=16, pad=40)

plt.text(0.5, 1.06,
         'The happiest countries tend to have higher average generosity.',
         fontsize=12,
         ha='center',
         va='center',
         style='italic',
         color='dimgray',
         transform=plt.gca().transAxes)

plt.ylabel('Average Generosity', fontsize=12, labelpad=15)
plt.ylim(0, max(top10_gen, rest_gen) + 0.05)

for i, val in enumerate([top10_gen, rest_gen]):
    plt.text(i, val + 0.01, f'{val:.3f}', ha='center', va='bottom', fontsize=11)

plt.grid(False)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('slide2_generosity_comparison.png')
plt.close()

# SLIDE 3
plt.figure(figsize=(8,6), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

sns.scatterplot(
    x='Social support', y='Score',
    data=df[~df['Country'].isin(top10_countries)],
    color=component_colors_all['Others'],
    alpha=0.6,
    s=40,
    edgecolor=None
)

sns.scatterplot(
    x='Social support', y='Score',
    data=top10,
    color=component_colors_all['Top 10'],
    s=100,
    linewidth=1,
    label='Top 10'
)

plt.title('Social Support vs Happiness Score (2019)', fontsize=16, pad=40)

plt.text(0.5, 1.06,
         'Countries with stronger social support networks tend to be happier.',
         fontsize=12,
         ha='center',
         va='center',
         style='italic',
         color='dimgray',
         transform=plt.gca().transAxes)

plt.xlabel('Social Support', fontsize=12, labelpad=15)
plt.ylabel('Happiness Score', fontsize=12, labelpad=15)

plt.grid(False)

x = pd.to_numeric(df['Social support'], errors='coerce')
y = pd.to_numeric(df['Score'], errors='coerce')
mask = x.notna() & y.notna()
x_clean = x[mask]
y_clean = y[mask]

coef = np.polyfit(x_clean, y_clean, 1)
poly1d_fn = np.poly1d(coef)
x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
plt.plot(x_line, poly1d_fn(x_line), color="#A8D0D0", linestyle='-', linewidth=2, label='Trend Line')

plt.legend(title='', loc='upper left')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('slide3_support_vs_score.png')
plt.close()

# SLIDE 4
plt.figure(figsize=(8,6), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

sns.scatterplot(
    x='GDP per capita', y='Score',
    data=df[~df['Country'].isin(top10_countries)],
    color=component_colors_all['Others'],
    alpha=0.6,
    s=40,
    edgecolor=None
)

sns.scatterplot(
    x='GDP per capita', y='Score',
    data=top10,
    color=component_colors_all['Top 10'],
    s=100,
    linewidth=1,
    label='Top 10'
)

plt.title('GDP per Capita vs Happiness Score (2019)', fontsize=16, pad=40)

plt.text(0.5, 1.06,
         'Higher GDP per capita is associated with greater happiness.',
         fontsize=12,
         ha='center',
         va='center',
         style='italic',
         color='dimgray',
         transform=plt.gca().transAxes)

plt.xlabel('GDP per Capita', fontsize=12, labelpad=15)
plt.ylabel('Happiness Score', fontsize=12, labelpad=15)

plt.grid(False)

x = pd.to_numeric(df['GDP per capita'], errors='coerce')
y = pd.to_numeric(df['Score'], errors='coerce')
mask = x.notna() & y.notna()
x_clean = x[mask]
y_clean = y[mask]

coef = np.polyfit(x_clean, y_clean, 1)
poly1d_fn = np.poly1d(coef)
x_line = np.linspace(x_clean.min(), x_clean.max(), 100)
plt.plot(x_line, poly1d_fn(x_line), color="#A8D0D0", linestyle='-', linewidth=2, label='Trend Line')

plt.legend(title='', loc='upper left')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('slide4_gdp_vs_score.png')
plt.close()

# SLIDE 5
core_factors = [
    'GDP per capita',
    'Social support',
    'Healthy life expectancy',
    'Freedom',
    'Generosity',
    'Perceptions of corruption'
]

top10['Residual'] = top10['Score'] - top10[core_factors].sum(axis=1)
all_components = core_factors + ['Residual']

component_colors = {
    'GDP per capita': component_colors_all['GDP per capita'],
    'Social support': component_colors_all['Social support'],
    'Healthy life expectancy': component_colors_all['Healthy life expectancy'],
    'Freedom': component_colors_all['Freedom'],
    'Generosity': component_colors_all['Generosity'],
    'Perceptions of corruption': component_colors_all['Perceptions of corruption'],
    'Residual': component_colors_all['Residual']
}

plt.figure(figsize=(16, 9), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

bottom = [0] * len(top10)

for component in all_components:
    values = top10[component]
    plt.bar(top10['Country'], values, label=component, bottom=bottom, color=component_colors[component])
    for j, value in enumerate(values):
        if value > 0.1:
            y_pos = bottom[j] + value / 2
            plt.text(j, y_pos, f'{value:.2f}', ha='center', va='center', fontsize=8)
    bottom = [bottom[j] + values.iloc[j] for j in range(len(values))]

ax.grid(False)

plt.title('Happiness Score Breakdown for Top 10 Countries (2019)', fontsize=16, pad=50)
plt.text(
    0.5, 1.04,
    'Each happiness score is made up of measurable factors — plus a residual (unexplained happiness) that captures the rest.',
    fontsize=12,
    ha='center',
    va='bottom',
    style='italic',
    color='dimgray',
    transform=ax.transAxes
)

plt.ylabel('Happiness Score (0–10)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Score Components', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout(rect=[0,0,1,0.9])
plt.savefig('slide5_stacked_score_breakdown.png')
plt.close()
