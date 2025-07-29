--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 17.0

-- Started on 2025-07-24 19:23:08 IST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 32827)
-- Name: bill; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.bill (
    id integer NOT NULL,
    bill_number character varying(50) NOT NULL,
    customer_id integer NOT NULL,
    bill_date date DEFAULT CURRENT_DATE NOT NULL,
    due_date date,
    subtotal numeric(12,2) DEFAULT 0 NOT NULL,
    discount_type character varying(20) DEFAULT 'none'::character varying,
    discount_value numeric(10,2) DEFAULT 0,
    discount_amount numeric(12,2) DEFAULT 0,
    cgst_amount numeric(12,2) DEFAULT 0 NOT NULL,
    sgst_amount numeric(12,2) DEFAULT 0 NOT NULL,
    igst_amount numeric(12,2) DEFAULT 0 NOT NULL,
    total_amount numeric(12,2) DEFAULT 0 NOT NULL,
    notes text,
    status character varying(20) DEFAULT 'Draft'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bill OWNER TO gst_user;

--
-- TOC entry 215 (class 1259 OID 32826)
-- Name: bill_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.bill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bill_id_seq OWNER TO gst_user;

--
-- TOC entry 3876 (class 0 OID 0)
-- Dependencies: 215
-- Name: bill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.bill_id_seq OWNED BY public.bill.id;


--
-- TOC entry 218 (class 1259 OID 32855)
-- Name: bill_item; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.bill_item (
    id integer NOT NULL,
    bill_id integer NOT NULL,
    product_id integer,
    product_name character varying(200) NOT NULL,
    description text,
    hsn_code character varying(10) NOT NULL,
    quantity numeric(10,3) DEFAULT 1 NOT NULL,
    unit character varying(20) DEFAULT 'Nos'::character varying,
    rate numeric(10,2) NOT NULL,
    amount numeric(12,2) NOT NULL,
    gst_rate numeric(5,2) NOT NULL,
    cgst_amount numeric(12,2) DEFAULT 0 NOT NULL,
    sgst_amount numeric(12,2) DEFAULT 0 NOT NULL,
    igst_amount numeric(12,2) DEFAULT 0 NOT NULL
);


ALTER TABLE public.bill_item OWNER TO gst_user;

--
-- TOC entry 217 (class 1259 OID 32854)
-- Name: bill_item_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.bill_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bill_item_id_seq OWNER TO gst_user;

--
-- TOC entry 3877 (class 0 OID 0)
-- Dependencies: 217
-- Name: bill_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.bill_item_id_seq OWNED BY public.bill_item.id;


--
-- TOC entry 220 (class 1259 OID 32880)
-- Name: bill_sequence; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.bill_sequence (
    id integer NOT NULL,
    year integer NOT NULL,
    sequence_number integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.bill_sequence OWNER TO gst_user;

--
-- TOC entry 219 (class 1259 OID 32879)
-- Name: bill_sequence_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.bill_sequence_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bill_sequence_id_seq OWNER TO gst_user;

--
-- TOC entry 3878 (class 0 OID 0)
-- Dependencies: 219
-- Name: bill_sequence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.bill_sequence_id_seq OWNED BY public.bill_sequence.id;


--
-- TOC entry 224 (class 1259 OID 32907)
-- Name: categories; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    category_name character varying(100) NOT NULL,
    date_added timestamp without time zone,
    date_updated timestamp without time zone
);


ALTER TABLE public.categories OWNER TO gst_user;

--
-- TOC entry 223 (class 1259 OID 32906)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO gst_user;

--
-- TOC entry 3879 (class 0 OID 0)
-- Dependencies: 223
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 210 (class 1259 OID 32786)
-- Name: company; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.company (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    address text NOT NULL,
    gst_number character varying(15) NOT NULL,
    tan_number character varying(10),
    logo_filename character varying(255),
    state_code character varying(2) NOT NULL,
    custom_fields json DEFAULT '{}'::json,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.company OWNER TO gst_user;

--
-- TOC entry 209 (class 1259 OID 32785)
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.company_id_seq OWNER TO gst_user;

--
-- TOC entry 3880 (class 0 OID 0)
-- Dependencies: 209
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.company_id_seq OWNED BY public.company.id;


--
-- TOC entry 212 (class 1259 OID 32798)
-- Name: customer; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.customer (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(120),
    phone character varying(15),
    address text,
    gst_number character varying(15),
    state_code character varying(2),
    is_guest boolean DEFAULT false,
    custom_fields json DEFAULT '{}'::json,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customer OWNER TO gst_user;

--
-- TOC entry 211 (class 1259 OID 32797)
-- Name: customer_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_id_seq OWNER TO gst_user;

--
-- TOC entry 3881 (class 0 OID 0)
-- Dependencies: 211
-- Name: customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.id;


--
-- TOC entry 214 (class 1259 OID 32813)
-- Name: product; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    hsn_code character varying(10) NOT NULL,
    gst_rate numeric(5,2) DEFAULT 18.0 NOT NULL,
    unit character varying(20) DEFAULT 'Nos'::character varying,
    custom_fields json DEFAULT '{}'::json,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    category character varying(100) DEFAULT 'General'::character varying
);


ALTER TABLE public.product OWNER TO gst_user;

--
-- TOC entry 213 (class 1259 OID 32812)
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_id_seq OWNER TO gst_user;

--
-- TOC entry 3882 (class 0 OID 0)
-- Dependencies: 213
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- TOC entry 222 (class 1259 OID 32890)
-- Name: users; Type: TABLE; Schema: public; Owner: gst_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    phone character varying(15),
    role character varying(20) DEFAULT 'user'::character varying NOT NULL,
    is_active boolean DEFAULT true,
    last_login timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO gst_user;

--
-- TOC entry 221 (class 1259 OID 32889)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: gst_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO gst_user;

--
-- TOC entry 3883 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gst_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3678 (class 2604 OID 32830)
-- Name: bill id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill ALTER COLUMN id SET DEFAULT nextval('public.bill_id_seq'::regclass);


--
-- TOC entry 3691 (class 2604 OID 32858)
-- Name: bill_item id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_item ALTER COLUMN id SET DEFAULT nextval('public.bill_item_id_seq'::regclass);


--
-- TOC entry 3697 (class 2604 OID 32883)
-- Name: bill_sequence id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_sequence ALTER COLUMN id SET DEFAULT nextval('public.bill_sequence_id_seq'::regclass);


--
-- TOC entry 3704 (class 2604 OID 32910)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 3662 (class 2604 OID 32789)
-- Name: company id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.company ALTER COLUMN id SET DEFAULT nextval('public.company_id_seq'::regclass);


--
-- TOC entry 3666 (class 2604 OID 32801)
-- Name: customer id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.customer ALTER COLUMN id SET DEFAULT nextval('public.customer_id_seq'::regclass);


--
-- TOC entry 3671 (class 2604 OID 32816)
-- Name: product id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- TOC entry 3699 (class 2604 OID 32893)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3712 (class 2606 OID 32848)
-- Name: bill bill_bill_number_key; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill
    ADD CONSTRAINT bill_bill_number_key UNIQUE (bill_number);


--
-- TOC entry 3716 (class 2606 OID 32867)
-- Name: bill_item bill_item_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_item
    ADD CONSTRAINT bill_item_pkey PRIMARY KEY (id);


--
-- TOC entry 3714 (class 2606 OID 32846)
-- Name: bill bill_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill
    ADD CONSTRAINT bill_pkey PRIMARY KEY (id);


--
-- TOC entry 3718 (class 2606 OID 32886)
-- Name: bill_sequence bill_sequence_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_sequence
    ADD CONSTRAINT bill_sequence_pkey PRIMARY KEY (id);


--
-- TOC entry 3728 (class 2606 OID 32912)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 3706 (class 2606 OID 32796)
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- TOC entry 3708 (class 2606 OID 32809)
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- TOC entry 3710 (class 2606 OID 32825)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- TOC entry 3720 (class 2606 OID 32888)
-- Name: bill_sequence unique_year_sequence; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_sequence
    ADD CONSTRAINT unique_year_sequence UNIQUE (year);


--
-- TOC entry 3722 (class 2606 OID 32905)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3724 (class 2606 OID 32901)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3726 (class 2606 OID 32903)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3729 (class 2606 OID 32849)
-- Name: bill bill_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill
    ADD CONSTRAINT bill_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);


--
-- TOC entry 3730 (class 2606 OID 32868)
-- Name: bill_item bill_item_bill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_item
    ADD CONSTRAINT bill_item_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES public.bill(id);


--
-- TOC entry 3731 (class 2606 OID 32873)
-- Name: bill_item bill_item_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gst_user
--

ALTER TABLE ONLY public.bill_item
    ADD CONSTRAINT bill_item_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


-- Completed on 2025-07-24 19:23:08 IST

--
-- PostgreSQL database dump complete
--

