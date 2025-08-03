import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('StudentsPerformance.csv')

# Create a size variable scaled from writing score
df['writing_scaled'] = df['writing score'] / df['writing score'].max() * 300

# Map gender to markers
marker_dict = {'female': 'o', 'male': 's'}

# Initialize the plot
g = sns.FacetGrid(df, col="race/ethnicity", hue="test preparation course", 
                  palette="Set2", height=4, col_wrap=3)

# Map scatterplot onto FacetGrid
g.map_dataframe(
    sns.scatterplot,
    x="math score",
    y="reading score",
    size="writing_scaled",
    sizes=(20, 300),
    style="gender",
    markers=marker_dict,
    legend=False
)

# Adjust legends and layout
g.add_legend(title="Test Prep")
g.set_axis_labels("Math Score", "Reading Score")
g.fig.suptitle("Multidimensional Student Performance Analysis", y=1.05)
plt.tight_layout()
plt.show()

