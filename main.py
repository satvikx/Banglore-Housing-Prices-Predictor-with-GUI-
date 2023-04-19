import pandas as pd
import numpy as np 

import os
os.chdir(r"C:\Users\v\Desktop\C Lang Tutorials\HPP with GUI\ ")

data = pd.read_csv("Bengaluru_House_Data.csv")
#print(data.head())

#print(data.isna().sum())

data.drop(columns=['availability', 'area_type', 'society', 'balcony' ], inplace = True)
# print(data.describe())
# print(data.info())

#-------------CLEANING THE DATA--------
data['location'] = data['location'].fillna('Sarjapur Road')
data['size'] = data['size'].fillna('2 BHK')
data['bath'] = data['bath'].fillna(data['bath'].median())
#print(data.info())

data['bhk'] = data['size'].str.split().str.get(0).astype(int)
# print(data[data.bhk > 20])

def convertRange(x):
    temp = x.split('-')
    if len(temp) == 2:
        return (float(temp[0]) + float(temp[1]))/2
    try:
        return float(x)
    except:
        return None

data['total_sqft'] = data['total_sqft'].apply(convertRange)
# print(data.head())

data['price_per_sqft'] = data['price'] * 100000 / data['total_sqft']
#print(data.describe())

data['location'] = data['location'].apply(lambda x : x.strip())
lc = data['location'].value_counts()
lcc = lc[lc<=10]

data['location'] = data['location'].apply(lambda x: 'other' if x in lcc else x)
#print(data['location'].value_counts())

data = data[((data['total_sqft']/data['bhk']) >= 300)]
#print(data.shape)

def rem(df):     #remove outliers of sqft
        df_output = pd.DataFrame()
        for key, subdf in df.groupby('location'):
            m = np.mean(subdf.price_per_sqft)
            st = np.std(subdf.price_per_sqft)
            gen_df = subdf[(subdf.price_per_sqft > (m-st)) & (subdf.price_per_sqft <= (m+st))]
            df_output = pd.concat([df_output, gen_df], ignore_index = True)
        return df_output
data = rem(data)
#print(data.describe())

def bhkrem(df):
    ei = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean' : np.mean(bhk_df.price_per_sqft),
                'std' : np.std(bhk_df.price_per_sqft),
                'count' : bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                ei = np.append(ei, bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values)
    return df.drop(ei, axis = 'index')

data = bhkrem(data)
print(data.shape)

data.drop(columns = ['size', 'price_per_sqft'], inplace = True)
#print(data.head())

data.to_csv('Cleaned_data.csv')

#-------------DATA CLEANED!!!--------------







