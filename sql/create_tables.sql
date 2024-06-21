CREATE TABLE IF NOT EXISTS public.items
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id uuid NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default",
    quantity integer NOT NULL,
    price numeric NOT NULL,
    status character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT items_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.items
    OWNER to postgres;
-- Index: ix_items_id

-- DROP INDEX IF EXISTS public.ix_items_id;

CREATE INDEX IF NOT EXISTS ix_items_id
    ON public.items USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;


CREATE TABLE IF NOT EXISTS public.users
(
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id uuid NOT NULL,
    email character varying COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL,
    password bytea,
    last_login timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;
-- Index: ix_users_id

-- DROP INDEX IF EXISTS public.ix_users_id;

CREATE INDEX IF NOT EXISTS ix_users_id
    ON public.users USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;