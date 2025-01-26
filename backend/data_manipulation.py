import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

df = pd.read_csv('backend/top_10000_1960-now.csv')
print(df.head())

# Display basic info about the dataset
print(df.info())

# Get summary statistics of numeric columns
print(df.describe())



