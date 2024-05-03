BEGIN;

-- Insert custom categories for user ID 1
INSERT INTO public."Category" (user_id, category_name)
VALUES
    (1, 'Rent'),
    (1, 'Utilities'),
    (1, 'Transportation'),
    (1, 'Entertainment'),
    (1, 'Shopping');

-- Insert budgets for user ID 1
INSERT INTO public."Budget" (user_id, category_id, total_amount, current_amount, start_date, end_date)
VALUES
    (1, 1, 1000.00, 1000.00, '2024-05-03', '2024-06-30'),
    (1, 2, 500.00, 500.00, '2024-05-03', '2024-06-30'),
    (1, 3, 200.00, 200.00, '2024-05-03', '2024-06-30'),
    (1, 4, 300.00, 300.00, '2024-05-03', '2024-06-30'),
    (1, 5, 400.00, 400.00, '2024-05-03', '2024-06-30'),
    (1, 6, 600.00, 600.00, '2024-05-03', '2024-06-30'),
    (1, 7, 250.00, 250.00, '2024-05-03', '2024-06-30'),
    (1, 8, 150.00, 150.00, '2024-05-03', '2024-06-30');

-- Insert expenses for user ID 1
INSERT INTO public."Expense" (user_id, category_id, amount, description, date)
VALUES
    (1, 1, 800.00, 'Monthly rent payment', '2024-05-03'),
    (1, 2, 120.00, 'Electricity bill', '2024-05-05'),
    (1, 2, 80.00, 'Water bill', '2024-05-10'),
    (1, 3, 50.00, 'Gas for car', '2024-05-08'),
    (1, 3, 30.00, 'Public transportation', '2024-05-15'),
    (1, 4, 40.00, 'Movie tickets', '2024-05-12'),
    (1, 4, 60.00, 'Dinner at a restaurant', '2024-05-20'),
    (1, 5, 100.00, 'Clothing purchase', '2024-05-18'),
    (1, 5, 50.00, 'Online shopping', '2024-05-25'),
    (1, 6, 120.00, 'Grocery shopping', '2024-05-05'),
    (1, 6, 90.00, 'Grocery shopping', '2024-05-15'),
    (1, 6, 100.00, 'Grocery shopping', '2024-05-25'),
    (1, 7, 50.00, 'Fast food', '2024-05-10'),
    (1, 7, 80.00, 'Dining out with friends', '2024-05-22'),
    (1, 8, 30.00, 'Haircut', '2024-05-08'),
    (1, 8, 50.00, 'Skincare products', '2024-05-20');

END;