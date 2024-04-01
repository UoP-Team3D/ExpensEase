from flask import current_app

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