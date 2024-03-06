import re
from .ocr import OCRProcessor

class Predictor:
    def __init__(self, ocr_processor):
        """
        Initialize the Predictor class with an OCR processor.

        Args:
            ocr_processor (OCRProcessor): An instance of the OCRProcessor class.
        """
        self.ocr_processor = ocr_processor

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

        return max(prices, default=None)