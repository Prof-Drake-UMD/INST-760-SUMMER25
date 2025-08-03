import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Iris.csv')

# Plot 1: Spatial Length vs Sepal Width
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='SepalLengthCm', y='SepalWidthCm')
plt.title("Sepal Length vs Sepal Width")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
plt.savefig("plot1_basic_scatter.png")
plt.clf()

# Plot 2: Add Color(Distinguish species using color)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='SepalLengthCm', y='SepalWidthCm', hue='Species', palette='Set2')
plt.title("Sepal Dimensions by Species")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
plt.legend(title='Species')
plt.savefig("plot2_add_color.png")
plt.clf()

# Plot 3: Add Shape (Introduce a second categorical dimension)
df['petal_width_bin'] = pd.cut(df['PetalWidthCm'], bins=[0, 0.5, 1, 1.5, 2.5], 
                               labels=['Thin', 'Medium', 'Thick', 'Very Thick'])
plt.figure(figsize=(9, 6), constrained_layout=True)
sns.scatterplot(data=df, x='SepalLengthCm', y='SepalWidthCm',
                hue='Species', style='petal_width_bin', palette='Set2')
plt.title("Sepal Dimensions by Species and Petal Thickness")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
plt.legend(title='Legend', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.savefig("plot3_add_shape.png", bbox_inches='tight')
plt.clf()

# Plot 4: Add Size (Petal Length)
plt.figure(figsize=(9, 6), constrained_layout=True)
sns.scatterplot(data=df, x='SepalLengthCm', y='SepalWidthCm',
                hue='Species', style='petal_width_bin', size='PetalLengthCm',
                palette='Set2', sizes=(40, 300), edgecolor='black', alpha=0.85)
plt.title("Sepal Dimensions by Species, Petal Width & Petal Length")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.savefig("plot4_add_size.png", bbox_inches='tight')
plt.clf()

# Plot 5: Final Clean Multi-Dimensional Plot with Custom Legend
plt.figure(figsize=(9, 7), constrained_layout=True)
plot = sns.scatterplot(data=df, x='SepalLengthCm', y='SepalWidthCm',
                       hue='Species', style='petal_width_bin', size='PetalLengthCm',   
                       palette='Set2',  sizes=(40, 300), edgecolor='black', alpha=0.85
  )
plt.title("Iris Flower Characteristics by Species, Petal & Sepal Attributes")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
handles, labels = plot.get_legend_handles_labels()
plot.legend(handles=handles[1:], labels=labels[1:], bbox_to_anchor=(1.02, 1), loc='upper left')
plt.savefig("plot5_final_multidimensional.png")
plt.clf()