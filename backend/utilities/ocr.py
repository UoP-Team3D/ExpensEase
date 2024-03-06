from PIL import Image
import pytesseract
import os
import cv2
import numpy as np

class OCRProcessor:
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR Processor.

        Args:
            tesseract_path (str, optional): Path to the Tesseract executable, if needed.
        """  
        if tesseract_path:
            pytesseract.tesseract_cmd = tesseract_path

    def _deskew_image(self, img: Image) -> Image:
        """Deskew the image for better OCR results.

        Args:
            img (Image): The image to deskew.

        Returns:
            Image: Deskewed image.
        """
        img_array = np.array(img)
        edges = cv2.Canny(img_array, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        angle_deg = 0
        if lines is not None:
            angles = [np.degrees(theta) - 90 for rho, theta in lines[:, 0] if 45 < np.degrees(theta) < 135]
            if angles:
                median_angle = np.median(angles)
                angle_deg = -median_angle

        rotation_matrix = cv2.getRotationMatrix2D((img_array.shape[1] / 2, img_array.shape[0] / 2), angle_deg, 1)
        deskewed_image = cv2.warpAffine(img_array, rotation_matrix, img_array.shape[1::-1])

        return Image.fromarray(deskewed_image)

    def _preprocess_image(self, image_path, save_path=None) -> Image:
        """Preprocess the image to enhance OCR accuracy.

        Args:
            image_path (str): Path to the image file.
            save_path (str, optional): Path to save the preprocessed image.

        Returns:
            Image: Preprocessed image.
        """
        img = cv2.imread(image_path)
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Removing shadows and improving contrast
        dilated_img = cv2.dilate(img, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        img = 255 - cv2.absdiff(img, bg_img)

        # Thresholding for binarization
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        if save_path:
            cv2.imwrite(save_path, img)

        return Image.fromarray(img)

    def extract_text(self, image_path, preprocess=True, testing=False) -> str:
        """Extract text from an image using OCR.

        Args:
            image_path (str): Path to the image file.
            preprocess (bool, optional): Whether to preprocess the image. Defaults to True.

        Returns:
            str: Extracted text.
        """
        image = Image.open(image_path)
        if preprocess:
            new_file_path = os.path.splitext(image_path)[0] + "-processed.png"
            image = self._preprocess_image(image_path, new_file_path)

        return pytesseract.image_to_string(image, lang="eng", config="--psm 3")


if __name__ == "__main__":
    ocrProcessor = OCRProcessor()
    print(ocrProcessor.extract_text("/home/erdit/Desktop/Projects/ExpensEase/ExpensEase/backend/templates/receipts/waitrose.jpg", True, True))