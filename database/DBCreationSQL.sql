BEGIN;

CREATE TABLE IF NOT EXISTS public."Users"
(
    user_id serial NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(40) NOT NULL,
    first_name character varying(20) NOT NULL,
    last_name character varying(20) NOT NULL,
    password character varying(60) NOT NULL,
    pin character varying(4) NOT NULL,
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id),
    CONSTRAINT "Users_username_key" UNIQUE (username),
    CONSTRAINT "Users_email_key" UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public."Category" (
    category_id serial NOT NULL,
    user_id integer,
    category_name character varying(20) NOT NULL,
    is_preset boolean NOT NULL DEFAULT false,
    CONSTRAINT "Category_pkey" PRIMARY KEY (category_id),
    CONSTRAINT "Category_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users" (user_id)
);

CREATE TABLE IF NOT EXISTS public."Budget"
(
    budget_id serial NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    total_amount numeric(8, 2) NOT NULL,
    current_amount numeric(8, 2) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT "Budget_pkey" PRIMARY KEY (budget_id),
    CONSTRAINT "Budget_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users" (user_id),
    CONSTRAINT "Budget_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public."Category" (category_id)
);

CREATE TABLE IF NOT EXISTS public."Expense"
(
    expense_id serial NOT NULL,
    user_id integer NOT NULL,
    category_id integer NOT NULL,
    amount numeric(8, 2) NOT NULL,
    description character varying(200),
    date date NOT NULL,
    CONSTRAINT "Expense_pkey" PRIMARY KEY (expense_id),
    CONSTRAINT "Expense_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users" (user_id),
    CONSTRAINT "Expense_category_id_fkey" FOREIGN KEY (category_id) REFERENCES public."Category" (category_id)
);

ALTER TABLE public."Category"
ADD CONSTRAINT "Category_category_name_key" UNIQUE (category_name);

-- Insert preset categories
INSERT INTO public."Category" (category_name, is_preset)
VALUES ('Groceries', true), ('Eating Out', true), ('Personal Upkeep', true)
ON CONFLICT (category_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS public."Receipt"
(
    receipt_id serial NOT NULL,
    expense_id integer NOT NULL,
    receipt_hash character varying(64) NOT NULL,
    CONSTRAINT "Receipt_pkey" PRIMARY KEY (receipt_id),
    CONSTRAINT "Receipt_expense_id_fkey" FOREIGN KEY (expense_id) REFERENCES public."Expense" (expense_id),
    CONSTRAINT "Receipt_receipt_hash_key" UNIQUE (receipt_hash)
);

ALTER TABLE public."Expense"
ADD COLUMN receipt_hash character varying(64) UNIQUE;

ALTER TABLE public."Receipt"
DROP CONSTRAINT "Receipt_expense_id_fkey",
ADD CONSTRAINT "Receipt_expense_id_fkey"
    FOREIGN KEY (expense_id) REFERENCES public."Expense" (expense_id)
    ON DELETE CASCADE;

END;