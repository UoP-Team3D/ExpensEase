try:
    from receipt_manager import OCRProcessor

    import joblib
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    import json
    import curses
    import os
    import chardet
    import numpy as np
    import sys
except ImportError as e:
    print("ERROR: One or more required modules are not installed! Please run 'pip install -r requirements.txt' to install them.")
    print(f"Exception data: {e}")
    exit(1)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_names = ["erdit.csv", "andreas.csv", "ben.csv", "mo.csv", "paul.csv", "toby.csv", "george.csv"]
file_paths = [os.path.join(current_dir, "group_datasets", file_name) for file_name in file_names]
complete_csv_path = os.path.join(current_dir, "complete", "complete.csv")

model_path = os.path.join(current_dir, "bin", "model.pkl")
vectorizer_path = os.path.join(current_dir, "bin", "vectorizer.pkl")
vocabulary_path = os.path.join(current_dir, "bin", "vocabulary.json")

class NumpyEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for numpy data types. This is used to convert numpy data types to JSON serializable data types.
    Python does not have a built-in JSON encoder for numpy data types, so this class is used to convert numpy data types to JSON serializable data types.

    Args:
        json (_type_): The JSON encoder class to inherit from.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)

class ReceiptCategoriser:
    """
    Class for the receipt categoriser model. This class is used to train and predict the category of a receipt.
    """
    def __init__(self):
        self.is_initialised = False
        try:
            self.clf = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.is_initialised = True
        except:
            self.clf = None
            self.vectorizer = None
        
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

    def predict(self, processed_receipt: str):
        """
        Predict the category of a receipt using the trained model. An exception is raised if the model is not initialised.

        Args:
            processed_receipt (str): The receipt !STRING DATA! to predict the category of. This does not accept the image file as input.

        Returns:
            Prediction string: The predicted category of the receipt. "Groceries", "Eating Out", or "Personal Upkeep".
        """

        if not os.path.exists(model_path) and not os.path.exists(vectorizer_path):
            raise FileNotFoundError("Model or vectorizer not found. Please build the model first.")

        if not self.clf or not self.vectorizer:
            raise Exception(details="Predictor model not initialised! Cannot predict testing data")
        
        processed_statement = self._preprocess_receipt(processed_receipt)
        statement_vector = self.vectorizer.transform([processed_statement])
        prediction = self.clf.predict(statement_vector)

        return str(prediction[0])
    
    def train(self, max_feat = 10000):
        """
        Train the model using the complete dataset. The model is saved to the bin directory, and the vocabulary is saved to the bin directory as a JSON file.
        You can re-call this function as many times as you want to re-train the model, but the previous model will be overwritten.

        Args:
            max_feat (int, optional): The maximum number of features to use in the CountVectorizer. Defaults to 10000.
                                      Countvectorizer is used to convert a collection of text documents to a matrix of token counts.

        Raises:
            FileNotFoundError: Raised if the complete dataset is not found.
            ValueError: Raised if the dataset is empty.
            Exception: Raised if an unexpected error occurs while reading the dataset.
            Exception: Raised if an error occurs during training.
            Exception: Raised if an error occurs while saving the model.
            Exception: Raised if an error occurs during model evaluation.

        Returns:
            summary string: A summary of the model evaluation. This includes the accuracy and classification report.
        """
        try:
            data = pd.read_csv(complete_csv_path)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File {complete_csv_path} not found.")

        except pd.errors.EmptyDataError:
            raise ValueError("Error: The data file is empty.")

        except Exception as e:
            raise Exception(f"An unexpected error occurred while reading the file: {e}")
        
        try:
            receipts = data['receipt'].values
            category = data['category'].values

            receipts = [self._preprocess_receipt(receipt) for receipt in receipts]

            X_train, X_test, y_train, y_test = train_test_split(receipts, category, test_size=0.2, random_state=42)
            self.vectorizer = CountVectorizer(stop_words='english', max_features=max_feat)
            X_train_vec = self.vectorizer.fit_transform(X_train)

            self.clf = LogisticRegression(solver='liblinear', max_iter=1000)
            self.clf.fit(X_train_vec, y_train)
        
        except Exception as e:
            raise Exception(f"An error occurred during training: {e}")

        try:
            vocabulary = self.vectorizer.vocabulary_
            with open('bin\\vocabulary.json', 'w') as f:
                json.dump(vocabulary, f, cls=NumpyEncoder)

            # Save the trained model and vectorizer for future use
            joblib.dump(self.clf, model_path)
            joblib.dump(self.vectorizer, vectorizer_path)

        except Exception as e:
            raise Exception(f"An error occurred while saving the model: {e}")

        try:
            X_test_vec = self.vectorizer.transform(X_test)
            predictions = self.clf.predict(X_test_vec)

            accuracy = accuracy_score(y_test, predictions)
            report = classification_report(y_test, predictions)

            summary = f"Accuracy: {accuracy:.2f}\n\n"
            summary += "Classification Report:\n"
            summary += report

            return summary

        except Exception as e:
            raise Exception(f"An error occured during model evaluation: {e}")

class CursesInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) 
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 
        self.machine_model = ReceiptCategoriser()
        self.ocr_processor = OCRProcessor()

    def _list_files_in_directory(self, path):
        """
        List all files in a given directory. Used for listing the files in the test_receipts directory.

        Args:
        path (str): Path to the directory.

        Returns:
        list: List of file names.
        """
        return [file for file in os.listdir(path)]
    
    def _regulate_csv(self, file_paths: list[str]):
        """
        Combines everyones CSV files into a single CSV file, and returns the count of the categories "Groceries", "Eating Out", and "Personal Upkeep".
        Removes duplicates of the same receipt (if any), and creates a new CSV file with the combined data in "complete/complete.csv".

        Args:
            file_paths (list[str]): A list of file paths to the CSV files to be processed.
        """
        def DetectEncoding(file_path):
            with open(file_path, 'rb') as file:
                return chardet.detect(file.read())['encoding']

        all_data = pd.DataFrame()
        
        for file_path in file_paths:
            #! should be commented out upon datasets being acquired by entire team
            if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                continue
    
            encoding = DetectEncoding(file_path)
            df = pd.read_csv(file_path, encoding=encoding)
            all_data = pd.concat([all_data, df])
            
        all_data = all_data.drop_duplicates()
        
        category_counts = all_data['category'].value_counts()
        
        all_data.to_csv(complete_csv_path, index=False)

        count_dict = {
            "groceries": category_counts.get("Groceries", 0),
            "eating out": category_counts.get("Eating Out", 0),
            "clothing": category_counts.get("Personal Upkeep", 0)
        }

        return count_dict
        
    def menu(self, options):
        self.loading_screen()
        category_counts = self._regulate_csv(file_paths)
        current_row = 0

        title = f"Model Builder 3000 - {sum(category_counts.values())} receipts in concatenated dataset"

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
        
    def loading_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        loading_text = "Loading..."
        x = w // 2 - len(loading_text) // 2
        y = h // 2

        self.stdscr.addstr(y, x, loading_text)
        self.stdscr.refresh()

        complete_dir = os.path.join(current_dir, "complete")
        bin_dir = os.path.join(current_dir, "bin")

        os.makedirs(complete_dir, exist_ok=True)
        os.makedirs(bin_dir, exist_ok=True)
        
        #! should be commented out upon datasets being acquired by entire team
        '''
        for filename in file_paths:
            if not os.path.exists(filename):
                error_text = f"Error: The dataset {filename} was not found."
                x = w // 2 - len(error_text) // 2
                y = h // 2
                self.stdscr.addstr(y, x, error_text)
                self.stdscr.refresh()
                self.stdscr.getch()
                exit(1)5
        '''

    def dataset_analytics(self):
        if not os.path.exists(complete_csv_path):
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Error: The dataset {complete_csv_path} was not found.")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        data = pd.read_csv(complete_csv_path)

        category_counts = data['category'].value_counts()

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        title = f"Dataset Analytics - {len(data)} receipts in dataset"
        title_x = w // 2 - len(title) // 2

        row = 2
        for category, count in category_counts.items():
            self.stdscr.addstr(row, 0, f"{category}: {count}")
            row += 1

        self.stdscr.addstr(0, title_x, title)
        self.stdscr.refresh()
        self.stdscr.getch()

    def train_model(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        try:
            if not os.path.exists(complete_csv_path):
                raise FileNotFoundError(f"The dataset {complete_csv_path} was not found.")
            
            summary = self.machine_model.train()

            self.stdscr.addstr(2, (w - len("Training Complete!")) // 2, "Training Complete!")
            for i, line in enumerate(summary.split('\n')):
                self.stdscr.addstr(4 + i, (w - len(line)) // 2, line)

        except FileNotFoundError as e:
            self.stdscr.addstr(h // 2, (w - len(str(e))) // 2, str(e))

        except Exception as e:
            error_message = f"An error occurred: {e}"
            self.stdscr.addstr(h // 2, (w - len(error_message)) // 2, error_message)

        finally:
            self.stdscr.getch()
    
    def test_model(self):
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        test_receipts_path = os.path.join(current_script_dir, "test_receipts")

        files = self._list_files_in_directory(test_receipts_path)

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        current_row = 0

        select_file_message = "Select a file:"
        self.stdscr.addstr(1, (w - len(select_file_message)) // 2, select_file_message)

        while True:
            self.stdscr.clear()

            # Reprint the select file message after screen clear
            self.stdscr.addstr(1, (w - len(select_file_message)) // 2, select_file_message)

            for idx, file in enumerate(files):
                x = w // 2 - len(file) // 2
                y = h // 2 - len(files) // 2 + idx + 2  # Adjusted y position to account for the message
                if idx == current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, x, file)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, x, file)
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(files) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break

        selected_file = files[current_row]
        selected_file_path = os.path.join(test_receipts_path, selected_file)

        predicting_message = "Predicting Category..."
        self.stdscr.clear()
        self.stdscr.addstr(h // 2, (w - len(predicting_message)) // 2, predicting_message)
        self.stdscr.refresh()

        ocr_result = self.ocr_processor.extract_text(selected_file_path)

        try:
            prediction = self.machine_model.predict(ocr_result)
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx() 
            message = f"ExpensEase Prediction: This receipt is in the category: {prediction}"
            self.stdscr.addstr(h // 2, (w - len(message)) // 2, message)  
        
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.stdscr.addstr(h // 2, (w - len(error_message)) // 2, error_message) 

        press_key_message = "Press any key to continue"
        self.stdscr.addstr(h - 2, (w - len(press_key_message)) // 2, press_key_message)

        self.stdscr.refresh()
        self.stdscr.getch()

    def how_to_use(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        instructions = [
            "Model Builder Tutorial:",
            "1. Ensure the 'group_datasets' folder contains the datasets for each person",
            "2. Run the program and select 'Build Model' from the menu to train the model using the complete dataset",
            "3. Once the model is trained, select 'Test Model' from the menu to test the model using the test_receipts folder",
            "3.1. The test_receipts folder contains images of receipts to test the model with. Add your own images to this folder to test the model with them.",
            "4. Ensure the model can accurately predict the category of the receipts",
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
        pass

    def main(self):
        while True:
            options = ["Dataset Analytics", "Build Model", "Test Model", "How To Use", "Exit"]
            selection = self.menu(options)
            
            if selection == "Dataset Analytics":
                self.dataset_analytics()
            
            elif selection == "Build Model":
                self.train_model()

            elif selection == "Test Model":
                self.test_model()

            elif selection == "How To Use":
                self.how_to_use()
            
            elif selection == "Exit":
                break
            
            else:
                # should never happen, but it is good practise to add
                raise Exception("unexpected selection!")
            
            self.stdscr.clear()

if __name__ == "__main__":
    curses.wrapper(lambda stdscr: CursesInterface(stdscr).main())    