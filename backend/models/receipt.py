from flask import request
import os
from utilities.ocr import OCRProcessor
from utilities.prediction import Predictor
import datetime
from models.budget import Budget
import hashlib

class Receipt:
    """
    Receipt class to handle receipt-related operations in the database.

    Attributes:
        db_connection: A psycopg2 connection object to the PostgreSQL database.
        
    Methods:
        upload_receipt: 
    """ 

    def __init__(self, db_connection):
        """
        Initializes the Receipt class with a database connection.

        Args:
            db_connection: A psycopg2 connection object to the PostgreSQL database.
        """
        self.db_connection = db_connection
        self.ocr_processor = OCRProcessor()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, '..', 'machine', 'model.pkl')
        vectorizer_path = os.path.join(current_dir, '..', 'machine', 'vectorizer.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}, make sure you generate the model first!")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}, make sure you generate the model first!")

        self.predictor = Predictor(self.ocr_processor, model_path, vectorizer_path)
        
    def process_receipt(self, user_id, receipt_image, receipt_image_path):
        receipt_image.save(receipt_image_path)

        receipt_text = self.ocr_processor.extract_text(receipt_image_path)
        total_price = self.predictor.extract_total_price(receipt_image_path)
        category = self.predictor.predict_category(receipt_text)

        # Generate hash of the receipt image
        receipt_hash = self.generate_receipt_hash(receipt_image_path)

        # Check if the hash already exists in the database
        with self.db_connection.cursor() as cursor:
            cursor.execute("SELECT expense_id FROM public.\"Receipt\" WHERE receipt_hash = %s", (receipt_hash,))
            exists_result = cursor.fetchone()
            if exists_result:
                # Receipt already exists, return a flag indicating this
                return None, None, receipt_hash, True, False

        # Check if a receipt with the same category and total price already exists for the user
        with self.db_connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.expense_id
                FROM public."Expense" e
                JOIN public."Category" c ON e.category_id = c.category_id
                WHERE e.user_id = %s
                AND c.category_name = %s
                AND e.amount = %s
            """, (user_id, category, total_price))
            result = cursor.fetchone()

        if result:
            return None, None, receipt_hash, False, True

        return total_price, category, receipt_hash, False, False

    def generate_receipt_hash(self, receipt_image_path):
        hasher = hashlib.sha256()
        with open(receipt_image_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def save_receipt(self, user_id, total_price, category, description, receipt_hash):
        current_date = datetime.date.today()

        with self.db_connection.cursor() as cursor:
            query = """
            INSERT INTO public."Expense" (user_id, category_id, amount, description, date, receipt_hash)
            VALUES (%s, (
                SELECT category_id
                FROM public."Category"
                WHERE category_name = %s
            ), %s, %s, %s, %s)
            RETURNING expense_id, category_id;
            """
            cursor.execute(query, (user_id, category, total_price, description, current_date, receipt_hash))
            result = cursor.fetchone()
            expense_id = result[0]
            category_id = result[1]
            self.db_connection.commit()

            # Update the budget based on the created expense
            budget_model = Budget(self.db_connection)
            budget_model.update_budget_amount(user_id, category_id, total_price, current_date)

        # Save the hash to the Receipt table
        with self.db_connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public."Receipt" (expense_id, receipt_hash)
                VALUES (%s, %s)
            """, (expense_id, receipt_hash))
            self.db_connection.commit()

        return expense_id