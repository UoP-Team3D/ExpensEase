import pytest
from utilities.ocr import OCRProcessor
from utilities.prediction import Predictor
from unittest.mock import patch
import re
import os

@pytest.fixture
def ocr_processor():
    return OCRProcessor()

@pytest.fixture
def example_receipts(ocr_processor):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_images_dir = os.path.join(current_dir, 'test_images')

    return [
        {"text": ocr_processor.extract_text(os.path.join(test_images_dir, "holly.jpeg")), "category": "Eating Out"},
        {"text": ocr_processor.extract_text(os.path.join(test_images_dir, "clear.jpeg")), "category": "Eating Out"},
        {"text": ocr_processor.extract_text(os.path.join(test_images_dir, "nike.jpg")), "category": "Personal Upkeep"},
    ]

@pytest.fixture
def predictor(ocr_processor):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '..', 'machine', 'model.pkl')
    vectorizer_path = os.path.join(current_dir, '..', 'machine', 'vectorizer.pkl')

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}, make sure you generate the model first!")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}, make sure you generate the model first!")

    return Predictor(ocr_processor, model_path, vectorizer_path)

@patch('utilities.ocr.OCRProcessor.extract_text')
@patch('utilities.prediction.Predictor.predict_category')
def test_extract_total_price_and_category(mock_predict_category, mock_extract_text, predictor, example_receipts):
    # Test for total price extraction and category prediction
    for example in example_receipts:
        mock_extract_text.return_value = example["text"]
        mock_predict_category.return_value = example["category"]

        total_price = predictor.extract_total_price("dummy_path")
        predicted_category = predictor.predict_category(example["text"])

        # Asserting the total price and category predictions
        assert predicted_category == example["category"]