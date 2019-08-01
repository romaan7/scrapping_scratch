#!/usr/bin/python
#
# Created on Sat Jun 22 16:36:50 2019
# Copyright (C) 2019, shaikhr@tcd.ie
# @author: shaikhr
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import correlation
from scipy.stats.stats import pearsonr

import warnings

#filter for warnings and ignore
warnings.filterwarnings('ignore')

#Load users data from csv
#users_df = pd.read_csv('data/CSVs/users.csv', sep=',')
#print(users_df.head())

#Load projects data from csv
projects_df = pd.read_csv('data/CSVs/project_blocks.csv', sep=',',index_col=0, nrows=100)
projects_df = projects_df.drop(columns="other")
galleries_df = pd.read_csv('data/CSVs/project_sprites.csv', sep=',',index_col=0)
main_frame = pd.merge(projects_df, galleries_df, left_index=True, right_index=True)
print(main_frame)

index = projects_df.index
columns = projects_df.columns
values = projects_df.values

#required_columns_df = projects_df[['viewers_website','lovers_website','downloaders_website','sprites_website','scripts_website', 'blocks', 'block_types', 'images', 'sounds', 'ugstrings']]
#new_value = {'sprites_website': 1000, 'scripts_website': 1000, 'blocks': 1000, 'block_types': 1000, 'images': 1000, 'sounds': 1000, 'ugstrings': 1000, 'viewers_website': 1000, 'lovers_website': 1000, 'downloaders_website': 1000}
#n = pd.Series(new_value)
#n.name = 1000001
#new_df = required_columns_df.append(n)

#print(new_df)

#Load galleries data from csv
#galleries_df = pd.read_csv('data/CSVs/galleries.csv', sep=',')
#print(galleries_df.head())

#Load friends data from csv
#friends_df = pd.read_csv('data/CSVs/friends.csv', sep=',')
#print(friends_df.head())

#Load lovers data from csv
#lovers_df = pd.read_csv('data/CSVs/lovers.csv', sep=',')
#print(lovers_df.head())

#Load favoriters data from csv
#favoriters_df = pd.read_csv('data/CSVs/favoriters.csv', sep=',')
#print(favoriters_df.head())

#Load downloaders data from csv
#downloaders_df = pd.read_csv('data/CSVs/downloaders.csv', sep=',')
#print(downloaders_df.head())

#Load viewers data from csv
#viewers_df = pd.read_csv('data/CSVs/viewers.csv', sep=',')
#print(viewers_df.head())

#print(required_columns_df)

#Check the density of the missing values
#print(required_columns_df.isnull().sum()/len(required_columns_df))


#Impute the missing values using IterativeImputer from sklearn
#imp = SimpleImputer(missing_values=np.nan, strategy='mean')
#imp = IterativeImputer(max_iter=10,initial_strategy='most_frequent', random_state=0)
#imputed_DF = pd.DataFrame(imp.fit_transform(new_df))
#imputed_DF.columns = new_df.columns
#imputed_DF.index = new_df.index

#Normalize the data for further calculation
#x = imputed_DF.values
#min_max_scaler = preprocessing.MinMaxScaler()
#x_scaled = min_max_scaler.fit_transform(imputed_DF)
#df = pd.DataFrame(x_scaled)
#df.columns = imputed_DF.columns
#df.index = imputed_DF.index


#Calculate the RMSE score
#df['RMSE'] = pd.Series((df.iloc[:,1:]**2).sum(1).pow(1/2))
sim = cosine_similarity(main_frame)
#sim = pearsonr(main_frame)
df1 = pd.DataFrame(sim)
df1.columns = main_frame.index
df1.index = main_frame.index

print(df1)
print(df1.corr(method='pearson'))

#df1.to_csv('Cosine_similarity_output.csv')
'''
rng = np.random.RandomState(10)
a = np.hstack((rng.normal(size=1000),rng.normal(loc=5, scale=2, size=1000)))
plt.hist(a, bins='auto')
plt.title("Histogram with 'auto' bins")
plt.show()
'''