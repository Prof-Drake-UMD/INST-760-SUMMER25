# variables
# x = percent_low_income
# y = avg_test_score_percent	
# color = school type (Public, Private, or Charter)
# size = funding_per_student_usd 
# facets = grade level (Elementary, Middle, or High)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('education_inequality_data.csv')

# before plotting, need to filter for only NY
select_state = 'New York'
df = df.query("state==@select_state")

# clean out empty rows
df = df.dropna()

# now plotting
sns.set_style("whitegrid")
g = sns.relplot(data=df, x="percent_low_income", y="avg_test_score_percent", kind="scatter", hue="school_type", size="funding_per_student_usd", sizes=(50,500), alpha=0.7, col="grade_level", palette="Set1")
# labels/titles
g.set_titles("Grade Level: {col_name}")
g.set_axis_labels("Percent Low Income (%)", "Average Test Score (%)")
g.fig.suptitle("The Impact of Student Household Income on Student Test Scores in New York", fontsize=16)
# brief caption to explain 
g.fig.text(0.5, 0.01, 
           "Figure: Relationship between the percentage of low-income students and their test scores in New York schools. "
           "Point size represents the amount of funding per student, and color indicates school type.", 
           ha='center', fontsize=10,fontstyle='italic')
# adjusting (bc y-axis starts at 40... want it to start at 0%)
g.set(ylim=(0, None))
g.fig.subplots_adjust(top=0.85, bottom=0.15)
plt.savefig("projct2.png")
plt.show()
plt.clf()