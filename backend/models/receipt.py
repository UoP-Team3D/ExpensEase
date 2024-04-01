from flask import request
import os
from utilities.ocr import OCRProcessor
from utilities.prediction import Predictor

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
        self.predictor = Predictor(self.ocr_processor, '/home/erdit/Desktop/Projects/ExpensEase/ExpensEase/ReceiptManager/bin/model.pkl', '/home/erdit/Desktop/Projects/ExpensEase/ExpensEase/ReceiptManager/bin/vectorizer.pkl')

    def process_receipt(self, user_id, receipt_image, receipt_image_path):
        receipt_image.save(receipt_image_path)

        receipt_text = self.ocr_processor.extract_text(receipt_image_path)
        total_price = self.predictor.extract_total_price(receipt_image_path)
        category = self.predictor.predict_category(receipt_text)

        return total_price, category

    def save_receipt(self, user_id, total_price, category, description):
        with self.db_connection.cursor() as cursor:
            query = """
            INSERT INTO public."Expense" (user_id, category_id, amount, description, date)
            VALUES (%s, (
                SELECT category_id
                FROM public."Category"
                WHERE category_name = %s
            ), %s, %s, CURRENT_DATE)
            RETURNING expense_id;
            """
            cursor.execute(query, (user_id, category, total_price, description))
            expense_id = cursor.fetchone()[0]
            self.db_connection.commit()

        return expense_id