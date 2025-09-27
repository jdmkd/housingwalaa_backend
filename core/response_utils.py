# response_utils.py
import uuid
from datetime import datetime
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import status as drf_status

def standard_response(
    success=True,
    message=None,
    data=None,
    errors=None,
    special_code=None,
    pagination=None,
    status_code=drf_status.HTTP_200_OK,
    request_id=None,
    use_json_response=False,
):
    """
    Standardized API Response for enterprise-level applications.

    Args:
        success (bool): Whether the request was successful.
        message (str): Human-readable message.
        data (dict/list): Response payload.
        errors (dict/list/str): Errors info if success=False.
        special_code (str): Application-specific code like "login_successful".
        pagination (dict): Optional pagination info.
        status_code (int): HTTP status code.
        request_id (str): Unique request ID for tracing.
        use_json_response (bool): If True, returns Django JsonResponse instead of DRF Response.

    Returns:
        Response or JsonResponse: Standardized API response.
    """

    if request_id is None:
        request_id = str(uuid.uuid4())

    timestamp = datetime.utcnow().isoformat() + "Z"

    meta = {
        "request_id": request_id,
        "timestamp": timestamp,
    }

    if pagination:
        meta["pagination"] = pagination

    # Ensure proper error/data structure based on success
    if success:
        if errors is not None:
            errors = None
        if message is None:
            message = "OK"
    else:
        data = None
        if message is None:
            message = "Error"
        if errors is None:
            errors = {"detail": ["An unknown error occurred."]}

    payload = {
        "success": success,
        "status": status_code,
        "message": message,
        "special_code": special_code,
        "data": data,
        "errors": errors,
        "meta": meta,
    }

    if use_json_response:
        return JsonResponse(payload, status=status_code, safe=False)

    return Response(payload, status=status_code)


def success_response(
    data=None,
    message="Success",
    special_code=None,
    pagination=None,
    status_code=drf_status.HTTP_200_OK,
    request_id=None,
):
    """
    Shortcut for successful responses
    """
    return standard_response(
        success=True,
        message=message,
        data=data,
        errors=None,
        special_code=special_code,
        pagination=pagination,
        status_code=status_code,
        request_id=request_id,
    )


def error_response(
    message="Error",
    errors=None,
    special_code=None,
    status_code=drf_status.HTTP_400_BAD_REQUEST,
    request_id=None,
):
    """
    Shortcut for error responses
    """
    return standard_response(
        success=False,
        message=message,
        data=None,
        errors=errors,
        special_code=special_code,
        status_code=status_code,
        request_id=request_id,
    )
