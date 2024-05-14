CREATE TABLE IF NOT EXISTS public.data_2022_oct (
    event_time TIMESTAMP,
    event_type  CHARACTER VARYING(16) NOT NULL,
    product_id INTEGER NOT NULL,
    price FLOAT NOT NULL,
    user_id INTEGER NOT NULL,
    user_session UUID
);

COPY public.data_2022_oct FROM '/tmp/data_2022_oct.csv' DELIMITER ',' CSV HEADER;