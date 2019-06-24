#!/usr/bin/python
#
# Created on Sat Jun 22 16:36:50 2019
# Copyright (C) 2019, shaikhr@tcd.ie
# @author: shaikhr
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

#filter for warnings and ignore
warnings.filterwarnings('ignore')

#Load users data from csv
users_df = pd.read_csv('data/CSVs/users.csv', sep=',')
print(users_df.head())

#Load projects data from csv
projects_df = pd.read_csv('data/CSVs/projects.csv', sep=',')
print(projects_df.head())

#Load galleries data from csv
galleries_df = pd.read_csv('data/CSVs/galleries.csv', sep=',')
print(galleries_df.head())

#Load friends data from csv
friends_df = pd.read_csv('data/CSVs/friends.csv', sep=',')
print(friends_df.head())

#Load lovers data from csv
lovers_df = pd.read_csv('data/CSVs/lovers.csv', sep=',')
print(lovers_df.head())

#Load favoriters data from csv
favoriters_df = pd.read_csv('data/CSVs/favoriters.csv', sep=',')
print(favoriters_df.head())

#Load downloaders data from csv
downloaders_df = pd.read_csv('data/CSVs/downloaders.csv', sep=',')
print(downloaders_df.head())

#Load viewers data from csv
viewers_df = pd.read_csv('data/CSVs/viewers.csv', sep=',')
print(viewers_df.head())


'''
rng = np.random.RandomState(10) 
a = np.hstack((rng.normal(size=1000),rng.normal(loc=5, scale=2, size=1000)))
plt.hist(a, bins='auto')
plt.title("Histogram with 'auto' bins")
plt.show()
'''