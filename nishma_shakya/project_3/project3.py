import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# dataframe from csv
df = pd.read_csv("teen_phone_addiction_dataset.csv")

"""
Story: Heavy phone usage hinders student lifestyle and academics
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
# plt.savefig("plot_1.png")
# plt.show()
plt.clf()

# plot 2: scatter (more addicted = checking phone more)
# sns.set_style("whitegrid")
# plt.figure(figsize=(8,5))
sns.regplot(
    data=df, x="Addiction_Level", y="Phone_Checks_Per_Day",
    scatter_kws={'alpha':0.3, 's':30}, line_kws={'color':'red'}
)
# labes titles
plt.title("Phone Checks Increase with Addiction Level", fontsize=14, weight='bold')
plt.xlabel("Addiction Level (scale 1-10)")
plt.ylabel("Number of Phone Checks Per Day")
plt.tight_layout()
# plt.savefig("plot_2.png")
# plt.show()
plt.clf()

# plot 3: boxplot (addiction affects academics)
# sns.set_style("whitegrid")
# plt.figure(figsize=(8,5))
# another scatter
sns.regplot(
    data=df, x="Addiction_Level", y="Sleep_Hours",
    scatter_kws={'alpha':0.4, 's':30}, line_kws={'color':'red'}
)
# lablesn and titles
plt.title("Higher Addiction Leads to Less Sleep", fontsize=14, weight='bold')
plt.xlabel("Addiction Level")
plt.ylabel("Average Sleep Time (hours)")
plt.tight_layout()
# plt.savefig("plot_3.png")
# plt.show()
plt.clf()

# plot 4: 
# sns.set_style("whitegrid")
# plt.figure(figsize=(8,5))

# sns.regplot(data=df, x="Sleep_Hours", y="Self_Esteem")

sns.catplot(data=df, kind="bar", x="Sleep_Hours", y="Self_Esteem")

# plt.title("Higher Addiction Means Less Study Time", fontsize=14, weight='bold')
# plt.xlabel("Addiction Level")
# plt.ylabel("Time on Education (hours per day)")

plt.tight_layout()
# plt.savefig("plot_4.png")
plt.show()
plt.clf()

# plot 5: 
