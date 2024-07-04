DB_USER="${PARC_ELEC_FR_DB_USER:-osm}"
DB_NAME="${PARC_ELEC_FR_DB_NAME:-osm}"
DB_PASSWORD="${PARC_ELEC_FR_DB_PASSWORD:-osm}"
PGPASSWORD=$DB_PASSWORD
DB_HOST="${PARC_ELEC_FR_DB_HOST:-localhost}"
DB_URI="postgis://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME"


# cd data/osm
# imposm import -mapping mapping.yml -read france.osm.pbf && \
# imposm import -mapping mapping.yml -write -connection $DB_URI && \
# imposm import -optimize -mapping mapping.yml -connection $DB_URI && \
# imposm import -deployproduction -mapping mapping.yml -connection $DB_URI

# cd ../..
cd data/regions
shp2pgsql -s 4326 -d regions-20180101.shp public.osm_regions | PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f 'post-import.sql'
