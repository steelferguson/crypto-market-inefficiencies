--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Homebrew)
-- Dumped by pg_dump version 16.8 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: crypto_prices; Type: TABLE; Schema: public; Owner: steelferguson
--

CREATE TABLE public.crypto_prices (
    id integer NOT NULL,
    "timestamp" timestamp without time zone,
    symbol character varying(10),
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric
);


ALTER TABLE public.crypto_prices OWNER TO steelferguson;

--
-- Name: crypto_prices_id_seq; Type: SEQUENCE; Schema: public; Owner: steelferguson
--

CREATE SEQUENCE public.crypto_prices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.crypto_prices_id_seq OWNER TO steelferguson;

--
-- Name: crypto_prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: steelferguson
--

ALTER SEQUENCE public.crypto_prices_id_seq OWNED BY public.crypto_prices.id;


--
-- Name: crypto_prices id; Type: DEFAULT; Schema: public; Owner: steelferguson
--

ALTER TABLE ONLY public.crypto_prices ALTER COLUMN id SET DEFAULT nextval('public.crypto_prices_id_seq'::regclass);


--
-- Name: crypto_prices crypto_prices_pkey; Type: CONSTRAINT; Schema: public; Owner: steelferguson
--

ALTER TABLE ONLY public.crypto_prices
    ADD CONSTRAINT crypto_prices_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

