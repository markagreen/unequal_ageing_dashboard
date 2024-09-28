# Libraries
import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt 
import numpy as np

# Title of the app
st.title("Ethnicity and Unequal Ageing Dashboard")
st.write("A mapping dashboard that presents data on ethnicity and ageing in Sheffield and Rotherham")

# Load LSOA vector files
gdf = gpd.read_file("vector_files/lsoas.geojson")

# Load Census datasets for mapping
ethnicity_df = pd.read_csv("data/ethnicity_lsoa.csv")
ageing_df = pd.read_csv("data/age_band_lsoa.csv")

# Specify the path to the GeoJSON file
# geojson_file = "lsoas_dashboard.geojson"  # Make sure this file is in the same directory as your script

# Sidebar for user selection
st.sidebar.header("Data Selection")
data_choice = st.sidebar.selectbox("Select data to visualize", ("Ethnicity Data", "Ageing Data"))

# Select the appropriate DataFrame based on user selection
if data_choice == "Ethnicity Data":
    df = ethnicity_df
else:
    df = ageing_df

# Merge GeoDataFrame with the selected DataFrame based on a common key
common_key = "lsoa11cd"  # Change this to the actual key in your data
merged_gdf = gdf.merge(df, how="left", left_on=common_key, right_on=common_key)

# Ask user to select the column for displaying data
data_column = st.selectbox('Select a column to display on the map', merged_gdf.columns)

# Convert the selected column to numeric, coercing errors to NaN
merged_gdf[data_column] = pd.to_numeric(merged_gdf[data_column], errors='coerce')

# Create a base folium map
m = folium.Map(location=[merged_gdf.geometry.centroid.y.mean(), merged_gdf.geometry.centroid.x.mean()], zoom_start=10)

# Define a color function that maps data values to colors using quintiles
def assign_colors(value, bins, colors):
    for i in range(len(bins) - 1):
        if bins[i] <= value < bins[i + 1]:
            return colors[i]
    return 'lightgrey'  # For NaN values or out of bounds

# Create quintile bins
bins = pd.qcut(merged_gdf[data_column].dropna(), 5, duplicates='drop').cat.categories

# Define a color palette with 5 colors (using a colorblind-friendly palette)
colors = ['#FEE08B', '#F46D43', '#D73027', '#A50026', '#313695']  # Adjust this palette as needed

# Add the GeoJSON layer to the map with the dynamic style function
folium.GeoJson(
    merged_gdf,
    name="Census Data",
    style_function=lambda feature: {
        'fillColor': assign_colors(feature['properties'][data_column], bins, colors),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7,
    }
).add_to(m)

# Add a color legend to the map
def add_color_legend(map_object):
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: auto; 
                background: white; z-index:9999; font-size:14px; 
                border:2px solid grey; padding: 10px;">
        <div style="text-align: center; font-weight: bold;">Legend</div>
        <div><i style="background: #FEE08B; width: 20px; height: 20px; display: inline-block;"></i> Low</div>
        <div><i style="background: #F46D43; width: 20px; height: 20px; display: inline-block;"></i> Medium-Low</div>
        <div><i style="background: #D73027; width: 20px; height: 20px; display: inline-block;"></i> Medium</div>
        <div><i style="background: #A50026; width: 20px; height: 20px; display: inline-block;"></i> Medium-High</div>
        <div><i style="background: #313695; width: 20px; height: 20px; display: inline-block;"></i> High</div>
    </div>
    """
    map_object.get_root().html.add_child(folium.Element(legend_html))

# Call the function to add the legend
add_color_legend(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)


