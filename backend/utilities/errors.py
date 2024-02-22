from flask import jsonify

"""
Common HTTP Status Codes for Web APIs

200 Series: Success
200 OK - Request has succeeded.
201 Created - Request has succeeded and a new resource has been created.
202 Accepted - Request has been received but not yet acted upon.
204 No Content - Request has succeeded, but no content is returned.

300 Series: Redirection
301 Moved Permanently - URL of the requested resource has been changed permanently.
302 Found - URL of the requested resource has been changed temporarily.
304 Not Modified - Resource has not been modified since the last request.

400 Series: Client Errors
400 Bad Request - Server cannot or will not process the request due to client error.
401 Unauthorized - Authentication is required and has failed or not been provided.
403 Forbidden - Client does not have access rights to the content.
404 Not Found - Server cannot find the requested resource.
405 Method Not Allowed - Method not allowed for the requested resource.
406 Not Acceptable - Requested resource is not acceptable according to the Accept headers.
409 Conflict - Request could not be processed because of conflict in the request.
422 Unprocessable Entity - Request was well-formed but unable to be followed due to semantic errors.

500 Series: Server Errors
500 Internal Server Error  - Generic error message when server fails to fulfill request.
501 Not Implemented  - Server does not support the functionality required to fulfill the request.
503 Service Unavailable  - Server is currently unable to handle the request due to temporary overload or maintenance.
"""

class ApiResponse:
    @staticmethod
    def success(message="Success", data=None, status=200):
        """Generate a success response.

        Args:
            message (str): Success message.
            data (dict, optional): Additional data to include in the response.
            status (int): HTTP status code.

        Returns:
            Response object with JSON data and status code.
        """
        response = {"success": True, "message": message}
        if data is not None:
            response["data"] = data
        return jsonify(response), status

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