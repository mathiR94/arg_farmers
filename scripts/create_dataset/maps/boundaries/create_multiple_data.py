#create multiple datasets in order to get shapefiles, each one with a different geometry

import os
import pandas as pd
import shapely as sh
from shapely import wkt
import geopandas as gpd
import numpy as np


project = os.path.join(Dropbox, "arg_framers_data")

data_frame_path = "C:/Users/ribei/Dropbox/arg_farmers_data/data/intermediate_data/maps/temp_distance_data/distance_data.csv"

distance_data = pd.read_csv(data_frame_path)

#we are going to create two differents datasets:
    
    # 1: with the lines that connects the centroid and their nearest point to the borders (lines_data)
    
    # 2: with the centroids of each department (points_data)

line = [wkt.loads(i) for i in distance_data['line']]

lines_data = gpd.GeoDataFrame(distance_data[['border', 'depto', 'provincia', 'distance_km']], geometry = line ,crs = 'EPSG:4326')


points = [wkt.loads(i) for i in distance_data['point1']]

points_data = gpd.GeoDataFrame(distance_data[['border', 'depto', 'provincia', 'distance_km']], geometry = points, crs = 'EPSG:4326')


lines_data.to_file("C:/Users/ribei/Dropbox/arg_farmers_data/data/intermediate_data/maps/temp_distance_data/lines_data.shp")

points_data.to_file("C:/Users/ribei/Dropbox/arg_farmers_data/data/intermediate_data/maps/temp_distance_data/points_data.shp")
