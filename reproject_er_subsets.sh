#! bin/bash

cd ./data/ecoregions/subsets/

files=`ls *.shp` # get all the shapefiles

for fl in $files; do
	
	filename=$(basename $fl) # grab the basename of the file
	filebody=${filename%.*} # grab the name without the extension
	ogr2ogr -f "ESRI Shapefile" -t_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -a_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -overwrite ./$filebody'_wgs84.shp' $fl
	
done 