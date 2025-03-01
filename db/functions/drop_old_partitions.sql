CREATE OR REPLACE FUNCTION drop_old_partitions() RETURNS void AS $$
DECLARE
    partition_name TEXT;
    drop_date DATE;
BEGIN
    -- Find the oldest partition to drop (3 months ago)
    drop_date := date_trunc('month', now()) - interval '3 months';
    partition_name := format('crypto_prices_%s', to_char(drop_date, 'YYYY_MM'));

    -- Check if partition exists before dropping
    IF EXISTS (SELECT FROM pg_tables WHERE tablename = partition_name) THEN
        EXECUTE format('DROP TABLE %I;', partition_name);
        RAISE NOTICE 'Dropped partition: %', partition_name;
    ELSE
        RAISE NOTICE 'Partition % does not exist, skipping...', partition_name;
    END IF;
END $$ LANGUAGE plpgsql;