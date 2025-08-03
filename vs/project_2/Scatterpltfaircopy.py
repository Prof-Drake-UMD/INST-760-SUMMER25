import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import path
import os


current_file_path=Path(_file_).resolve()
parent_directory=current_file_path.parent

filename="Credit_Data_updated.csv"
data_file_path=os.path.join(parent_directory,filename)
sns.set_theme(style="whitegrid")
df=pad.read.csv('data_file_path')





sns.scatterplot(data=df,
                x='Annual Income(in thousands of dollars)',
                y='Credit Rating',
                hue='Number of Cards owned per person',
                palette="Set1" ,
                style ="Gender"
                )

                
plt.xticks(rotation=90)
plt.show()
               
