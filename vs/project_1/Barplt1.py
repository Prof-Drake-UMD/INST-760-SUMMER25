import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")

df= pd.read_csv('Credit_Data.csv')


Ratesort =df.sort_values("Rating",ascending=False)


sns.barplot(x="Rating",
            y="Ethnicity",
            data=Ratesort,
            errorbar=('ci',0),
            hue="Student"
             )
        
plt.xticks(rotation=90)
plt.show()

