import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")

df= pd.read_csv('')


Ratesort =df.sort_values("Rating",ascending=False)


sns.barplot(x="Rating",
            y="Ethnicity",
            data=Ratesort,
            errorbar=('ci',0),
            hue="Student"
             )
        
plt.xticks(rotation=90)
plt.show()


g=sns.catplot(x="Ethnicity",
                y="Rating",
                data=df, kind="box",
                whis=[0,100],
              col="Gender",
              hue="Ethnicity"
              )


plt.xticks(rotation=90)
plt.show()


sns.catplot(x="Ethnicity",
            data=df,
            hue="Ethnicity",
            kind="count")

plt.xticks(rotation=90)
plt.show()

sns.relplot(x="Education",
            y="Income",
            data=df,
            kind="line",
            errorbar=None)
plt.xticks(rotation=90)
plt.show()


sns.relplot(x="Cards",
                y="Rating",
                data=df, kind="scatter", hue="Married")

plt.xticks(rotation=90)
plt.show()
             


