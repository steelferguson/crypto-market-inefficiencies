-- db/functions/create_monthly_partition.sql

CREATE OR REPLACE FUNCTION create_monthly_partition() RETURNS void AS $$
DECLARE
    new_partition TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    -- Get the first day of next month
    start_date := date_trunc('month', now()) + interval '1 month';
    end_date := start_date + interval '1 month';

    -- Format partition table name
    new_partition := format('crypto_prices_%s', to_char(start_date, 'YYYY_MM'));

    -- Create partition
    EXECUTE format(
        'CREATE TABLE %I PARTITION OF crypto_prices FOR VALUES FROM (%L) TO (%L);',
        new_partition, start_date, end_date
    );

    RAISE NOTICE 'Created partition: %', new_partition;
END $$ LANGUAGE plpgsql;