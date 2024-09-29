# Libraries
import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import st_folium
import branca.colormap as cm

# Title of the app
st.title("Ethnicity and Unequal Ageing in Rotherham and Sheffield")
st.write("A mapping dashboard that presents data on ethnicity and ageing in Sheffield and Rotherham. The dashboard uses data from the 2021 Census.")

# Load LSOA vector files
gdf = gpd.read_file("lsoas.geojson")
gdf = gdf[gdf.geometry.notnull() & gdf.is_valid]

# Load Census datasets for mapping
ethnicity_df = pd.read_csv("data/ethnicity_lsoa.csv")
ageing_df = pd.read_csv("data/age_band_lsoa.csv")

# Sidebar for user selection
st.sidebar.header("Data Selection")
data_choice = st.sidebar.selectbox("Select data to visualize", ("Ethnicity", "Ageing"))

# Select the appropriate DataFrame based on user selection
if data_choice == "Ethnicity":
    df = ethnicity_df
    # Create a colormap (continuous color scale)
    min_value = 0
    max_value = 100
else:
    df = ageing_df
    # Create a colormap (continuous color scale)
    min_value = 0
    max_value = 67

st.write(min_value)
st.write(max_value)

# Merge GeoDataFrame with the selected DataFrame based on a common key
common_key = "lsoa21cd"  # Change this to the actual key in your data
# merged_gdf = gdf.merge(df, how="left", left_on=common_key, right_on=common_key)
merged_gdf = gdf.merge(df, on='lsoa21cd', how='left', validate="one_to_one") # Merge
merged_gdf = merged_gdf.dropna(subset=['geometry']) # Check geometries are valid

# Select the column for displaying data
# Ensure that the user selects the column before it's used
data_column = st.selectbox('Select a column to display on the map', merged_gdf.columns)

# Ensure the data column is numeric (convert if necessary)
merged_gdf[data_column] = pd.to_numeric(merged_gdf[data_column], errors='coerce')

# Check for non-null values in the selected data column
non_null_values = merged_gdf[data_column].notnull().sum()
st.write(f"Number of non-null values in {data_column}: {non_null_values}")

# Remove rows with NaN values in the selected data column or missing geometries
merged_gdf = merged_gdf.dropna(subset=[data_column])
merged_gdf = merged_gdf[merged_gdf.geometry.notnull()]

# Print unique values for debugging
st.write(f"Unique values in {data_column}: {merged_gdf[data_column].unique()}")

# Dynamically calculate min and max values for the selected data column
min_value2 = merged_gdf[data_column].min()
max_value2 = merged_gdf[data_column].max()

st.write(min_value2)
st.write(max_value2)

# Use a linear colormap (e.g., Viridis)
colormap = cm.LinearColormap(colors=['blue', 'green', 'yellow', 'orange', 'red'], vmin=min_value, vmax=max_value)

# Calculate the centroid for the map center
centroid_lat = '53.394418'
centroid_lon = '-1.429725'

# Create a base folium map
m = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=10)

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
colormap.caption = f"{data_column} Percentage"
m.add_child(colormap)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

