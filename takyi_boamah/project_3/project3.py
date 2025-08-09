import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_path = os.path.join(os.path.dirname(__file__), "sp500")
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG'] 

# Load and Clean Data 
stock_data = []
for ticker in tickers:
    file_path = os.path.join(base_path, f"{ticker}.csv")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.replace('# ', '', regex=False)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
    df.rename(columns={'Date': 'date'}, inplace=True)
    df['ticker'] = ticker
    stock_data.append(df)

# Combine and Pivot 
df_all = pd.concat(stock_data)
pivot_df = df_all.pivot(index='date', columns='ticker', values='Close')

# Time Slices
pre_covid = pivot_df['2015':'2019']
covid_crash = pivot_df['2020-01':'2020-03']
recovery = pivot_df['2020-04':'2021-12']
post_covid = pivot_df['2022':'2023']

# slide 1
plt.figure(figsize=(10, 6))
pre_covid.plot(ax=plt.gca())
plt.title("The Rise of Tech Before the Storm")
plt.suptitle("Tech stocks soared steadily through the late 2010s.", fontsize=10)
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price ($)")
plt.legend(title="Ticker", loc='upper left', bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.savefig("slide1_pre_covid.png")
plt.clf()

# Slide 2
plt.figure(figsize=(10, 6))
covid_crash.plot(ax=plt.gca(), linewidth=2)
plt.title("March 2020: The COVID Cliff")
plt.suptitle("A sudden drop hit all tech giants in March 2020.", fontsize=10)
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price ($)")
plt.legend(title="Ticker", loc='upper left', bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.savefig("slide2_covid_crash.png")
plt.clf()

# Slide 3
plt.figure(figsize=(10, 6))
recovery.plot(ax=plt.gca(), linewidth=2)
plt.title("Tech Bounces Back — Harder and Faster")
plt.suptitle("Recovery came fast, especially for remote-enabled companies.", fontsize=10)
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price ($)")
plt.legend(title="Ticker", loc='upper left', bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.savefig("slide3_recovery.png")
plt.clf()

# Slide 4 
growth = ((pivot_df.loc['2021-12-31'] - pivot_df.loc['2020-01-02']) / pivot_df.loc['2020-01-02']) * 100
plt.figure(figsize=(8, 6))
growth[tickers].sort_values().plot(kind='bar', color=sns.color_palette("pastel"))
plt.title("Not All Tech Stocks Grew Equally")
plt.suptitle("Apple led the pack, while others lagged.", fontsize=10)
plt.ylabel("Growth (%) Jan 2020 - Dec 2021")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("slide4_growth_comparison.png")
plt.clf()


# Slide 5 
plt.figure(figsize=(10, 6))
post_covid.plot(ax=plt.gca(), linewidth=2)
plt.title("Have Tech Stocks Stabilized Post-Pandemic?")
plt.suptitle("Volatility remains, but trends differ heading into 2023.", fontsize=10)
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price ($)")
plt.legend(title="Ticker", loc='upper left', bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.savefig("slide5_post_covid.png")
plt.clf()