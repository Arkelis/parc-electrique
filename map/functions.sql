-- from https://github.com/openinframap/openinframap
-- Convert a power value into a numeric value in watts
CREATE OR REPLACE FUNCTION normalize_power(value TEXT) RETURNS NUMERIC
PARALLEL SAFE
IMMUTABLE
RETURNS NULL ON NULL INPUT
AS $$
DECLARE
  parts TEXT[];
  val NUMERIC;
BEGIN
  parts := regexp_matches(upper(value), '([0-9]+[\.,]?[0-9]*)[ ]?([KMG]?W)?', '');
  val := replace(parts[1], ',', '.');
  IF parts[2] = 'KW' THEN
    val := val * 1e3;
  ELSIF parts[2] = 'MW' THEN
    val := val * 1e6;
  ELSIF parts[2] = 'GW' THEN
    val := val * 1e9;
  END IF;
  RETURN val;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION simplify_boundary(g1 geometry)
    RETURNS geometry
    LANGUAGE plpgsql
    IMMUTABLE STRICT
    PARALLEL UNSAFE AS $$
begin
    return st_buffer(st_concavehull(g1, 0.95), 10);
EXCEPTION
    WHEN SQLSTATE 'XX000' THEN
        RETURN st_buffer(g1, 10);
end
$$;

CREATE MATERIALIZED VIEW power_plant_relations AS
    SELECT rel.osm_id, simplify_boundary(ST_Collect(mem.geometry)) AS geometry, 
        rel.name, rel.output, rel.source
        FROM osm_power_plants_relations as rel, osm_power_plants_relation_members as mem
        WHERE mem.osm_id = rel.osm_id
        GROUP BY rel.osm_id, rel.name, rel.output, rel.source;