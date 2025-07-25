import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv('')
sns.relplot(x="Education",
            y="Income",
            data=df,
            kind="line",
            ci=None)
plt.xticks(rotation=90)
plt.show()

