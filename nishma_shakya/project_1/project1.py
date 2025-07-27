import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# load in data
df = pd.read_csv("ramen-ratings.csv")
df_short = df.head(100)  
# limiting to first 100 rows bc it's a big dataset and it makes the graph overcrowsded

# Columns: Brand, Style, Country, Stars 


# PLOT 1: Count plot of count of ramen brands
# DESCRIPTION: This count plot shows how many times each ramen brand appears in the dataset (limited to 100 entries). Some brands appear more frequently than others, indicating higher representation or popularity in reviews. The most popular ramen brand according to this dataset it Nissin.

brand_order = df_short['Brand'].value_counts().index.tolist()  # to order countplot bars
sns.set_style("dark")
g = sns.catplot(y="Brand", data=df_short, kind="count", order=brand_order, palette="colorblind", height=10)
g.set(xlabel="Count of Ratings", ylabel="Ramen Brand") 
plt.title("Rating Count of Different Brands of Ramen", y=1.02)
plt.tight_layout()
plt.savefig("plot1.png")
plt.show()
plt.clf()


# PLOT 2: Bar plot of average rating by country
# DESCRIPTION: This bar plot shows the average customer rating (on a 0–5 star scale) of ramen products by country of origin, based on the dataset (limited to 100 entries). Only countries with valid numeric ratings are included.

# Stars column is string, so converting to numeric
df_short['Stars'] = pd.to_numeric(df_short['Stars'], downcast='float', errors='coerce')
# Stars column has some non-numeric values so dropping those
df_short = df_short.dropna(subset=['Stars'])
# Order bars for country (this time it's ordering based on ratings instead of just count)
# country_order = df_short['Country'].value_counts().index.tolist()
country_order = df_short.groupby('Country')['Stars'].mean().sort_values(ascending=False).index.tolist()

sns.set()
sns.set_style("white")
# g = sns.catplot(x="Stars", y="Country", data=df_short.query("Brand in @top_brands"), hue="Brand", kind="bar", ci=None)
g = sns.catplot(x="Country", y="Stars", data=df_short, kind="bar", ci=None, order=country_order, palette="RdBu_r")
g.set(xlabel="Country", ylabel="Average Rating (0-5 stars)") 
sns.despine(left=True, bottom=True)
plt.title("Average Ramen Rating by Country", y=1.02)
plt.xticks(rotation=90)
plt.tight_layout()   
plt.savefig("plot2.png")
plt.show()
plt.clf()



# PLOT 3: Box plot of distribution of ratings
# DESCRIPTION:This box plot displays the distribution of average ratings (scale of 0-5 stars) for each ramen brand in the dataset (limited to 100 rows). Brands are ordered by median rating. This helps identify consistency and variability in brand ratings.

# df_short['Stars'] = pd.to_numeric(df_short['Stars'], downcast='float', errors='coerce')
# # Stars column has some non-numeric values so dropping those
# df_short = df_short.dropna(subset=['Stars'])

# order the brands by the median to make it easier to read (sorts it)
brand_order = df_short.groupby("Brand")["Stars"].median().sort_values(ascending=False).index.tolist()

sns.set()
sns.set_style("whitegrid")
g = sns.catplot(x="Brand", y="Stars", data=df_short, kind="box", order=brand_order, palette="colorblind", aspect=2)
g.set(xlabel="Ramen Brands", ylabel="Ratings of Ramen Brands (0-5 stars)")
plt.title("Distribution of Average Ramen Ratings by Brand", y=1.02)
plt.ylim(0)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("plot3.png")
plt.show()
plt.clf()



# PLOT 4: Point plot of avg rating by brand in different countries
# DESCRIPTION: This point plot shows the average ramen ratings (scale 0-5 stars) for different brands, categorized by country. Each point represents the mean rating for a brand within a specific country. The plot reveals how ratings for brands vary across countries.

sns.set()
sns.set_style("whitegrid")
g = sns.catplot(x="Brand", y="Stars", data=df_short, kind="point", join=False, ci=None, hue="Country", height=4, aspect=2)
g.set(xlabel="Ramen Brands", ylabel="Ratings of Ramen Brands (0-5 stars)")
plt.title("Average Ramen Rating by Brand Across Countries", y=1.02)
plt.xticks(rotation=90)
plt.ylim(0)
# plt.tight_layout()
g.fig.set_size_inches(10, 10)

plt.savefig("plot4.png")
plt.show()
plt.clf()


# PLOT 5: Faceted bar plot of of the ratings vs. brand  by diff styles
# DESCRIPTION: This faceted bar plot compares the average star ratings (cale of 0-5 stars) of ramen across different styles (such as cup, pack, and bowl) for five frequently reviewed brands. 

# df_short['Stars'] = pd.to_numeric(df_short['Stars'], downcast='float', errors='coerce')
# # Stars column has some non-numeric values so dropping those
# df_short = df_short.dropna(subset=['Stars'])

# Get 5 brands (just by how many ratings they have)
five_brands = df_short['Brand'].value_counts().index[:5].tolist()
# Filter data to just rows with those brands
df_brands = df_short[df_short['Brand'].isin(five_brands)]

sns.set()
sns.set_style("whitegrid")
g = sns.catplot(data=df_brands, x="Brand", y="Stars", kind="bar", col="Style", ci=None, palette="colorblind")
g.set(xlabel="Ramen Brands", ylabel="Ratings of Ramen Brands (0-5 stars)")
g.fig.suptitle("Average Ratings of Different Ramen Styles Across Selected Brands", y=1.0)
g.set_titles("Ramen Style: {col_name}")
# need to rotate all subplot x labels, call in loop
for ax in g.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)
plt.tight_layout() 
plt.savefig("plot5.png")
plt.show()
plt.clf()



""" 
Sources:
tight layout: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/demo_tight_layout.html
convert data string to numeric: https://www.statology.org/pandas-to_numeric/
loop through axes in facet grid: https://www.tutorialspoint.com/what-does-axes-flat-in-matplotlib-do
"""