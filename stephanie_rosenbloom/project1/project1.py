import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs("plots", exist_ok=True)
df = pd.read_csv("popular_anime.csv")
print(df.head())

# Narrow down to a few studios
studios_to_keep = ['Kyoto Animation', 'MAPPA', 'Bones', 'Wit Studio']
df_filtered = df[df['studios'].isin(studios_to_keep)]

# Plot1
plt.figure(figsize=(12, 8))

sns.scatterplot(
    data=df_filtered, x="episodes", y="rank",  palette="Set2", alpha=0.7,  edgecolor=None, s=20, hue="studios", style='studios')

plt.title("Number of Episodes vs Ranking")
plt.xlabel("Number of Episodes")
plt.ylabel("Ranking")
plt.legend(title="Studios")
plt.savefig("plots/plot1.png")
plt.close()


# Plot2 
plt.figure(figsize=(8, 6))

sns.countplot(
    data=df_filtered, x="type", palette="Set2")

plt.title("Type v. Count")
plt.xlabel("Type")
plt.ylabel("Count")
plt.savefig("plots/plot2.png")
plt.close()


# Plot3
plt.figure(figsize=(8, 6))

sns.histplot(
    df["score"].dropna(), kde=True, color="skyblue")

plt.title("Anime Score Distribution")
plt.xlabel("Score")
plt.ylabel("Count")
plt.savefig("plots/plot3.png")
plt.close()

#Plot4
plt.figure(figsize=(14, 10))

sns.boxplot(
    data=df_filtered, x="type", y="score", palette="colorblind")

plt.title("Score Distribution by Anime Type")
plt.xlabel("Type")
plt.ylabel("Score")
plt.savefig("plots/plot4.png")
plt.close()

#Plot5
plt.figure(figsize=(14, 10))

sns.violinplot(
    data=df, x="type", y="score", inner="quartile", palette="Set3")

plt.title("Score Distribution by Anime Type")
plt.xlabel("Type")
plt.ylabel("Score")
plt.savefig("plots/plot5.png")
plt.close()

