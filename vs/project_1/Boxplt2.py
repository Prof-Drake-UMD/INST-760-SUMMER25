import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




df= pd.read_csv('Credit_Data.csv')
g=sns.catplot(x="Ethnicity",
                y="Rating",
                data=df, kind="box",
                whis=[0,100],
              col="Gender",
              hue="Ethnicity"
              )


plt.xticks(rotation=90)
plt.show()
               
