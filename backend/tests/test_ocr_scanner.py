import pytest
from PIL import Image
from utilities.ocr import OCRProcessor
from unittest.mock import patch, MagicMock
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
TEST_IMAGE_PATH = os.path.join(current_dir, '..', 'tests', 'test_images', 'clear.jpeg')

@pytest.fixture
def ocr_processor():
    return OCRProcessor()

def test_deskew_image(ocr_processor):
    # Provide a test image (use a simple fixture or a dummy image)
    test_image = Image.new('RGB', (100, 100))
    test_image_np = np.array(test_image)  # Convert PIL Image to NumPy array

    deskewed_image = ocr_processor._deskew_image(test_image_np)
    assert isinstance(deskewed_image, Image.Image)

def test_preprocess_image(ocr_processor, tmp_path):
    # Provide a path to a test image file
    processed_image = ocr_processor._preprocess_image(TEST_IMAGE_PATH)
    assert isinstance(processed_image, np.ndarray)

@patch('pytesseract.image_to_string', return_value='mocked text')
def test_extract_text(mocked_ocr, ocr_processor):
    extracted_text = ocr_processor.extract_text(TEST_IMAGE_PATH)
    assert extracted_text == 'mocked text'