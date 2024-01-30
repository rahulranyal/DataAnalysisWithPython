import pandas as pd 
import numpy as np
import requests
from io import BytesIO
import matplotlib as plt 
from matplotlib import pyplot 

file_path="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
response = requests.get(file_path)
df = pd.read_csv(BytesIO(response.content),names=headers)
df.replace('?',np.NaN, inplace=True)

#Check Missing values 
missing_data = df.isnull()
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print("")

#Replacing with mean value 
avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0)
df["normalized-losses"].replace(np.nan, avg_norm_loss, inplace=True)

#Replacing with most frequent value 
most_frequent_doors = df['num-of-doors'].value_counts().idxmax()
df['num-of-doors'].replace(np.nan,most_frequent_doors, inplace=True)

#Convert Data types 
df[['bore','stroke']] =df[['bore','stroke']].astype("float")

#data-transfromation 
df['city-L/100km'] = 235/df['city-mpg']

#data normalisation 
df['length'] = df['length']/df['length'].max() 

#Convert data to correct format and binning  
mean_horsepower = df['horsepower'].astype("float").mean(axis=0) 
df['horsepower'].replace(np.nan,mean_horsepower, inplace=True)
df['horsepower'] = df['horsepower'].astype(int,copy=True)

bins = np.linspace(min(df['horsepower']),max(df['horsepower']),4)
group_name = ['Low','Medium','High']
df['horsepower-binned'] = pd.cut(df['horsepower'],bins, labels=group_name,include_lowest=True)
print(df[['horsepower','horsepower-binned']].head())
print(df['horsepower-binned'].value_counts())

pyplot.bar(group_name, df["horsepower-binned"].value_counts())

# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")


plt.pyplot.hist(df["horsepower"], bins = 3)

# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

dummy_variables_1 = pd.get_dummies(df['fuel-type'])
df = pd.concat([df,dummy_variables_1],axis=1)
df.to_csv('clean_df.csv')

