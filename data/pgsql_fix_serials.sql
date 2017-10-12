CREATE OR REPLACE FUNCTION fix_serials()
  RETURNS VOID AS $$
DECLARE
  tables_   VARCHAR [] := ARRAY ['tournament', 'participant', 'game', 'deck', 'player'];
  max_value INT := 0;
  t         VARCHAR;
BEGIN

  FOREACH t IN ARRAY tables_
  LOOP
    RAISE NOTICE 'verifying table %', t;
    EXECUTE 'SELECT max(id) FROM ' || t INTO max_value;
    RAISE NOTICE 'max value to table % is %', t, max_value;
    RAISE NOTICE 'changing seq %_id_seq to %', t, (max_value + 1);
    EXECUTE 'ALTER SEQUENCE ' || t || '_id_seq RESTART WITH ' || (max_value + 1);
  END LOOP;
END;
$$ LANGUAGE plpgsql