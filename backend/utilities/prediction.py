import re
from .ocr import OCRProcessor
import joblib
from sklearn import tree
from sklearn.linear_model import LogisticRegression

class Predictor:
    def __init__(self, ocr_processor, model_path, vectorizer_path):
        """
        Initialize the Predictor class with an OCR processor and paths to the trained model and vectorizer.

        Args:
            ocr_processor (OCRProcessor): An instance of the OCRProcessor class.
            model_path (str): Path to the trained model file.
            vectorizer_path (str): Path to the trained vectorizer file.
        """
        self.ocr_processor = ocr_processor
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
    
    def extract_total_price(self, image_path, preprocess=True):
        """
        Extract the total price from a receipt.

        Args:
            image_path (str): The path to the receipt image.
            preprocess (bool): Whether to preprocess the image before OCR. Defaults to True

        Returns:
            float or None: The extracted total price, or None if not found.
        """
        text = self.ocr_processor.extract_text(image_path, preprocess=True)

        pattern = r"(total|amount due|grand total|balance).*?[\$€£]?\s*(\d{1,3}(?:[.,]\d{2,3})?(?:[.,]\d{2})?)"
        matches = re.findall(pattern, text, re.IGNORECASE)

        prices = []
        for match in matches:
            try:
                price = float(match[1].replace(',', '.'))
                prices.append(price)
            except ValueError:
                continue

        print("Extracted Price: ", max(prices, default=None))
        return max(prices, default=None)

    def predict_category(self, receipt_text):
        """
        Predict the category of a receipt.

        Args:
            receipt_text (str): Text extracted from the receipt.

        Returns:
            str: Predicted category.
        """
        processed_text = self.vectorizer.transform([receipt_text])
        predicted_category = self.model.predict(processed_text)
        return predicted_category[0]
    
    @staticmethod
    def _preprocess_receipt(review):
        """
        Preprocess the receipt text. This function removes all non-alphabetic characters from the receipt text.

        Args:
            review (_type_): The receipt text to preprocess.

        Returns:
            _type_: The preprocessed receipt text.
        """
        review = ''.join(char for char in review if char.isalpha() or char.isspace())
        return review