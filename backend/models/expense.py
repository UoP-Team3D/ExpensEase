from flask import current_app
from models.budget import Budget

class Expense:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_expenses(self, user_id, category=None, start_date=None, end_date=None, sort_by=None, sort_order=None, page=1, per_page=10):
        with self.db_connection.cursor() as cursor:
            query = """
            SELECT e.expense_id, e.amount, e.description, e.date, c.category_name
            FROM public."Expense" e
            JOIN public."Category" c ON e.category_id = c.category_id
            WHERE e.user_id = %s
            """
            params = [user_id]

            if category:
                query += " AND c.category_name = %s"
                params.append(category)

            if start_date:
                query += " AND e.date >= %s"
                params.append(start_date)

            if end_date:
                query += " AND e.date <= %s"
                params.append(end_date)

            sort_query = ""
            if sort_by:
                if sort_by == "amount":
                    sort_query = " ORDER BY e.amount"
                elif sort_by == "date":
                    sort_query = " ORDER BY e.date"
                elif sort_by == "category":
                    sort_query = " ORDER BY c.category_name"

                if sort_order == "desc":
                    sort_query += " DESC"
                else:
                    sort_query += " ASC"

            query += sort_query

            offset = (page - 1) * per_page
            query += " LIMIT %s OFFSET %s"
            params.extend([per_page, offset])

            cursor.execute(query, params)
            expenses = cursor.fetchall()

            expense_list = []
            for expense in expenses:
                expense_list.append({
                    "expense_id": expense[0],
                    "amount": float(expense[1]),
                    "description": expense[2],
                    "date": expense[3].strftime('%Y-%m-%d'),
                    "category": expense[4]
                })

            return expense_list

    def update_expense(self, expense_id, user_id, description=None, amount=None, category=None):
        with self.db_connection.cursor() as cursor:
            # Retrieve the old expense amount, category, and date
            query = """
            SELECT amount, category_id, date
            FROM public."Expense"
            WHERE expense_id = %s AND user_id = %s
            """
            cursor.execute(query, (expense_id, user_id))
            old_expense = cursor.fetchone()

            if old_expense:
                old_amount, old_category_id, old_expense_date = old_expense
                # Update the expense
                query = """
                UPDATE public."Expense"
                SET description = COALESCE(%s, description),
                    amount = COALESCE(%s, amount),
                    category_id = COALESCE((
                        SELECT category_id
                        FROM public."Category"
                        WHERE category_name = %s
                    ), category_id)
                WHERE expense_id = %s AND user_id = %s
                RETURNING expense_id, amount, category_id, date;
                """
                params = [description, amount, category, expense_id, user_id]
                cursor.execute(query, params)
                updated_expense = cursor.fetchone()
                self.db_connection.commit()

                if updated_expense:
                    new_amount, new_category_id, new_expense_date = updated_expense[1], updated_expense[2], updated_expense[3]
                    # Update the budget
                    budget_model = Budget(self.db_connection)
                    budget_model.update_budget_amount(user_id, old_category_id, -old_amount, old_expense_date)  # Revert the old amount
                    budget_model.update_budget_amount(user_id, new_category_id, new_amount, new_expense_date)  # Apply the new amount
                    return updated_expense[0]
        return None

    def delete_expense(self, expense_id, user_id):
        with self.db_connection.cursor() as cursor:
            # Retrieve the expense amount and category
            query = """
            SELECT amount, category_id
            FROM public."Expense"
            WHERE expense_id = %s AND user_id = %s
            """
            cursor.execute(query, (expense_id, user_id))
            expense = cursor.fetchone()

            if expense:
                amount, category_id = expense
                # Delete the expense
                query = """
                DELETE FROM public."Expense"
                WHERE expense_id = %s AND user_id = %s
                RETURNING expense_id;
                """
                params = [expense_id, user_id]
                cursor.execute(query, params)
                deleted_expense_id = cursor.fetchone()
                self.db_connection.commit()

                if deleted_expense_id:
                    # Update the budget
                    budget_model = Budget(self.db_connection)
                    budget_model.update_budget_amount(user_id, category_id, -amount, None)  # Revert the amount
                    return deleted_expense_id[0]
        return None

    @staticmethod
    def get_expenses_by_budget(budget_id):
        with current_app.db_connection.cursor() as cursor:
            query = """
            SELECT e.expense_id, e.amount, e.description, e.date, c.category_name
            FROM public."Expense" e
            JOIN public."Category" c ON e.category_id = c.category_id
            WHERE e.user_id = (
                SELECT user_id
                FROM public."Budget"
                WHERE budget_id = %s
            )
            AND e.date >= (
                SELECT start_date
                FROM public."Budget"
                WHERE budget_id = %s
            )
            AND e.date <= (
                SELECT end_date
                FROM public."Budget"
                WHERE budget_id = %s
            )
            """
            cursor.execute(query, (budget_id, budget_id, budget_id))
            expenses = cursor.fetchall()

            expense_list = []
            for expense in expenses:
                expense_list.append(Expense(
                    expense_id=expense[0],
                    amount=float(expense[1]),
                    description=expense[2],
                    date=expense[3].strftime('%Y-%m-%d'),
                    category=expense[4]
                ))

            return expense_list