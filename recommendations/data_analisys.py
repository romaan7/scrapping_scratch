import pandas as pd
import warnings
import matplotlib.pyplot as plt

#filter for warnings and ignore
warnings.filterwarnings('ignore')
projects_df = pd.read_csv('C:/Users/shaikhr/Downloads/scratch_recommendation/recommendations/data/CSVs/data/CSVs/projects.csv', sep=',',nrows=100)
projects_df['date_created'] = pd.to_datetime(projects_df['date_created'], errors='coerce')
#projects_df['just_date'] = projects_df['date_created'].dt.date
#projects_df = projects_df.drop(columns="date_created")
print(projects_df)
projects_df.set_index('date_created', inplace=True)
projects_df.plot()
projects_df.groupby(projects_df["date_created"].dt.month).count().plot(kind="bar")
