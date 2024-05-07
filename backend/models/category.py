from flask import current_app

class Category:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_category(self, user_id, category_name):
        with self.db_connection.cursor() as cursor:
            query = """
            INSERT INTO public."Category" (user_id, category_name)
            VALUES (%s, %s)
            RETURNING category_id;
            """
            cursor.execute(query, (user_id, category_name))
            category_id = cursor.fetchone()[0]
            self.db_connection.commit()
        return category_id

    def get_category_by_id(self, category_id):
        with self.db_connection.cursor() as cursor:
            query = """
            SELECT category_id, user_id, category_name, is_preset
            FROM public."Category"
            WHERE category_id = %s;
            """
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()
            if row:
                category = {
                    'category_id': row[0],
                    'user_id': row[1],
                    'category_name': row[2],
                    'is_preset': row[3]
                }
                return category
        return None

    def update_category(self, category_id, category_name):
        with self.db_connection.cursor() as cursor:
            query = """
            UPDATE public."Category"
            SET category_name = %s
            WHERE category_id = %s;
            """
            cursor.execute(query, (category_name, category_id))
            self.db_connection.commit()

    def delete_category(self, category_id):
        with self.db_connection.cursor() as cursor:
            # Delete dependent receipts
            cursor.execute("""
                DELETE FROM public."Receipt"
                WHERE expense_id IN (
                    SELECT expense_id
                    FROM public."Expense"
                    WHERE category_id = %s
                );
            """, (category_id,))
            # Delete dependent expenses
            cursor.execute("""
                DELETE FROM public."Expense"
                WHERE category_id = %s;
            """, (category_id,))
            # Delete dependent budgets
            cursor.execute("""
                DELETE FROM public."Budget"
                WHERE category_id = %s;
            """, (category_id,))
            # Delete the category
            cursor.execute("""
                DELETE FROM public."Category"
                WHERE category_id = %s;
            """, (category_id,))
            self.db_connection.commit()

    def get_categories_by_user(self, user_id):
        with self.db_connection.cursor() as cursor:
            query = """
            SELECT category_id, user_id, category_name, is_preset
            FROM public."Category"
            WHERE user_id = %s OR is_preset = true;
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            categories = []
            for row in rows:
                category = {
                    'category_id': row[0],
                    'user_id': row[1],
                    'category_name': row[2],
                    'is_preset': row[3]
                }
                categories.append(category)
            return categories