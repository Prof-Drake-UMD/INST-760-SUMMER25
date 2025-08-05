# pokemon_viz.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines

df = pd.read_csv("Pokemon.csv")
df = df.dropna()

df['marker'] = df['Legendary'].apply(lambda x: '*' if x else 'o')

gen_min, gen_max = df['Generation'].min(), df['Generation'].max()
df['alpha'] = 0.4 + 0.6 * (1 - (df['Generation'] - gen_min) / (gen_max - gen_min))

types = df['Type 1'].unique()
palette = sns.color_palette('hls', len(types))
type_color = dict(zip(types, palette))

plt.figure(figsize=(14, 9))
sns.set(style='whitegrid')

for marker_type in ['o', '*']:
    subset = df[df['marker'] == marker_type]
    plt.scatter(
        x=subset['Attack'],
        y=subset['Defense'],
        s=subset['Speed'],  
        c=subset['Type 1'].map(type_color),  
        alpha=subset['alpha'],  
        marker=marker_type,
        edgecolor='black',
        linewidths=0.5,
        label='Legendary' if marker_type == '*' else 'Regular'
    )

top5 = df.nlargest(5, 'Total')
plt.scatter(
    top5['Attack'],
    top5['Defense'],
    s=top5['Speed'] * 3,  
    c=top5['Type 1'].map(type_color),
    marker='s',  
    edgecolor='red',
    linewidths=2,
    label='Top 5 Total'
)

# Legend for Pokémon Type (Type 1) — colored circles
handles_type = [plt.Line2D([0], [0], marker='o', color='w',
                          label=type_, markerfacecolor=color,
                          markersize=10) for type_, color in type_color.items()]
legend1 = plt.legend(handles=handles_type, title="Type 1", bbox_to_anchor=(1.05, 1), loc='upper left')

# Legend for marker shapes (Legendary vs Regular + Top 5)
legendary_handles = [
    mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=10, label='Regular'),
    mlines.Line2D([], [], color='black', marker='*', linestyle='None', markersize=15, label='Legendary'),
    mlines.Line2D([], [], color='red', marker='s', linestyle='None', markersize=15, markeredgecolor='red', markeredgewidth=2, label='Top 5 Total')
]
plt.legend(handles=legendary_handles, title='Legendary Status', loc='lower right')

# Add the Type 1 legend back on the plot
plt.gca().add_artist(legend1)

# Titles and labels
plt.title("Pokémon Battle Stats by Type, Speed, and Generation", fontsize=16)
plt.xlabel("Attack")
plt.ylabel("Defense")

plt.tight_layout(rect=[0, 0, 0.85, 1])

# Save the plot to file
plt.savefig("pokemon_multidimensional_plot.png", dpi=300)
plt.show()
