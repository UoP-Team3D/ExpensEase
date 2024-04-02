from flask import Blueprint, request, current_app, session
from models.category import Category
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager

category_blueprint = Blueprint('category', __name__)

@category_blueprint.route('/', methods=['GET'])
def get_user_categories():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    category_model = Category(current_app.db_connection)
    categories = category_model.get_categories_by_user(user_id)

    return ApiResponse.success("Categories retrieved successfully", data=categories)

@category_blueprint.route('/', methods=['POST'])
def create_category():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    category_name = data.get('category_name')

    if not category_name:
        return ApiResponse.error("Category name is required", status=400)

    category_model = Category(current_app.db_connection)
    category_id = category_model.create_category(user_id, category_name)

    return ApiResponse.success("Category created successfully", data={'category_id': category_id})

@category_blueprint.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    category_name = data.get('category_name')

    if not category_name:
        return ApiResponse.error("Category name is required", status=400)

    category_model = Category(current_app.db_connection)
    category = category_model.get_category_by_id(category_id)

    if not category or (category['user_id'] != user_id and not category['is_preset']):
        return ApiResponse.error("Category not found or unauthorised", status=404)

    category_model.update_category(category_id, category_name)

    return ApiResponse.success("Category updated successfully")

@category_blueprint.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    category_model = Category(current_app.db_connection)
    category = category_model.get_category_by_id(category_id)

    if not category or (category['user_id'] != user_id and not category['is_preset']):
        return ApiResponse.error("Category not found or unauthorized", status=404)

    category_model.delete_category(category_id)

    return ApiResponse.success("Category deleted successfully")