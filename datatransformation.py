
import numpy as np
import pandas as pd

!pip install openpyxl

df = pd.read_excel("Dataset.xlsx")

# setting columns as identifiers
id_vars = ['iso3', 'country', 'hdicode', 'region']

# metric columns
value_vars = [col for col in df.columns if '_' in col and col.split('_')[-1].isdigit()]

# transforming dataset from wide to long
long_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name="metric_year", value_name="value")

# Splitting metric_year into two columns
long_df[['metric', 'year']] = long_df['metric_year'].str.extract(r'(\D+)_([0-9]{4})')
long_df['year'] = long_df['year'].astype(int)

# Removing original metric_year
long_df.drop(columns=['metric_year'], inplace=True)

long_df = long_df[['iso3', 'country', 'region', 'metric', 'year', 'value']]

long_df.shape

long_df.info()

long_df.head()

long_df.isnull().sum()

long_df.to_csv("LongDataset.csv", index=False)

