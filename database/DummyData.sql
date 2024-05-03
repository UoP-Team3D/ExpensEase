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
(1, 1, 1000.00, 200.00, '2024-01-01', '2024-04-30'),
(1, 2, 500.00, 300.00, '2024-02-01', '2024-05-31'),
(1, 3, 200.00, 120.00, '2024-03-01', '2024-06-30'),
(1, 14, 300.00, 260.00, '2023-12-01', '2024-02-29'),
(1, 15, 400.00, 150.00, '2024-01-15', '2024-04-15');

-- Insert expenses for user ID 1
INSERT INTO public."Expense" (user_id, category_id, amount, description, date)
VALUES
(1, 1, 800.00, 'Monthly rent payment', '2024-01-05'),
(1, 2, 120.00, 'Electricity bill', '2024-02-10'),
(1, 2, 80.00, 'Water bill', '2024-02-15'),
(1, 14, 50.00, 'Gas for car', '2024-03-02'),
(1, 15, 30.00, 'Public transportation', '2024-03-20'),
(1, 17, 40.00, 'Movie tickets', '2024-01-18'),
(1, 2, 60.00, 'Dinner at a restaurant', '2024-02-14'),
(1, 3, 100.00, 'Clothing purchase', '2024-01-25'),
(1, 18, 150.00, 'Online shopping', '2024-04-05');