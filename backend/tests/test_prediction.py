import pytest
from utilities.ocr import OCRProcessor
from utilities.prediction import Predictor
from unittest.mock import patch
import re

# TODO: make this actual receipt data
EXAMPLE_RECEIPTS = [
    {"text": "Sub Total USD$ 25.23\nTip: 3.78\nTotal USD$ 29.01", "category": "Groceries"},
    {"text": "Amount Due: EUR 15.75", "category": "Eating Out"},
    {"text": "Total: £100.75\nTip: £41.75\nTotal Spent: £141.75", "category": "Clothing"},
    {"text": "Items Total: $45.00\nTax: $3.50\nGrand Total: $48.50", "category": "Personal Care"},
    {"text": "1 x Coffee - $2.99\n1 x Sandwich - $5.49\n------------------------------\nTotal Payment: $8.48", "category": "Eating Out"}
]

@pytest.fixture
def ocr_processor():
    return OCRProcessor()

@pytest.fixture
def predictor(ocr_processor):
    return Predictor(ocr_processor, "/home/erdit/Desktop/Projects/ExpensEase/ExpensEase/ReceiptManager/bin/model.pkl", "/home/erdit/Desktop/Projects/ExpensEase/ExpensEase/ReceiptManager/bin/vectorizer.pkl")

@patch('utilities.ocr.OCRProcessor.extract_text')
@patch('utilities.prediction.Predictor.predict_category')
def test_extract_total_price_and_category(mock_predict_category, mock_extract_text, predictor):
    # Test for total price extraction and category prediction
    for example in EXAMPLE_RECEIPTS:
        mock_extract_text.return_value = example["text"]
        mock_predict_category.return_value = example["category"]
        
        total_price = predictor.extract_total_price("dummy_path")
        predicted_category = predictor.predict_category(example["text"])

        # Asserting the total price and category predictions
        assert total_price == float(re.findall(r"\d+\.?\d*", example["text"].split('Total')[-1])[0])
        assert predicted_category == example["category"]
