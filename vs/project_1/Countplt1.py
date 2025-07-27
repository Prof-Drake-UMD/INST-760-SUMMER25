import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv('')
sns.catplot(x="Ethnicity",
            data=df,
            hue="Ethnicity",
            kind="count")

plt.xticks(rotation=90)
plt.show()
