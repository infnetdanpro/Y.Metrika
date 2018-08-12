# Y.Metrika
requests, json, psycopg2

For work use PostgreSQL:

CREATE TABLE public.stats
(
    id integer NOT NULL DEFAULT nextval('stats_id_seq'::regclass),
    keyword text COLLATE pg_catalog."default",
    searchsystem text COLLATE pg_catalog."default",
    visit text COLLATE pg_catalog."default",
    bouncerate text COLLATE pg_catalog."default",
    deeppage text COLLATE pg_catalog."default",
    visittime text COLLATE pg_catalog."default",
    CONSTRAINT stats_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.stats
    OWNER to postgres;
