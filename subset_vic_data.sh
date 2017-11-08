#! bin/bash

shapedir=/Volumes/Users/Theo/projects/Budyko_vic/data/WSC_basins/HUC8/

raster=/Volumes/Users/Theo/projects/Budyko_vic/grass_data/ascii_data/simulation.tif

cd $shapedir

shapes=`ls *.shp` #grab all the shapefiles

# cut the simulation by the us outline

#gdalwarp -t_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -r 'near' -tap -tr 0.0625 0.0625 -cutline ../../ecoregions/cb_2013_us_nation_20m.shp -crop_to_cutline -dstnodata -9999 -overwrite $raster ../../simulation_CONUS.tif

echo 'made it'

for shape in $shapes; do
	
	filename=$(basename $shape) # grab the basename of the file
	filebody=${filename%.*} # grab the name without the extension
	
	gdalwarp -t_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -r 'near' -tap -tr 0.0625 0.0625 -cutline $shape -crop_to_cutline -dstnodata -9999 -overwrite ../../simulation_CONUS.tif ../../WSC_basin_tiffs/$filebody.tif

	echo $filebody' Done!'

done

