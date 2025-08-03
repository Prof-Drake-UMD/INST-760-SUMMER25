import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set pastel colors for all charts
pastel_colors = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#FFB3F7", "#B3FFBA", "#FFD9B3", "#E6B3FF"]
sns.set_palette(pastel_colors)

# Load our chocolate sales data
chocolate_data = pd.read_csv("Chocolate Sales.csv")

# Clean up the sales amounts (remove $ and commas)
chocolate_data["Amount"] = chocolate_data["Amount"].str.replace("$", "").str.replace(",", "").str.strip()
chocolate_data["Amount"] = pd.to_numeric(chocolate_data["Amount"], errors="coerce")

# Convert dates to proper format
chocolate_data["Date"] = pd.to_datetime(chocolate_data["Date"], errors="coerce")

# Create our first chart - Sales by Country
plt.figure(figsize=(10, 6))
sns.barplot(x="Country", y="Amount", data=chocolate_data)
plt.title("Sales by Country")
plt.xticks(rotation=45)
plt.savefig("chart1.png")
plt.close()

# Create our second chart - Sales by Product  
plt.figure(figsize=(12, 8))
sns.barplot(x="Amount", y="Product", data=chocolate_data)
plt.title("Sales by Product")
plt.savefig("chart2.png")
plt.close()

# Create our third chart - Amount vs Boxes Shipped
plt.figure(figsize=(10, 6))
sns.scatterplot(x="Boxes Shipped", y="Amount", data=chocolate_data)
plt.title("Amount vs Boxes Shipped")
plt.savefig("chart3.png")
plt.close()

# Create our fourth chart - Sales Over Years
chocolate_data["Year"] = chocolate_data["Date"].dt.year
plt.figure(figsize=(10, 6))
sns.barplot(x="Year", y="Amount", data=chocolate_data)
plt.title("Sales Over Years")
plt.savefig("chart4.png")
plt.close()

# Create our fifth chart - Boxes Shipped by Country
plt.figure(figsize=(10, 6))
sns.boxplot(x="Country", y="Boxes Shipped", data=chocolate_data)
plt.title("Boxes Shipped by Country")
plt.xticks(rotation=45)
plt.savefig("chart5.png")
plt.close()


