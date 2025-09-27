from rest_framework.views import exception_handler
from rest_framework import status
from .response_utils import error_response

def custom_exception_handler(exc, context):
    """
    Custom exception handler to wrap DRF errors in standard_response format.
    """
    # First get default DRF response
    response = exception_handler(exc, context)

    if response is not None:
        # Example: ValidationError or IntegrityError
        return error_response(
            message="Validation failed" if response.status_code == status.HTTP_400_BAD_REQUEST else "Error",
            errors=response.data,  # This will be {"phone_number": ["already exists"]} etc.
            special_code="VALIDATION_ERROR" if response.status_code == status.HTTP_400_BAD_REQUEST else None,
            status_code=response.status_code,
        )

    # If DRF didn't handle, fall back
    return error_response(
        message=str(exc),
        errors={"detail": [str(exc)]},
        special_code="UNHANDLED_EXCEPTION",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
