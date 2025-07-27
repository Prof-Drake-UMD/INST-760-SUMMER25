import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# Plot 1: Count of Movies vs TV Shows 
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='type', hue='type', palette='pastel')
plt.title('Count of Movies vs TV Shows')
plt.xlabel('Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig("plot1_movies_vs_tvshows.png")
plt.clf()

# Plot 2: Top 10 Countries Producing Titles 
top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, dodge=False, palette='muted', legend=False)
plt.title('Top 10 Countries by Content Production')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig("plot2_top_countries.png")
plt.clf()

# Plot 3: Distribution of Titles by Release Year
plt.figure(figsize=(8, 5))
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
bins = max_year - min_year + 1 
sns.histplot(df['release_year'], bins=bins, color='#007acc', edgecolor='black')
plt.title('Trend of Movie/TV Titles Released Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Release Year', fontsize=12)
plt.ylabel('Number of Titles', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("plot3_year_distribution.png")
plt.clf()

# Plot 4: Top 10 Genres by Count
top_genres = df['listed_in'].str.split(', ').explode().value_counts().head(10)
plt.figure(figsize=(8, 5)) 
sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette='viridis', dodge=False)
plt.title('Top 10 Genres by Count', fontsize=14, fontweight='bold')
plt.xlabel('Number of Titles', fontsize=12)
plt.ylabel('Genre', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("plot4_top_genres.png")
plt.clf()


# Plot 5: Duration of Movies
df_movies = df[df['type'] == 'Movie'].copy()
df_movies['duration'] = df_movies['duration'].str.extract('(\d+)').astype(float)
sns.set_style("whitegrid")
plt.figure(figsize=(8, 5))
sns.histplot(df_movies['duration'].dropna(), bins=30, color='#4c72b0', edgecolor='black')
plt.title('Distribution of Movie Durations', fontsize=14, fontweight='bold')
plt.xlabel('Duration (minutes)', fontsize=12)
plt.ylabel('Number of Movies', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
sns.despine()
median_duration = df_movies['duration'].median()
plt.axvline(median_duration, color='red', linestyle='--', linewidth=1.5, label=f'Median: {int(median_duration)} min')
plt.legend()
plt.savefig("plot5_duration_distribution.png")
plt.clf()