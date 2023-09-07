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