from flask import jsonify, make_response

class ApiResponse:
    @staticmethod
    def success(message="Success", data=None, status=200):
        """Generate a success response.

        Args:
            message (str): Success message.
            data (dict, optional): Additional data to include in the response.
            status (int): HTTP status code.

        Returns:
            Response object with JSON data & status code.
        """
        response = {"success": True, "message": message}
        if data is not None:
            response["data"] = data

        resp = make_response(jsonify(response), status)
        return resp

    @staticmethod
    def error(message, status=400):
        """Generate an error response.

        Args:
            message (str): Error message.
            status (int): HTTP status code.

        Returns:
            Response object with JSON data and status code.
        """
        return jsonify({"success": False, "message": message}), status