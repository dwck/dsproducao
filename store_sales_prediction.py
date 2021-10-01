#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:35:56 2021

@author: dwerneck
"""

import pandas as pd
import inflection
import math
import seaborn as sns
from matplotlib import pyplot as plt

df_sales_raw = pd.read_csv('train.csv',low_memory=False)
df_store_raw = pd.read_csv('store.csv',low_memory=False)
df = pd.merge(df_sales_raw,df_store_raw,how='left',on='Store')

df.columns
cols_old = ['Store', 'DayOfWeek', 'Date', 'Sales', 'Customers', 'Open', 'Promo','StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment','CompetitionDistance', 'CompetitionOpenSinceMonth','CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek','Promo2SinceYear', 'PromoInterval']
snakecase = lambda x: inflection.underscore(x)
cols_new = list(map(snakecase,cols_old))
df.columns = cols_new
df.dtypes

df['date'] = pd.to_datetime(df['date'])
df.isna().sum()

## Filling NA

df['competition_distance'].max()
df['competition_distance'] = df['competition_distance'].fillna(200000)

df['competition_open_since_month'] = df.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)

df['competition_open_since_year'] = df['competition_open_since_year'].fillna(df['date'].dt.year)
             
df['promo2_since_week'] = df['promo2_since_week'].fillna(df['date'].dt.isocalendar().week)

df['promo2_since_year'] = df['promo2_since_year'].fillna(df['date'].dt.year)
                 
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec' }
df['promo_interval'].fillna(0, inplace=True)
df['month_map'] = df['date'].dt.month.map(month_map)
df['is_promo'] = df[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1)

## Change Types

df['competition_open_since_month'] = df['competition_open_since_month'].astype(int)
df['competition_open_since_year'] = df['competition_open_since_year'].astype(int)
df['promo2_since_week'] = df['promo2_since_week'].astype(int)
df['promo2_since_year'] = df['promo2_since_year'].astype(int)

## Descriptive Statistical
num_attributes = df.select_dtypes(include=['int64','float64'])
cat_attributes = df.select_dtypes(exclude=['int64','float64','datetime64[ns]'])

d1 = num_attributes.describe().T
d2 = pd.DataFrame(num_attributes.apply(lambda x: x.skew()))
d2.columns = ['skew']
d3 = pd.DataFrame(num_attributes.apply(lambda x: x.kurtosis()))
d3.columns = ['kurtosis']
num_attributes_describe = pd.concat([d1,d2,d3],axis=1).reset_index()

sns.histplot(df['sales'])

cat_attributes.apply(lambda x: x.unique().shape[0])

aux1 = df[(df['state_holiday'] != '0') & (df['sales'] > 0)]
plt.subplot(1,3,1)
sns.boxplot(x='store_type',y='sales',data=aux1)            
plt.subplot(1,3,2)
sns.boxplot(x='state_holiday',y='sales',data=aux1) 
plt.subplot(1,3,3)
sns.boxplot(x='assortment',y='sales',data=aux1)











