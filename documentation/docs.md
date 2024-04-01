# ExpensEase API Documentation

## Authentication (auth.py)

### Register

- Endpoint: `POST /api/v1/register`
- Description: Register a new user.
- Request Body:
  ```json
  {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "pin": "string"
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "User registered successfully",
        "data": {
          "user_id": integer
        }
      }
      ```
  - Error:
    - Status Code: 400 (Bad Request)
    - Body:
      ```json
      {
        "success": false,
        "message": "Error message"
      }
      ```

### Login

- Endpoint: `POST /api/v1/login`
- Description: Authenticate and log in a user.
- Request Body:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Login successful"
      }
      ```
  - Error:
    - Status Code: 401 (Unauthorized)
    - Body:
      ```json
      {
        "success": false,
        "message": "Invalid username or password."
      }
      ```

### Logout

- Endpoint: `DELETE /api/v1/logout`
- Description: Log out the currently authenticated user.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Logout successful"
      }
      ```

## Receipts (receipt.py)

### Upload Receipt

- Endpoint: `POST /api/v1/receipt/upload`
- Description: Upload a receipt image and process it.
- Request Body: Form-data
  - `receipt_image`: File (Image file)
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Receipt processed successfully",
        "data": {
          "receipt_id": "string",
          "category": "string",
          "total_price": float
        }
      }
      ```
  - Error:
    - Status Code: 400 (Bad Request)
    - Body:
      ```json
      {
        "success": false,
        "message": "Error message"
      }
      ```

### Save Receipt

- Endpoint: `POST /api/v1/receipt/save_receipt`
- Description: Save a processed receipt.
- Request Body:
  ```json
  {
    "receipt_id": "string",
    "description": "string",
    "total_price": number (optional),
    "category": "string" (optional)
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Receipt saved successfully",
        "data": {
          "expense_id": integer
        }
      }
      ```
  - Error:
    - Status Code: 400 (Bad Request)
    - Body:
      ```json
      {
        "success": false,
        "message": "Error message"
      }
      ```

## Budgets (budget.py)

### Create Budget

- Endpoint: `POST /api/v1/budget/create`
- Description: Create a new budget.
- Request Body:
  ```json
  {
    "category_id": integer,
    "total_amount": number,
    "start_date": "string" (YYYY-MM-DD),
    "end_date": "string" (YYYY-MM-DD)
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Budget created successfully",
        "data": {
          "budget_id": integer
        }
      }
      ```
  - Error:
    - Status Code: 400 (Bad Request)
    - Body:
      ```json
      {
        "success": false,
        "message": "Error message"
      }
      ```

### Get Budget

- Endpoint: `GET /api/v1/budget/<budget_id>`
- Description: Retrieve a specific budget by ID.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Budget retrieved successfully",
        "data": {
          "budget_id": integer,
          "user_id": integer,
          "category_id": integer,
          "total_amount": number,
          "current_amount": number,
          "start_date": "string" (YYYY-MM-DD),
          "end_date": "string" (YYYY-MM-DD)
        }
      }
      ```
  - Error:
    - Status Code: 404 (Not Found)
    - Body:
      ```json
      {
        "success": false,
        "message": "Budget not found"
      }
      ```

### Update Budget

- Endpoint: `PUT /api/v1/budget/<budget_id>`
- Description: Update a specific budget by ID.
- Request Body:
  ```json
  {
    "total_amount": number
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Budget updated successfully"
      }
      ```
  - Error:
    - Status Code: 404 (Not Found)
    - Body:
      ```json
      {
        "success": false,
        "message": "Budget not found"
      }
      ```

### Delete Budget

- Endpoint: `DELETE /api/v1/budget/<budget_id>`
- Description: Delete a specific budget by ID.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Budget deleted successfully"
      }
      ```
  - Error:
    - Status Code: 404 (Not Found)
    - Body:
      ```json
      {
        "success": false,
        "message": "Budget not found"
      }
      ```

### Get User Budgets

- Endpoint: `GET /api/v1/budget/`
- Description: Retrieve all budgets for the authenticated user.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Budgets retrieved successfully",
        "data": [
          {
            "budget_id": integer,
            "user_id": integer,
            "category_id": integer,
            "total_amount": number,
            "current_amount": number,
            "start_date": "string" (YYYY-MM-DD),
            "end_date": "string" (YYYY-MM-DD)
          },
          ...
        ]
      }
      ```

## Expenses (expense.py)

### Get Expenses

- Endpoint: `GET /api/v1/expense/`
- Description: Retrieve expenses with filtering, sorting, and pagination.
- Query Parameters:
  - `category` (optional): Filter expenses by category name.
  - `start_date` (optional): Filter expenses by start date (YYYY-MM-DD).
  - `end_date` (optional): Filter expenses by end date (YYYY-MM-DD).
  - `sort_by` (optional): Sort expenses by "amount", "date", or "category".
  - `sort_order` (optional): Sort order, "asc" for ascending or "desc" for descending.
  - `page` (optional, default: 1): Page number for pagination.
  - `per_page` (optional, default: 10): Number of expenses per page.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Expenses retrieved successfully",
        "data": [
          {
            "expense_id": integer,
            "amount": number,
            "description": "string",
            "date": "string" (YYYY-MM-DD),
            "category": "string"
          },
          ...
        ]
      }
      ```

### Update Expense

- Endpoint: `PUT /api/v1/expense/<expense_id>`
- Description: Update a specific expense by ID.
- Request Body:
  ```json
  {
    "description": "string" (optional),
    "amount": number (optional),
    "category": "string" (optional)
  }
  ```
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Expense updated successfully"
      }
      ```
  - Error:
    - Status Code: 404 (Not Found)
    - Body:
      ```json
      {
        "success": false,
        "message": "Expense not found or unauthorized"
      }
      ```

### Delete Expense

- Endpoint: `DELETE /api/v1/expense/<expense_id>`
- Description: Delete a specific expense by ID.
- Response:
  - Success:
    - Status Code: 200
    - Body:
      ```json
      {
        "success": true,
        "message": "Expense deleted successfully"
      }
      ```
  - Error:
    - Status Code: 404 (Not Found)
    - Body:
      ```json
      {
        "success": false,
        "message": "Expense not found or unauthorized"
      }
      ```
