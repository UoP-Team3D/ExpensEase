import pytest
from utilities.ocr import OCRProcessor
from utilities.prediction import Predictor
from unittest.mock import patch

EXAMPLE_RECEIPT_1 = """
Sub Total USD$ 25.23
Tip: 3.78
Total USD$ 29.01
"""

EXAMPLE_RECEIPT_2 = """
Amount Due: EUR 15.75
"""

EXAMPLE_RECEIPT_3 = """
Total: £100.75
Tip: £41.75
Total Spent: £141.75
"""

EXAMPLE_RECEIPT_4 = """
Items Total: $45.00
Tax: $3.50
Grand Total: $48.50
"""

EXAMPLE_RECEIPT_5 = """
1 x Coffee - $2.99
1 x Sandwich - $5.49
------------------------------
Total Payment: $8.48
"""

@pytest.fixture
def ocr_processor():
    return OCRProcessor()

@pytest.fixture
def predictor(ocr_processor):
    return Predictor(ocr_processor)

@patch('utilities.ocr.OCRProcessor.extract_text')
def test_extract_total_price(mock_extract_text, predictor):
    mock_extract_text.return_value = EXAMPLE_RECEIPT_1
    total_price = predictor.extract_total_price("dummy_path")
    assert total_price == 29.01

    mock_extract_text.return_value = EXAMPLE_RECEIPT_2
    total_price = predictor.extract_total_price("dummy_path")
    assert total_price == 15.75

    mock_extract_text.return_value = EXAMPLE_RECEIPT_3
    total_price = predictor.extract_total_price("dummy_path")
    assert total_price == 141.75

    mock_extract_text.return_value = EXAMPLE_RECEIPT_4
    total_price = predictor.extract_total_price("dummy_path")
    assert total_price == 48.50

    mock_extract_text.return_value = EXAMPLE_RECEIPT_5
    total_price = predictor.extract_total_price("dummy_path")
    assert total_price == 8.48