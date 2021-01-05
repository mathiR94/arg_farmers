
import geopandas as gpd
import fiona
import unidecode as unc
from shapely.geometry import mapping

limits  = gpd.read_file("C:/Users/ribei/Dropbox/arg_farmers_data/data/intermediate_data/maps/raw_maps/arg_limits/linea_de_limite_070111.shp")

#here we construct the borders as unique lines objects#


borders = set(list(limits["gna"]))

#getting the crs of each figure
limits.crs


#setting the schema for each figure
schema = {
    'geometry': 'LineString',
    'properties': {'id': 'int'},
}
             
for i in borders:
    
    j = int(1)
    border = limits[limits["gna"] == str(i)]
    border_u = border.unary_union
    
    file_name = str( "/" + str(i).lower().replace("-", "_").replace(" ", "") + ".shp")
    file_name = unc.unidecode(file_name)
    path = "C:/Users/ribei/Dropbox/arg_farmers_data/data/intermediate_data/maps/raw_maps/arg_limits/inter_prov/" + file_name 
    
    with fiona.open(path, 'w', 'ESRI Shapefile', schema = schema, crs = fiona.crs.from_epsg(4326)) as c:
            c.write({
                'geometry': mapping(border_u),
                'properties': {'id': int(j)},
            })
    j = j + 1    
    
    



