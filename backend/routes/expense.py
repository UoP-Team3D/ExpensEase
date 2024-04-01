from flask import Blueprint, request, current_app, session
from models.expense import Expense
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager

expense_blueprint = Blueprint('expenses', __name__)

@expense_blueprint.route('/', methods=['GET'])
def get_expenses():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    expense_model = Expense(current_app.db_connection)
    expenses = expense_model.get_expenses(
        user_id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )

    return ApiResponse.success("Expenses retrieved successfully", data=expenses)

@expense_blueprint.route('/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    description = data.get('description')
    amount = data.get('amount')
    category = data.get('category')

    expense_model = Expense(current_app.db_connection)
    updated_expense_id = expense_model.update_expense(
        expense_id,
        user_id,
        description=description,
        amount=amount,
        category=category
    )

    if updated_expense_id:
        return ApiResponse.success("Expense updated successfully")
    else:
        return ApiResponse.error("Expense not found or unauthorised", status=404)

@expense_blueprint.route('/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    expense_model = Expense(current_app.db_connection)
    deleted_expense_id = expense_model.delete_expense(expense_id, user_id)

    if deleted_expense_id:
        return ApiResponse.success("Expense deleted successfully")
    else:
        return ApiResponse.error("Expense not found or unauthorized", status=404)