ExpensEase/
|-- app/
|   |-- __init__.py           # Initializes Flask app and brings together other components
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- auth.py           # Authentication routes (login, logout, register)
|   |   |-- dashboard.py      # Dashboard, income/expense visualization
|   |   |-- expenses.py       # Handle expense-related functionalities
|   |-- models/
|   |   |-- __init__.py
|   |   |-- user.py           # User model (username, password, pin, biometrics)
|   |   |-- expense.py        # Expense model
|   |   |-- category.py       # Category model for expenses
|   |-- utilities/
|   |   |-- __init__.py
|   |   |-- ocr.py            # OCR scanner utility
|   |   |-- token_manager.py  # Authentication token utility
|   |-- static/               # Contains static files like CSS, JavaScript, images
|   |-- templates/            # Contains HTML templates
|-- config.py                 # Configuration variables
|-- run.py                    # Main entry to the application
|-- requirements.txt          # Required Python packages