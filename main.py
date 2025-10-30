import pandas as pd

df = pd.read_csv("/Users/rauf/Desktop/car_dataset/data/cars.csv")
# print(df.head())

# print(df.info())

print("Duplicate rows:", df.duplicated().sum())

print("Duplicate IDs:", df['id'].duplicated().sum())

print(df.nunique())

df['purchased_date'] = pd.to_datetime(df['purchased_date'])

print(df['purchased_date'].min(), df['purchased_date'].max())

print(df.dtypes)

df["purchase_year"] = df["purchased_date"].dt.year
df["purchase_month"] = df["purchased_date"].dt.month
df["purchase_day"] = df["purchased_date"].dt.day
df["purchase_weekday"] = df["purchased_date"].dt.day_name()

print(df.head())

