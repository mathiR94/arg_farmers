#here we are going to measure distance and create lines for each distance 
# in order to create maps for descriptive purpuses

import geopandas as gpd


import os
import shapely as sh
import unidecode as unc
import pandas as pd
import pyproj


project = os.path.join(Dropbox, "arg_farmers_data")



arg_2 = gpd.read_file(os.path.join(Dropbox, "arg_farmers_data", "data", "intermediate_data", "maps", "raw_maps", "arg_limits", "gadm36_ARG_2.shp"))

#here we create the centroids
arg_2["centroid"] = arg_2["geometry"].centroid

# just for check:
test = gpd.read_file(os.path.join(Dropbox, "arg_farmers_data", "data", "intermediate_data", "maps", "raw_maps","arg_limits","inter_prov", "tucuman_catamarca.shp")) 


#this is the function we have to use in order to get a shapely format of linestring 
sh.geometry.shape(sh.geometry.mapping(test)['features'][0]['geometry'])

test.crs == arg_2.crs


#now we create a function that will calculate the distance and create a line for each departamento in order to get the graphic and the data of the nearest distance to each interprovincial border

#------------function---------------------------------------------------------#
def dist(ob1, ob2, name1, name2):
    
    
    distance = ob1.distance(ob2)    
    p1 = sh.ops.nearest_points(ob1, ob2)[0]
    p2 = sh.ops.nearest_points(ob1, ob2)[1]
    line =  sh.geometry.linestring.LineString((p1,p2))
    
    geod = pyproj.Geod(ellps = 'WGS84')
    real_distance = geod.inv(p1.x, p1.y, p2.x, p2.y)
    
    
    res = {"object1" : name1 , "object2" : name2, "distance" : distance, 'distance_km':real_distance[2]/1000, "point1":p1, "point2" : p2 , "line": line}    
    
    return res

#---------------------------------for loop------------------------------------#
files = os.listdir(os.path.join(project, "data", "intermediate_data", "maps", "raw_maps","arg_limits","inter_prov"))

names = [file for file in files if "shp" in file]
#------------------------------------------------------------------------------#

final_data = []

for i in arg_2["NAME_1"].unique():
    
    h = unc.unidecode(i.lower().replace(" ", ""))
    borders = [name for name in names if h in name]

    for j in borders:
       
       
       bord_shp = gpd.read_file(os.path.join(Dropbox, "arg_farmers_data", "data", "intermediate_data", "maps", "raw_maps","arg_limits","inter_prov", j))
       
       bord_geom = sh.geometry.shape(sh.geometry.mapping(bord_shp)['features'][0]['geometry'])
       
     
       for t,u in zip(arg_2[arg_2["NAME_1"]==i]["centroid"], arg_2[arg_2["NAME_1"]==i]['NAME_2']):
           
           bord = str(j.replace(".shp", ""))
           depto = str(unc.unidecode(u.lower().replace(" ", "_")))
           
           
           output = dist(t, bord_geom, depto, bord)
           output['provincia'] = unc.unidecode(i.lower().replace(" ", "_"))
           
           final_data.append(output)
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#


# we fix the keys for making the dataframe
for e in final_data:
    e['depto'] = e.pop('object1')  
    e['border'] = e.pop('object2')
    

# here we create the data frame 
dataframe = pd.DataFrame()
for i in final_data[0].keys():
    num = 0
    dataframe.insert(int(num), str(i), pd.Series([ob[str(i)] for ob in final_data ]))
    num += 1


data_frame_path = os.path.join(project, "data", "intermediate_data", "maps", "temp_distance_data", "distance_data.csv")

dataframe.to_csv(data_frame_path)


