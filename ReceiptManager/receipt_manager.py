try: 
    import curses
    from PIL import Image
    import pytesseract
    import os
    import csv
    import cv2
    import numpy as np
    import shutil
    import sys
except ImportError:
    print("ERROR: One or more required modules are not installed! Please run 'pip install -r requirements.txt' to install them.")
    exit(1)

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
            pass
#            cv2.imwrite(new_file_path, img)
        return img

    def extract_text(self, image_path, preprocess=True) -> str:
        # Open the image
        image = Image.open(image_path)

        if preprocess:
          #  filename_extracted = os.path.basename(image_path)

          #  file_extension = os.path.splitext(filename_extracted)[1]
          #  new_file_name = os.path.splitext(filename_extracted)[0] + "-processed" + file_extension
          #  new_file_path = os.path.join(os.path.dirname(image_path) + "//processed", new_file_name)
            image = self._preprocess_image(image_path)
          #  final = pytesseract.image_to_string(image, lang="eng", config="--psm 3") 
          #  # create text file containing final, named the same as image_path, in new_file_path
          #  text_file = open(new_file_path + ".txt", "w")
          #  text_file.write(final)
            return pytesseract.image_to_string(image, lang="eng", config="--psm 3") 
        return pytesseract.image_to_string(image, lang="eng", config="--psm 3") 

class CursesInterface:
    total_receipts = 0

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) 
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
        self.ocr_processor = OCRProcessor()
    
    def scan_image(self, image_name):
        script_directory = os.path.dirname(__file__)
        image_path = os.path.join(script_directory, "receipts", image_name)
        extracted_text = self.ocr_processor.extract_text(image_path)
        
        source = os.path.join(script_directory, "receipts", image_name)
        destination = os.path.join(script_directory, "receipts", "processed", image_name)
        shutil.move(source, destination)
        
        return extracted_text

    def loading_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        loading_text = "Loading..."
        x = w // 2 - len(loading_text) // 2
        y = h // 2

        self.stdscr.addstr(y, x, loading_text)
        self.stdscr.refresh()

        script_directory = os.path.dirname(__file__)
        subfolders = ["dataset", "receipts"]

        # Create the required subfolders if they don't exist
        for subfolder in subfolders:
            subfolder_path = os.path.join(script_directory, subfolder)
            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)
                
        if not os.path.exists(os.path.join(script_directory, "receipts", "processed")):
            os.mkdir(os.path.join(script_directory, "receipts", "processed"))

        dataset_folder_path = os.path.join(script_directory, "dataset")
        csv_file = os.path.join(dataset_folder_path, "dataset.csv")
        count = 0

        if not os.path.isfile(csv_file):
            return
        
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row
            for row in reader:
                if row[0] and row[1]:  # Check if both "receipt" and "category" columns are not empty
                    count += 1
        
        self.total_receipts = count

        if self.total_receipts > 0:
            # Check if teseearct is installed
            try:
                dummy_image = Image.new('RGB', (60, 30), color = 'red')
                pytesseract.image_to_string(dummy_image)
                
            except FileNotFoundError:
                self.stdscr.clear()
                
                loading_text = "ERROR: Tesseract is not installed! Press any key to continue"
                x = w // 2 - len(loading_text) // 2
                y = h // 2

                self.stdscr.addstr(y, x, loading_text)
                self.stdscr.refresh()
                self.stdscr.getch()
                exit(1)
                
            except Exception as e:
                self.stdscr.clear()
                
                loading_text = "ERROR: Tesseract has an error while trying to initialise. Press any key to continue"
                x = w // 2 - len(loading_text) // 2
                y = h // 2

                self.stdscr.addstr(y, x, loading_text)
                self.stdscr.refresh()
                self.stdscr.getch()
                pass     

    def iterative_scan_and_categorise(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        information_text = "Feature will iteratively categorize items in the receipts folder. Press any key to continue."
        x = w // 2 - len(information_text) // 2
        y = h // 2
        self.stdscr.addstr(y, x, information_text)
        self.stdscr.refresh()
        self.stdscr.getch()

        # Step 1: Select an image
        script_directory = os.path.dirname(__file__)
        receipt_folder_path = os.path.join(script_directory, "receipts")

        all_images = [f for f in os.listdir(receipt_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        count = 0
        image_length = len(all_images)

        if not all_images:
            error_text = f"No images found in the receipts folder ({receipt_folder_path}). Press any key to continue."
            x = w // 2 - len(error_text) // 2
            y = h // 2
            self.stdscr.addstr(y, x, error_text)
            self.stdscr.refresh()
            self.stdscr.getch()
            return
        
        for image in all_images:
            count+=1

            try:
                extracted_text = self.scan_image(image)
            except(IOError):
                count-=1
                image_length-=1

                self.stdscr.clear()
                failure_message = f"ERROR: There was an error trying to scan the image {image}! This image will be ignored. Press any key to continue"
                x = w // 2 - len(failure_message) // 2
                y = h // 2
                self.stdscr.addstr(y, x, failure_message)
                self.stdscr.refresh()
                self.stdscr.getch()
                continue

            self.stdscr.clear()

            categories = ["Groceries", "Personal Upkeep", "Eating Out", "Entertainment"]
            selected_category = self.select_from_list(f"Select a category for {image} ({count}/{image_length}) using arrow keys and press Enter:", categories)

            dataset_folder_path = os.path.join(script_directory, "dataset")
            csv_file_path = os.path.join(dataset_folder_path, "dataset.csv")

            try:
                self.save_to_csv(csv_file_path, extracted_text, selected_category)
            except Exception:
                count-=1
                image_length-=1

                self.stdscr.clear()
                failure_message = f"ERROR: You have already scanned this receipt (for {image})! Press any key to continue"
                x = w // 2 - len(failure_message) // 2
                y = h // 2
                self.stdscr.addstr(y, x, failure_message)
                self.stdscr.refresh()
                self.stdscr.getch()
                continue

    def automatic_scan_and_categorise(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        instructions = [  "Auto-Scan & Categorise Receipts:",
                            "- Based on file names.",
                            "- 'groceries.png' or 'gro.png' → `Groceries`",
                            "- 'personal-upkeep.png' or 'pu.png' → `Personal Upkeep`", 
                            "- 'eating-out.png' or 'eo.png' → `Eating Out`", 
                            "- 'entertainment.png' or 'ent.png' → `Entertainment`",
                            "- Identifier separate (e.g., 'pu-ma.png', not 'puma.png'). Case insensitive.",
                            "Press any key to continue."]

        for idx, line in enumerate(instructions):
            x = w // 2 - len(line) // 2
            y = h // 2 - len(instructions) // 2 + idx
            self.stdscr.addstr(y, x, line)

        self.stdscr.refresh()
        self.stdscr.getch()

        script_directory = os.path.dirname(__file__)
        receipt_folder_path = os.path.join(script_directory, "receipts")
        all_images = [f for f in os.listdir(receipt_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not all_images:
            self.stdscr.clear()
            error_text = f"No images found in the receipts folder ({receipt_folder_path}). Press any key to continue."
            x = w // 2 - len(error_text) // 2
            y = h // 2
            self.stdscr.addstr(y, x, error_text)
            self.stdscr.refresh()
            self.stdscr.getch()
            return
        
        count = 0
        image_length = len(all_images)

        self.stdscr.clear()

        for image in all_images:
            count+=1

            message = f"Processing {image} ({count}/{image_length})..."
            x = w // 2 - len(message) // 2
            y = h // 2
            self.stdscr.addstr(y, x, message)
            self.stdscr.refresh()

            try:
                extracted_text = self.scan_image(image)
            except(IOError):
                count-=1
                image_length-=1

                self.stdscr.clear()
                failure_message = f"ERROR: There was an error scanning the image {image}! This image will be ignored. Press any key to continue"
                x = w // 2 - len(failure_message) // 2
                y = h // 2
                self.stdscr.addstr(y, x, failure_message)
                self.stdscr.refresh()
                self.stdscr.getch()
                continue

            self.stdscr.clear()

            if "groceries" in image.lower() or "gro" in image.lower():
                selected_category = "Groceries"

            elif "personal-upkeep" in image.lower() or "pu" in image.lower():
                selected_category = "Personal Upkeep"

            elif "eating-out" in image.lower() or "eo" in image.lower():
                selected_category = "Eating Out"

            elif "entertainment" in image.lower() or "ent" in image.lower():
                selected_category = "Entertainment"

            else:
                selected_category = self.select_from_list(f"Category wasn't found for {image} ({count}/{image_length}), select it using arrow keys and press Enter:", ["Groceries", "Personal Upkeep", "Eating Out", "Entertainment"])

            dataset_folder_path = os.path.join(script_directory, "dataset")
            csv_file_path = os.path.join(dataset_folder_path, "dataset.csv")

            try:
                self.save_to_csv(csv_file_path, extracted_text, selected_category)

            except(IOError):
                count-=1
                image_length-=1

                self.stdscr.clear()
                failure_message = f"ERROR: I/O Error occurred while trying to save {image}! Make sure the file is not open. Press any key to continue"
                x = w // 2 - len(failure_message) // 2
                y = h // 2
                self.stdscr.addstr(y, x, failure_message)
                self.stdscr.refresh()
                self.stdscr.getch()
                continue

            except(Exception):
                count-=1
                image_length-=1

                self.stdscr.clear()
                failure_message = f"ERROR: You have already scanned receipt (for {image})! Press any key to continue"
                x = w // 2 - len(failure_message) // 2
                y = h // 2
                self.stdscr.addstr(y, x, failure_message)
                self.stdscr.refresh()
                self.stdscr.getch()
                continue


    def scan_and_categorise(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # Step 1: Select an image
        script_directory = os.path.dirname(__file__)
        receipt_folder_path = os.path.join(script_directory, "receipts")
        all_images = [f for f in os.listdir(receipt_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not all_images:
            self.stdscr.clear()
            error_text = f"No images found in the receipts folder ({receipt_folder_path}). Press any key to continue."
            x = w // 2 - len(error_text) // 2
            y = h // 2
            self.stdscr.addstr(y, x, error_text)
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        selected_image = self.select_from_list("Select an image using arrow keys and press the Enter key:", all_images)
        selected_image_path = os.path.join(receipt_folder_path, selected_image)

        try: 
            extracted_text = self.scan_image(selected_image_path)
        except(Exception):
            self.stdscr.clear()

            failure_message = "ERROR: There was an error trying to scan the image! This will not be saved to your dataset. Press any key to continue"
            x = w // 2 - len(failure_message) // 2
            y = h // 2
            self.stdscr.addstr(y, x, failure_message)
            self.stdscr.refresh()
            self.stdscr.getch()
            return


        self.stdscr.clear() 

        # Step 4: Select category
        categories = ["Groceries", "Personal Upkeep", "Eating Out", "Entertainment"]
        selected_category = self.select_from_list("Select a category using arrow keys and press Enter:", categories)

        # Step 5: Save to CSV
        dataset_folder_path = os.path.join(script_directory, "dataset")
        csv_file_path = os.path.join(dataset_folder_path, "dataset.csv")

        try:
            self.save_to_csv(csv_file_path, extracted_text, selected_category)

        except(IOError):
            self.stdscr.clear()

            failure_message = f"ERROR: I/O Error occurred while trying to save the image! Make sure the file is not open. Press any key to continue"
            x = w // 2 - len(failure_message) // 2
            y = h // 2
            self.stdscr.addstr(y, x, failure_message)
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        except(Exception):
            self.stdscr.clear()

            failure_message = "ERROR: You have already scanned this receipt! Press any key to continue"
            x = w // 2 - len(failure_message) // 2
            y = h // 2
            self.stdscr.addstr(y, x, failure_message)
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        self.stdscr.clear()
        # Display success message
        success_message = "Receipt data saved successfully! Press any key to continue."
        x = w // 2 - len(success_message) // 2
        y = h // 2
        self.stdscr.addstr(y, x, success_message)
        self.stdscr.refresh()
        self.stdscr.getch()


    def select_from_list(self, prompt, items):
        selected_index = 0

        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            x = w // 2 - max(len(item) for item in items) // 2
            y = h // 2 - len(items) // 2

            self.stdscr.addstr(y - 2, x, prompt)

            for idx, item in enumerate(items):
                if idx == selected_index:
                    self.stdscr.addstr(y + idx, x, item, curses.color_pair(1))
                else:
                    self.stdscr.addstr(y + idx, x, item)

            key = self.stdscr.getch()

            if key == curses.KEY_UP and selected_index > 0:
                selected_index -= 1

            elif key == curses.KEY_DOWN and selected_index < len(items) - 1:
                selected_index += 1

            elif key == curses.KEY_ENTER or key in [10, 13]:
                return items[selected_index]

    def select_category(self):
        curses.curs_set(0)  # Hide the cursor
        categories = ["Groceries", "Personal Upkeep", "Eating Out", "Entertainment"]
        selected_category_index = 0

        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Select a category using arrow keys and press Enter:")

            for idx, category in enumerate(categories):
                if idx == selected_category_index:
                    self.stdscr.addstr(idx + 2, 0, category, curses.color_pair(1))

                else:
                    self.stdscr.addstr(idx + 2, 0, category)

            key = self.stdscr.getch()

            if key == curses.KEY_UP and selected_category_index > 0:
                selected_category_index -= 1

            elif key == curses.KEY_DOWN and selected_category_index < len(categories) - 1:
                selected_category_index += 1

            elif key == curses.KEY_ENTER or key in [10, 13]:
                return categories[selected_category_index]

    def save_to_csv(self, csv_file_path, receipt_text, category):
        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["receipt", "category"])

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                existing_receipt = row[0]
                if existing_receipt == receipt_text:
                    raise Exception("Receipt already exists in the CSV file! Try another receipt")

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([receipt_text, category])

    def how_to_page(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        instructions = [
            "Receipt Scanning Instructions:",
            "1. Ensure good lighting and place receipt on a flat surface.",
            "2. Take a clear photo using your phone.",
            "3. Save the photo to the 'receipts' folder.",
            "4. Run the scan+categorise feature you'd like from the menu.",
            "Press any key to go back to the menu."]

        for idx, line in enumerate(instructions):
            x = w // 2 - len(line) // 2
            y = h // 2 - len(instructions) // 2 + idx
            self.stdscr.addstr(y, x, line)

        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, 10, 13, 2]:  # 2 is ASCII for CTRL+B, 10 and 13 are ASCII for ENTER
                break

    def dataset_rundown(self):
        script_directory = os.path.dirname(__file__)
        dataset_folder_path = os.path.join(script_directory, "dataset")
        csv_file_path = os.path.join(dataset_folder_path, "dataset.csv")

        category_counts = {}

        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row["category"]
                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # Calculate the center of the screen
        center_x = w // 2
        center_y = h // 2

        self.stdscr.addstr(center_y - len(category_counts) // 2 - 1, center_x - len("Category Counts:") // 2, "Category Counts:")

        row = 1
        for category, count in category_counts.items():
            self.stdscr.addstr(center_y - len(category_counts) // 2 + row, center_x - len(f"{category}: {count}") // 2, f"{category}: {count}")
            row += 1

        # Add "press any key to continue" message at the bottom
        self.stdscr.addstr(center_y + len(category_counts) // 2 + 1, center_x - len("Press any key to continue...") // 2, "Press any key to continue...", curses.A_BOLD)

        self.stdscr.refresh()
        self.stdscr.getch()

    def menu(self, options):
        self.loading_screen()
        current_row = 0

        title = f"Receipt Scanner 3000 (ExpensEase™) - You have {self.total_receipts} unique receipt{'s' if self.total_receipts != 1 else ''} in your dataset"

        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()

            # Display the title
            title_x = w // 2 - len(title) // 2
            title_y = h // 2 - len(options) // 2 - 2
            self.stdscr.addstr(title_y, title_x, title)

            for idx, option in enumerate(options):
                x = w // 2 - len(option) // 2
                y = h // 2 - len(options) // 2 + idx
                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, option)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, x, option)
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1

            elif key == curses.KEY_DOWN and current_row < len(options) - 1:
                current_row += 1

            elif key == curses.KEY_ENTER or key in [10, 13]:
                return options[current_row]

    def main(self):
        while True:
            options = ["Basic Scan + Categorise", "Iterative Scan + Categorise", "Auto Scan + Categorise", "Dataset Breakdown", "How To Take Receipt Photos", "Exit"]
            selection = self.menu(options)

            if selection == "How To Take Receipt Photos":
                self.how_to_page()

            elif selection == "Basic Scan + Categorise":
                self.scan_and_categorise()

            elif selection == "Iterative Scan + Categorise":
                self.iterative_scan_and_categorise()

            elif selection == "Auto Scan + Categorise":
                self.automatic_scan_and_categorise()

            elif selection == "Dataset Breakdown":
                self.dataset_rundown()

            elif selection == "Exit":
                break

            else:
                raise Exception("Invalid selection")
            
            self.stdscr.clear()
        
if __name__ == "__main__":
    if sys.version_info.major == 3 and sys.version_info.minor == 11 and sys.version_info.micro == 6:
        curses.wrapper(lambda stdscr: CursesInterface(stdscr).main())    
    else:
        print("ERROR: This program requires Python 3.11.6. Please install Python 3.11.6 to run this program.")
        exit(1)