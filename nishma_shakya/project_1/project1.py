import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# load in data
df = pd.read_csv("ramen-ratings.csv")
df_short = df.head(100)  
# limiting to first 100 rows bc it's a big dataset and it makes the graph overcrowsded

# Columns: Brand, Style, Country, Stars 


# PLOT 1: Count plot of count of ramen brands
# Description: This count plot shows how many times each ramen brand appears in the dataset (limited to 100 entries). Some brands appear more frequently than others, indicating higher representation or popularity in reviews. The most popular ramen brand according to this dataset it Nissin.

brand_order = df_short['Brand'].value_counts().index.tolist()  # to order countplot bars
sns.set_style("dark")
g = sns.catplot(y="Brand", data=df_short, kind="count", order=brand_order, palette="colorblind", height=10)
g.set(xlabel="Count of Brands", ylabel="Ramen Brand") 
plt.title("Count of Different Brands of Ramen", y=1.02)
plt.tight_layout()
plt.savefig("plot1.png")
plt.show()
plt.clf()


# PLOT 2: Bar plot of average rating by country
# Description: This bar plot shows the average customer rating (on a 0–5 star scale) of ramen products by country of origin, based on the dataset (limited to 100 entries). Only countries with valid numeric ratings are included.

# Stars column is string, so converting to numeric (source: https://www.statology.org/pandas-to_numeric/)
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
g.set(xlabel="Country", ylabel="Average Rating (Stars)") 
sns.despine(left=True, bottom=True)
plt.title("Average Ramen Rating by Country", y=1.02)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("plot2.png")
plt.show()
plt.clf()



# PLOT 3: Box plot of distribution of ratings
# sns.catplot(x=“day”, y=“total_bill”, data=tips, kind="box")


# PLOT 4: Point plot of avg rating by brand in different countries
# sns.catplot(x=“day”, y=“total_bill”, data=tips, kind="point")


# PLOT 5: Scatter plot of of the ratings vs. brand for diff styles


# HISTOGRAM?


# note: save all plots as images in folder