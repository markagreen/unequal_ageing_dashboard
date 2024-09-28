# Libraries
import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt 
import numpy as np
import branca.colormap as cm

# Title of the app
st.title("Ethnicity and Unequal Ageing Dashboard")
st.write("A mapping dashboard that presents data on ethnicity and ageing in Sheffield and Rotherham")

# Load LSOA vector files
gdf = gpd.read_file("vector_files/lsoas.geojson")

# Load Census datasets for mapping
ethnicity_df = pd.read_csv("data/ethnicity_lsoa.csv")
ageing_df = pd.read_csv("data/age_band_lsoa.csv")

# Sidebar for user selection
st.sidebar.header("Data Selection")
data_choice = st.sidebar.selectbox("Select data to visualize", ("Ethnicity Data", "Ageing Data"))

# Select the appropriate DataFrame based on user selection
if data_choice == "Ethnicity Data":
    df = ethnicity_df
else:
    df = ageing_df

# Merge GeoDataFrame with the selected DataFrame based on a common key
common_key = "lsoa21cd"  # Change this to the actual key in your data
merged_gdf = gdf.merge(df, how="left", left_on=common_key, right_on=common_key)

# Ask user to select the column for displaying data
data_column = st.selectbox('Select a column to display on the map', merged_gdf.columns)

# Ensure the data column is numeric (convert if necessary)
merged_gdf[data_column] = pd.to_numeric(merged_gdf[data_column], errors='coerce')

# Remove rows with NaN values in the selected data column
merged_gdf = merged_gdf.dropna(subset=[data_column])

# Create a colormap (continuous color scale)
min_value = merged_gdf[data_column].min()
max_value = merged_gdf[data_column].max()

# Use a linear colormap (e.g., Viridis)
colormap = cm.LinearColormap(colors=['blue', 'green', 'yellow', 'orange', 'red'], vmin=min_value, vmax=max_value)

# Create a base folium map
m = folium.Map(location=[merged_gdf.geometry.centroid.y.mean(), merged_gdf.geometry.centroid.x.mean()],
               zoom_start=10)

# Function to assign colors using the colormap
def style_function(feature):
    value = feature['properties'][data_column]
    if pd.notnull(value):
        return {
            'fillColor': colormap(value),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        }
    else:
        return {
            'fillColor': 'gray',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        }

# Add the GeoJSON layer to the map
folium.GeoJson(merged_gdf,
               name="Census Data",
               style_function=style_function).add_to(m)

# Add the colormap as a legend to the map
colormap.caption = f"{data_column} Values"
m.add_child(colormap)

# Display the map in Streamlit
st_folium(m, width=700, height=500)


