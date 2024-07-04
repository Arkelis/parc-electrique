#!/bin/bash
set -e

createuser --no-superuser --no-createrole --createdb osm
createdb -E UTF8 -O osm osm
psql -d osm -c "CREATE EXTENSION postgis;"
psql -d osm -c "CREATE EXTENSION hstore;"
echo "ALTER USER osm WITH PASSWORD 'osm';" | psql -d osm