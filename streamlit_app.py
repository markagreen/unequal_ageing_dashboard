# Libraries
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Title of the app
st.title("Ethnicity and Unequal Ageing Dashboard")

# Specify the path to the GeoJSON file
geojson_file = "lsoas_dashboard.geojson"  # Make sure this file is in the same directory as your script

# Check if GeoDataFrame loaded correctly
st.write("GeoDataFrame:")
st.write(gdf.head())  # Show the first few rows
st.write("GeoDataFrame Columns:", gdf.columns.tolist())

invalid_geometries = gdf[~gdf.is_valid]
st.write("Invalid Geometries:", invalid_geometries)

# Try to read the GeoJSON file using geopandas
try:
    gdf = gpd.read_file(geojson_file)

    if gdf.crs is not None:
    gdf = gdf.to_crs(epsg=4326)

    # Display a simple dataframe preview
    #st.write("Data Preview:")
    # st.write(gdf.head())

    # Ask user to select the column for displaying data
    data_column = st.selectbox('Select a column to display on the map', gdf.columns)

    # Create a base folium map
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()],
                   zoom_start=10)

    # Add the GeoJSON layer to the map
    folium.GeoJson(gdf, name="Census Data",
                   style_function=lambda feature: {
                       'fillColor': 'blue',
                       'color': 'black',
                       'weight': 0.5,
                       'fillOpacity': 0.7,
                   }).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)

except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")


