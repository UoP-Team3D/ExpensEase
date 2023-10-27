from PIL import Image, ImageFilter
import pytesseract
import os
import cv2
import numpy as np


class OCRProcessor:
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR Processor.
        
        Args:
            tesseract_path (str, optional): Path to the Tesseract executable, if needed. (in case the executable is not in the PATH)
        """  
        if tesseract_path:
            pytesseract.tesseract_cmd = tesseract_path

    def _deskew_image(self, img: Image):        
        # Detect lines in the image using Hough transform on the inverted binary image
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

        if lines is not None:
            angles = []
            for rho, theta in lines[:, 0]:
                if 45 < np.degrees(theta) < 135:  # Filtering near-vertical lines
                    angles.append(theta)
            
            # Compute the median angle
            if len(angles) > 0:
                median_angle = np.median(angles)
                angle_deg = -np.degrees(median_angle) + 90  # Convert to degrees and account for vertical angle
            else:
                angle_deg = 0
        else:
            angle_deg = 0

        img_array = np.array(img)
        if len(img_array.shape) == 2:
            rows, cols = img_array.shape
        else:
            rows, cols, _ = img_array.shape

        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle_deg, 1)
        deskewed_image = cv2.warpAffine(img_array, rotation_matrix, (cols, rows))


        return Image.fromarray(deskewed_image)

    def _preprocess_image(self, image_path, save_path=None) -> Image:
        img = cv2.imread(image_path)

        file_name = os.path.basename(image_path).split('.')[0]

        file_name = file_name.split()[0]
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb_planes = cv2.split(img)
        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            result_planes.append(diff_img)
        img = cv2.merge(result_planes)
        
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)#increases the white region in the image 
        img = cv2.erode(img, kernel, iterations=1) #erodes away the boundaries of foreground object
        
        # Apply threshold to get image with only b&w (binarization)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        if save_path:
            image_dir = os.path.join(current_dir, os.pardir, "templates", "receipts")
            filename_extracted = os.path.basename(os.path.join(image_dir, image))
            file_extension = os.path.splitext(filename_extracted)[1]
            new_file_name = os.path.splitext(filename_extracted)[0] + "-processed" + file_extension
            new_file_path = os.path.join(os.path.dirname(os.path.join(image_dir, image)) + "//processed", new_file_name)

            #Save the filtered image in the output directory
            cv2.imwrite(new_file_path, img)

        return img

    def extract_text(self, image_path, preprocess=True) -> str:
        # Open the image
        image = Image.open(image_path)

        if preprocess:
            filename_extracted = os.path.basename(image_path)

            file_extension = os.path.splitext(filename_extracted)[1]
            new_file_name = os.path.splitext(filename_extracted)[0] + "-processed" + file_extension
            new_file_path = os.path.join(os.path.dirname(image_path) + "//processed", new_file_name)
            image = self._preprocess_image(image_path, new_file_path)
            final = pytesseract.image_to_string(image, lang="eng", config="--psm 3") 
            # create text file containing final, named the same as image_path, in new_file_path
            text_file = open(new_file_path + ".txt", "w")
            text_file.write(final)
            
        return pytesseract.image_to_string(image, lang="eng", config="--psm 3") 


# Example use
if __name__ == "__main__":
    ocr_processor = OCRProcessor()

    # Calculate the relative path to the clear.jpeg file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    image_dir = os.path.join(current_dir, os.pardir, "templates", "receipts")

    all_images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    for image in all_images:
        filename_extracted = os.path.basename(os.path.join(image_dir, image))
        file_extension = os.path.splitext(filename_extracted)[1]
        new_file_name = os.path.splitext(filename_extracted)[0] + "-processed" + file_extension
        new_file_path = os.path.join(os.path.dirname(os.path.join(image_dir, image)) + "//processed", new_file_name)

        text = ocr_processor.extract_text(os.path.join(image_dir, image))
        print(f"{image}:  {text}")