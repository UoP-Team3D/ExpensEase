-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."Budget"
(
    budget_id serial NOT NULL,
    total_amount numeric(8, 2) NOT NULL,
    current_amount numeric(8, 2) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    CONSTRAINT "Budget_pkey" PRIMARY KEY (budget_id)
);

CREATE TABLE IF NOT EXISTS public."Category"
(
    category_id serial NOT NULL,
    category_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    user_id integer,
    CONSTRAINT "Category_pkey" PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS public."Expense"
(
    expense_id serial NOT NULL,
    amount numeric(8, 2) NOT NULL,
    description character varying(200) COLLATE pg_catalog."default",
    date date NOT NULL,
    transcription_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    user_id integer NOT NULL,
    category_id integer,
    CONSTRAINT "Expense_pkey" PRIMARY KEY (expense_id)
);

CREATE TABLE IF NOT EXISTS public."Income"
(
    income_id serial NOT NULL,
    amount numeric(8, 2) NOT NULL,
    source character varying(200) COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    recurrence integer,
    user_id integer NOT NULL,
    CONSTRAINT "Income_pkey" PRIMARY KEY (income_id)
);

CREATE TABLE IF NOT EXISTS public."Users"
(
    user_id serial NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    email character varying(40) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(60) COLLATE pg_catalog."default" NOT NULL,
    pin character varying(4) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id)
);

ALTER TABLE IF EXISTS public."Budget"
    ADD CONSTRAINT category_id FOREIGN KEY (category_id)
    REFERENCES public."Category" (category_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Budget"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."Users" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Category"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."Users" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS fki_user_id
    ON public."Category"(user_id);


ALTER TABLE IF EXISTS public."Expense"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."Users" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Income"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."Users" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;