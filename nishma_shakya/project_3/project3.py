import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# dataframe from csv
df = pd.read_csv("teen_phone_addiction_dataset.csv")

"""
Story: Students are becoming addiction to their phones
"""

# plot 1: bar stacked (time on social, time on education, time on games BY age groups)
sns.set_style("whitegrid")
# get the columns to stack
activity_columns = ['Time_on_Social_Media', 'Time_on_Gaming', 'Time_on_Education']
# group by age category
df_age_activities = df.groupby('Age')[activity_columns].mean()
# stacked bar plot
fig, ax = plt.subplots(figsize=(8,5))
df_age_activities.plot(kind='bar', stacked=True, ax=ax)
# labels
ax.set_xlabel("Age")
ax.set_ylabel("Average Hours per Day")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0) # bc rotated
plt.title("How Teens Spend Their Phone Time", fontsize=14, weight='bold')
# set legend and its postion
plt.legend(title="Activity Type", loc='upper center', bbox_to_anchor=(0.5, 1.45))
plt.tight_layout()
plt.savefig("plot_1.png")
plt.show()
plt.clf()

# plot 2: scatter (more addicted = checking phone more)
sns.set_style("white")
# plt.figure(figsize=(8,5))
sns.regplot(data=df, x="Phone_Checks_Per_Day", y="Addiction_Level", scatter_kws={'alpha':0.4, 's':30}, line_kws={'color':'red'}
)
sns.despine()
# labes titles
plt.title("Addiction Level Increases with Phone Checks", fontsize=14, weight='bold')
# SWITCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
plt.ylabel("Addiction Level (scale 1-10)")
plt.xlabel("Number of Phone Checks Per Day")
plt.tight_layout()
plt.savefig("plot_2.png")
plt.show()
plt.clf()

# plot 3: scatter (addiction affects sleep)
sns.set_style("white")
# plt.figure(figsize=(8,5))
# another scatter with regression
sns.regplot(data=df, x="Addiction_Level", y="Sleep_Hours", scatter_kws={'alpha':0.4, 's':30}, line_kws={'color':'red'}
)
sns.despine()
# lablesn and titles
plt.title("Higher Addiction Leads to Less Sleep", fontsize=14, weight='bold')
plt.xlabel("Addiction Level")
plt.ylabel("Average Sleep Time (hours)")
plt.tight_layout()
plt.savefig("plot_3.png")
plt.show()
plt.clf()

# plot 4: addiction level vs education time
# make it rounded so no decimals
sns.set_style("whitegrid")
df['Addiction_Level_Round'] = df['Addiction_Level'].round().astype(int)
plt.figure(figsize=(8,5))
# box... with CI
sns.boxplot(data=df, x='Addiction_Level_Round', y='Apps_Used_Daily')
sns.despine()
# labels titles
plt.title("Addiction Increases the Apps Used Daily", fontsize=14, weight='bold')
plt.xlabel("Addiction Level (rounded)")
plt.ylabel("Number of Apps Used Daily")
plt.tight_layout()
plt.savefig("plot_4.png")
plt.show()
plt.clf()


# plot 5: more addicted = more phone use
# plt.figure(figsize=(8,5))
sns.set_style("white")
# scatter agian
# sns.scatterplot(data=df, x='Addiction_Level', y='Daily_Usage_Hours', alpha=0.5)
sns.regplot(data=df, x='Addiction_Level', y='Daily_Usage_Hours', scatter_kws={'alpha':0.4, 's':30}, line_kws={'color': 'red'})
sns.despine()
# titles labels
plt.title("Higher Addiction Level Leads to More Daily Phone Usage", fontsize=14, weight='bold')
plt.xlabel("Addiction Level (1-10)")
plt.ylabel("Daily Phone Usage (hours)")
plt.tight_layout()
plt.savefig("plot_5.png")
plt.show()
plt.clf()
