import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("CSV_PATH")

df = pd.read_csv(CSV_PATH)
print(df.head())
print()
print(df.info())
print()
print("Duplicate rows:", df.duplicated().sum())
print()
print("Duplicate IDs:", df['id'].duplicated().sum())
print()
print(df.nunique())
print()
df['purchased_date'] = pd.to_datetime(df['purchased_date'])
print()
print(df['purchased_date'].min(), df['purchased_date'].max())
print()
print(df.dtypes)
print()
print(df.head())