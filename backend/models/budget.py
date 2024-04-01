from flask import current_app

class Budget:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_budget(self, user_id, category_id, total_amount, start_date, end_date):
        with self.db_connection.cursor() as cursor:
            query = """
            INSERT INTO public."Budget" (user_id, category_id, total_amount, current_amount, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING budget_id;
            """
            cursor.execute(query, (user_id, category_id, total_amount, total_amount, start_date, end_date))
            budget_id = cursor.fetchone()[0]
            self.db_connection.commit()
        return budget_id

    def get_budget_by_id(self, budget_id):
        with self.db_connection.cursor() as cursor:
            query = """
            SELECT budget_id, user_id, category_id, total_amount, current_amount, start_date, end_date
            FROM public."Budget"
            WHERE budget_id = %s;
            """
            cursor.execute(query, (budget_id,))
            row = cursor.fetchone()
            if row:
                budget = {
                    'budget_id': row[0],
                    'user_id': row[1],
                    'category_id': row[2],
                    'total_amount': float(row[3]),
                    'current_amount': float(row[4]),
                    'start_date': row[5].strftime('%Y-%m-%d'),
                    'end_date': row[6].strftime('%Y-%m-%d')
                }
                return budget
        return None

    def update_budget(self, budget_id, total_amount):
        with self.db_connection.cursor() as cursor:
            query = """
            UPDATE public."Budget"
            SET total_amount = %s, current_amount = %s
            WHERE budget_id = %s;
            """
            cursor.execute(query, (total_amount, total_amount, budget_id))
            self.db_connection.commit()

    def delete_budget(self, budget_id):
        with self.db_connection.cursor() as cursor:
            query = """
            DELETE FROM public."Budget"
            WHERE budget_id = %s;
            """
            cursor.execute(query, (budget_id,))
            self.db_connection.commit()

    def get_budgets_by_user(self, user_id):
        with self.db_connection.cursor() as cursor:
            query = """
            SELECT budget_id, user_id, category_id, total_amount, current_amount, start_date, end_date
            FROM public."Budget"
            WHERE user_id = %s;
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            budgets = []
            for row in rows:
                budget = {
                    'budget_id': row[0],
                    'user_id': row[1],
                    'category_id': row[2],
                    'total_amount': float(row[3]),
                    'current_amount': float(row[4]),
                    'start_date': row[5].strftime('%Y-%m-%d'),
                    'end_date': row[6].strftime('%Y-%m-%d')
                }
                budgets.append(budget)
            return budgets

    def update_budget_amount(self, user_id, category_id, expense_amount, expense_date):
        print(f"Updating budget for user_id: {user_id}, category_id: {category_id}, expense_amount: {expense_amount}, expense_date: {expense_date}")
        with self.db_connection.cursor() as cursor:
            query = """
            UPDATE public."Budget"
            SET current_amount = current_amount - %s
            WHERE user_id = %s
            AND category_id = %s
            AND start_date <= %s
            AND end_date >= %s;
            """
            cursor.execute(query, (expense_amount, user_id, category_id, expense_date, expense_date))
            rows_affected = cursor.rowcount
            print(f"Rows affected by the update query: {rows_affected}")
            self.db_connection.commit()

    @staticmethod
    def get_all_active_budgets():
        with current_app.db_connection.cursor() as cursor:
            query = """
            SELECT budget_id, user_id, category_id, total_amount, current_amount, start_date, end_date
            FROM public."Budget"
            WHERE end_date >= CURRENT_DATE
            """
            cursor.execute(query)
            budgets = cursor.fetchall()

            budget_list = []
            
            for budget in budgets:
                budget_list.append(Budget(
                    budget_id=budget[0],
                    user_id=budget[1],
                    category_id=budget[2],
                    total_amount=float(budget[3]),
                    current_amount=float(budget[4]),
                    start_date=budget[5].strftime('%Y-%m-%d'),
                    end_date=budget[6].strftime('%Y-%m-%d')
                ))

            return budget_list