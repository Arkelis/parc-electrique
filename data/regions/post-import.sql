-- Use 3857 geometry
ALTER TABLE osm_regions
ALTER COLUMN geom
    type geometry(MULTIPOLYGON,3857)
    USING ST_Multi(ST_Transform(geom, 3857));

-- Add region id fk in osm_power_plants table
ALTER TABLE osm_power_plants
ADD COLUMN region_gid bigint,
ADD CONSTRAINT power_plant_region_fk
  FOREIGN KEY(region_gid) REFERENCES osm_regions(gid);
