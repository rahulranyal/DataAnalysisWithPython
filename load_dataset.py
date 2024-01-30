import pandas as pd 
import numpy as np 
import requests
from io import BytesIO

file_path="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv" 

#download data from the url 
# from pyodide.http import pyfetch 

# def download(url,filename):
#     response = pyfetch(url)
#     if response.status == 200:
#         with open(filename,"wb") as f:
#             f.write( response.bytes())

response = requests.get(file_path)
if response.status_code ==200:
    df=pd.read_csv(BytesIO(response.content))
    # print(df.head())
else:
    print(f"failed with status code :{response.status_code}")


#Adding Headers to dataframe 
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
print("headers\n", headers)
df.columns = headers 
df.replace('?',np.NaN, inplace=True)
df.dropna(subset=['price'],axis=0)
df.to_csv("auto.csv",index=False)
print(df.dtypes)
print(df.describe(include='all'))
print(df[['make','fuel-type','price']].describe())
print(df.info())






