from flask import Blueprint, request, current_app, make_response, session
from models.receipt import Receipt
from utilities.errors import ApiResponse
from utilities.session_manager import SessionManager
import os
import time
import uuid

receipt_blueprint = Blueprint('receipts', __name__)

@receipt_blueprint.route('/upload', methods=['POST'])
def upload_receipt():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    if 'receipt_image' not in request.files:
        return ApiResponse.error("No receipt image provided", status=400)

    receipt_image = request.files['receipt_image']
    if receipt_image.filename == '':
        return ApiResponse.error("No receipt image selected", status=400)

    # Generate a unique filename for the receipt image
    receipt_image_filename = f"{user_id}_{int(time.time())}_{receipt_image.filename}"
    receipt_image_path = os.path.join('storage', receipt_image_filename)

    receipt_model = Receipt(current_app.db_connection)
    total_price, category = receipt_model.process_receipt(user_id, receipt_image, receipt_image_path)

    # Generate a unique identifier for the processed receipt
    receipt_id = str(uuid.uuid4())

    # Store the processed receipt details in memory or a temporary storage
    current_app.processed_receipts[receipt_id] = {
        'user_id': user_id,
        'total_price': total_price,
        'category': category,
        'receipt_image_path': receipt_image_path
    }

    return ApiResponse.success("Receipt processed successfully", data={
        'receipt_id': receipt_id,
        'total_price': total_price,
        'category': category
    })

@receipt_blueprint.route('/save_receipt', methods=['POST'])
def save_receipt():
    session_manager = current_app.session_manager
    user_id = session_manager.get_user_id(session.sid)

    if not user_id:
        return ApiResponse.error("Invalid session token", status=401)

    data = request.json
    receipt_id = data.get('receipt_id')
    description = data.get('description')
    total_price = data.get('total_price')
    category = data.get('category')

    if not receipt_id or not description:
        return ApiResponse.error("Receipt ID and description are required", status=400)

    # Retrieve the processed receipt details
    processed_receipt = current_app.processed_receipts.get(receipt_id)
    if not processed_receipt:
        return ApiResponse.error("Invalid receipt ID", status=400)

    # Update the total_price and category if provided in the request
    if total_price is not None:
        processed_receipt['total_price'] = float(total_price)
    if category is not None:
        processed_receipt['category'] = category

    receipt_model = Receipt(current_app.db_connection)
    
    expense_id = receipt_model.save_receipt(
        user_id,
        processed_receipt['total_price'],
        processed_receipt['category'],
        description
    )

    # Remove the processed receipt from temporary storage
    del current_app.processed_receipts[receipt_id]

    return ApiResponse.success("Receipt saved successfully", data={
        'expense_id': expense_id
    })