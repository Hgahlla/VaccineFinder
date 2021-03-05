CREATE TABLE location (
	location_id SERIAL PRIMARY KEY,
	city VARCHAR(30) UNIQUE NOT NULL,
	state CHAR(2) NOT NULL,
	latitude DECIMAL(9,7),
	longitude DECIMAL(10,7),
	status VARCHAR(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.location
(
    location_id integer NOT NULL DEFAULT nextval('location_location_id_seq'::regclass),
    city character varying(30) COLLATE pg_catalog."default" NOT NULL,
    state character(2) COLLATE pg_catalog."default" NOT NULL,
    latitude numeric(9,7),
    longitude numeric(10,7),
    status character varying(12) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT location_pkey PRIMARY KEY (location_id),
    CONSTRAINT location_city_key UNIQUE (city)
);

TABLESPACE pg_default;

ALTER TABLE public.location
    OWNER to postgres;