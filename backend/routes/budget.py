from flask import Blueprint, request, current_app, session
from models.budget import Budget
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager

budget_blueprint = Blueprint('budget', __name__)

@budget_blueprint.route('/', methods=['GET'])
def get_user_budgets():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    budget_model = Budget(current_app.db_connection)
    budgets = budget_model.get_budgets_by_user(user_id)

    return ApiResponse.success("Budgets retrieved successfully", data=budgets)

@budget_blueprint.route('/create', methods=['POST'])
def create_budget():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    category_id = data.get('category_id')
    total_amount = data.get('total_amount')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not all([category_id, total_amount, start_date, end_date]):
        return ApiResponse.error("All fields are required", status=400)

    if total_amount <= 0:
        return ApiResponse.error("Total amount must be greater than zero", status=400)

    budget_model = Budget(current_app.db_connection)
    budget_id = budget_model.create_budget(user_id, category_id, total_amount, start_date, end_date)

    return ApiResponse.success("Budget created successfully", data={
        'budget_id': budget_id
    })

@budget_blueprint.route('/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    budget_model = Budget(current_app.db_connection)
    budget = budget_model.get_budget_by_id(budget_id)

    if not budget or budget['user_id'] != user_id:
        return ApiResponse.error("Budget not found", status=404)

    return ApiResponse.success("Budget retrieved successfully", data=budget)

@budget_blueprint.route('/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    total_amount = data.get('total_amount')

    if not total_amount:
        return ApiResponse.error("Total amount is required", status=400)

    budget_model = Budget(current_app.db_connection)
    budget = budget_model.get_budget_by_id(budget_id)

    if not budget or budget['user_id'] != user_id:
        return ApiResponse.error("Budget not found", status=404)

    budget_model.update_budget(budget_id, total_amount)

    return ApiResponse.success("Budget updated successfully")

@budget_blueprint.route('/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    budget_model = Budget(current_app.db_connection)
    budget = budget_model.get_budget_by_id(budget_id)

    if not budget or budget['user_id'] != user_id:
        return ApiResponse.error("Budget not found", status=404)

    budget_model.delete_budget(budget_id)

    return ApiResponse.success("Budget deleted successfully")

@budget_blueprint.route('/category/<int:category_id>', methods=['GET'])
def get_budgets_by_category(category_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)
    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    budget_model = Budget(current_app.db_connection)
    budgets = budget_model.get_budgets_by_category(user_id, category_id)
    return ApiResponse.success("Budgets retrieved successfully", data=budgets)