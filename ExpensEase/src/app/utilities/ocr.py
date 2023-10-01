from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR Processor.
        
        Args:
            tesseract_path (str, optional): Path to the Tesseract executable, if needed. (in case the executable is not in the PATH)
        """  
        if tesseract_path:
            pytesseract.tesseract_cmd = tesseract_path

    def _preprocess_image(self, image_path, save_path=None) -> Image:
        """
        Preprocess the given image to enhance its quality for OCR. 
        This method is intended for internal use within the class.

        Futher information: https://nanonets.com/blog/ocr-with-tesseract/
        """
        image = Image.open(image_path)

        # Convert to grayscale, "L" mode is for grayscale (8-bit pixels, black and white)
        grayscale_image = image.convert("L")

        # Binarization, the process of converting an image to black and white pixels, reducing "noise" in the image
        threshold = 128
        binarized_image = grayscale_image.point(lambda p: 255 if p > threshold else 0) # 255 is white, 0 is black, "point" applies a function to each pixel in the image, hence, if a pixel is greater than the threshold, it is set to white, otherwise, it is set to black

        # Resizing is important to improve text detection accuracy, as the OCR engine expects a consistent image size (if characters are too small, they'll probably be missed by the scanner)
        base_width = 1000
        w_percent = base_width / float(binarized_image.width) # get the percentage of the base width relative to the image width
        h_size = int(float(binarized_image.height) * float(w_percent)) # get the height size based on the percentage of the base width relative to the image width
        
        resized_image = binarized_image.resize((base_width, h_size), Image.BICUBIC) # "BICUBIC" ensures a smooth image when resizing an image, as opposed to "NEAREST" which is the default
        
        if save_path:
            resized_image.save(save_path)
        
        return resized_image


    def extract_text(self, image_path, preprocess=True) -> str:
        """
        Extract text from an image.
        
        Args:
            image_path (str): Path to the image to extract text from.
            preprocess (bool, optional): Whether to preprocess the image before extracting text (takes longer). Defaults to True.
        
        Returns:
            str: The extracted text.
        """

        # Open the image
        image = Image.open(image_path)

        # Preprocess the image if needed
        if preprocess:
            image = self._preprocess_image(image_path, "C:\\Users\\azulx\\Documents\\GitHub\\ExpensEase\\ExpensEase\\src\\app\\templates\\receipts\\clear_processed.jpeg")
        
        # Extract and return the text from the image
        return pytesseract.image_to_string(image)


# Example use
if __name__ == "__main__":
    ocr_processor = OCRProcessor()

    text = ocr_processor.extract_text("C:\\Users\\azulx\\Documents\\University\\receipt\\clear.jpeg")
    print(text)