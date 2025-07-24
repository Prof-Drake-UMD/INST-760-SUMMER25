import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




df= pd.read_csv('c:/UMDFILES/UMD/Summer2025/Summer-2-2025/Project/Credit_Data.csv')
sns.relplot(x="Cards",
                y="Rating",
                data=df, kind="scatter", hue="Married")

plt.xticks(rotation=90)
plt.show()
               
