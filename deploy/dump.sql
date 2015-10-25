--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: game_map; Type: TABLE; Schema: public; Owner: agerasym; Tablespace: 
--

CREATE TABLE game_map (
    x integer,
    y integer,
    game_object_id character varying(64)
);


ALTER TABLE public.game_map OWNER TO agerasym;

--
-- Name: game_object; Type: TABLE; Schema: public; Owner: agerasym; Tablespace: 
--

CREATE TABLE game_object (
    id character varying(64) NOT NULL,
    name character varying(50),
    description text
);


ALTER TABLE public.game_object OWNER TO agerasym;

--
-- Data for Name: game_map; Type: TABLE DATA; Schema: public; Owner: agerasym
--

COPY game_map (x, y, game_object_id) FROM stdin;
0	0	Tower123
1	1	Tower2015-10-25 19:48:09.326333+02
2	2	1445795813
3	3	1445796550
\.


--
-- Data for Name: game_object; Type: TABLE DATA; Schema: public; Owner: agerasym
--

COPY game_object (id, name, description) FROM stdin;
Tower123	Tower	tower with cannons
Tower2015-10-25 19:48:09.326333+02	Tower	tower with cannons
1445795813	FireStarter	Thing that makes hell
1445796550	FireStarter	Thing that makes hell
\.


--
-- Name: all_fields_unique; Type: CONSTRAINT; Schema: public; Owner: agerasym; Tablespace: 
--

ALTER TABLE ONLY game_map
    ADD CONSTRAINT all_fields_unique UNIQUE (x, y, game_object_id);


--
-- Name: game_object_pkey; Type: CONSTRAINT; Schema: public; Owner: agerasym; Tablespace: 
--

ALTER TABLE ONLY game_object
    ADD CONSTRAINT game_object_pkey PRIMARY KEY (id);


--
-- Name: game_map_game_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: agerasym
--

ALTER TABLE ONLY game_map
    ADD CONSTRAINT game_map_game_object_id_fkey FOREIGN KEY (game_object_id) REFERENCES game_object(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

