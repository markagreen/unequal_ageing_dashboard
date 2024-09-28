# Libraries
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Title of the app
st.title("Ethnicity and Unequal Ageing Dashboard")
st.write("A mapping dashboard that presents data on ethnicity and ageing in Sheffield and Rotherham")

# Specify the path to the GeoJSON file
geojson_file = "lsoas_dashboard.geojson"  # Make sure this file is in the same directory as your script

# Try to read the GeoJSON file using geopandas
try:
    gdf = gpd.read_file(geojson_file)

    # Ask user to select the column for displaying data
    data_column = st.selectbox('Select a column to display on the map', gdf.columns)

    # Create a base folium map
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()],
                   zoom_start=10)

    # Define a color function that maps data values to colors using a colorblind-friendly palette
    def color_function(value):
        if pd.isna(value):  # Handle NaN values
            return 'lightgrey'  # Use light grey for NaN values
        else:
            # Normalize the value for better color mapping
            normalized_value = (value - gdf[data_column].min()) / (gdf[data_column].max() - gdf[data_column].min())
            
            # Create a color palette (3 colors for low, medium, high)
            colors = plt.cm.get_cmap('Set2', 3)  # Using a colorblind-friendly palette
            color = colors(int(normalized_value * (colors.N - 1)))  # Get color from the palette
            
            # Convert RGBA to hex
            return f'#{int(color[0] * 255):02x}{int(color[1] * 255):02x}{int(color[2] * 255):02x}'

    # Add the GeoJSON layer to the map with the dynamic style function
    folium.GeoJson(
        gdf,
        name="Census Data",
        style_function=lambda feature: {
            'fillColor': color_function(feature['properties'][data_column]),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        }
    ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)

except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")


