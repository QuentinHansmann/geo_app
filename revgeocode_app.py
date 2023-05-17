import streamlit as st 
import PointInPolygon as pnp
from shapely.geometry import Point, Polygon
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
import csv 
import io
import json 
import pandas as pd 
from bs4 import BeautifulSoup

### Install the drivers that allow to read KML 
fiona.drvsupport.supported_drivers['kml'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'

### Title 
st.title("Is my position inside the polygon ?")

### Functions 

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

############ CODE BODY 
polygon_upload = st.file_uploader("Paste the kml.files of your polygon")

### Conditions for uploading the polygon in KML
if polygon_upload is not None:
    polygon_KML = gpd.read_file(polygon_upload, driver='KML')
    st.markdown("#### Here's the kml file of your polygon upload")
    st.write(polygon_KML)


point_upload = st.file_uploader("Paste the kml.files with your points inside")

### Conditions for uploading the points in KML
if point_upload is not None:
    point_KML = gpd.read_file(point_upload, driver='KML')
    st.markdown("#### Here's the kml file of your point upload")
    st.write(point_KML)

### Conditions for uploading the results    
if point_upload is not None and polygon_upload is not None:
    polygon_checker = polygon_KML.reset_index(drop=True)
    point = point_KML.reset_index(drop=True)
    pip_mask = point.within(polygon_checker.loc[0, 'geometry'])
    point["is_inside"] = pip_mask
    point = point.drop(['Description'], axis=1)

    ### Display a map  
    
    ### Convert into df
    df = pd.DataFrame(point)
    df['geometry'] = df['geometry'].astype('str')
    df['words_with_dot'] = df['geometry'].str.findall(r'\w+\.\w+')
    df['words_with_dot'] = df['words_with_dot'].astype ('str')

    ### Create empty list for append latitude and longitude 
    latitude = []
    longitude = []
    
    ### Iteration through word_with_dots 
    for i in df['words_with_dot']:
        parts_item = i.split(",")
        latitude.append(parts_item[0])
        longitude.append(parts_item[1])

    df = df.reset_index(drop=True)

    df['latitude'] = latitude
    df['longitude'] = longitude

    df['latitude']= df['latitude'].astype('str')
    df['longitude']=df['longitude'].astype('str')

    df['latitude'] = df['latitude'].str.replace("'","").str.replace("[", "")
    df['longitude'] = df['longitude'].str.replace("'","").str.replace("]", "")

    df['latitude'] = df['latitude'].astype ('float64')
    df['longitude'] = df['longitude'].astype ('float64')

    df = df.drop(['geometry','words_with_dot'], axis=1)

    ### Show the results 
    st.markdown("#### Here's the results")
    st.write(df)

### Convert into csv. + Button to download the code
    csv_result = convert_df(df)
    st.download_button("Download", csv_result, 'results.csv', 'text/csv')
