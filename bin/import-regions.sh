cd data/regions
shp2pgsql -s 4326 -d regions-20180101.shp public.osm_regions | psql -h localhost -U osm -d osm
psql -h localhost -U osm -d osm -f 'post-import.sql'
