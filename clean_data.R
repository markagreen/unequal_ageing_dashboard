##################
### Clean data ###
##################

# Libraries
library(sf)


## Output Areas ##

# Load in shapefile of Sheffield and Rotherham
# Shapedfiles are downloaded using https://borders.ukdataservice.ac.uk/ (as can just download Sheffield and Rotherham areas rather than everywhere)
shape <- read_sf('/Users/markagreen/Desktop/eua_dashboard/shapefiles_outputareas/england_oa_2021.shp')

# Load Census data
# Census data are downloaded via https://www.nomisweb.co.uk/sources/census_2021
eth_cen <- read.csv('/Users/markagreen/Desktop/eua_dashboard/Census data/Output Areas/ethnicity_outputarea.csv')

# Merge data together
shape <- merge(shape, eth_cen, by = "oa21cd")

# Tidy
shape$label <- NULL # Delete as not needed
shape$name <- NULL

# Save
st_write(shape, "outputareas.geojson", delete_dsn = TRUE)


## LSOAs ##

# Load data
shape <- read_sf('/Users/markagreen/Desktop/eua_dashboard/shapefiles_lsoa/england_lsoa_2021.shp') # Shapefile
eth_cen <- read.csv('/Users/markagreen/Desktop/eua_dashboard/Census data/LSOAs/ethnicity_lsoa.csv') # Census data

# Merge data together
shape <- merge(shape, eth_cen, by = "lsoa21cd")

# Tidy
shape$label <- NULL # Delete as not needed
shape$name <- NULL
shape$lsoa21nm <- NULL

# Save
st_write(shape, "lsoas_dashboard.geojson", delete_dsn = TRUE)
