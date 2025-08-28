"""
Responses constants
"""

from starlette import status

EXPIRED_TOKEN_ERROR = {
    "key": "expired_token_error_key",
    "message": "The token has expired.",
    "status_code": status.HTTP_401_UNAUTHORIZED,
}

INVALID_TOKEN_ERROR = {
    "key": "invalid_token_error_key",
    "message": "Invalid token.",
    "status_code": status.HTTP_401_UNAUTHORIZED,
}

INVALID_CREDENTIALS_ERROR = {
    "key": "invalid_credentials_error_key",
    "message": "Invalid credentials.",
    "status_code": status.HTTP_401_UNAUTHORIZED,
}

INVALID_REFRESH_TOKEN_ERROR = {
    "key": "invalid_refresh_token_error_key",
    "message": "Invalid refresh token.",
    "status_code": status.HTTP_401_UNAUTHORIZED,
}

INVALID_CREATION_USER_TOKEN_ERROR = {
    "key": "invalid_creation_user_token_error_key",
    "message": "Invalid user creation token.",
    "status_code": status.HTTP_401_UNAUTHORIZED,
}

UNKNOWN_ERROR = {
    "key": "unknown_error_key",
    "message": "An unknown error occurred.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

FORBIDDEN_PERMISSIONS_ERROR = {
    "key": "forbidden_permissions_error_key",
    "message": "Permission denied.",
    "status_code": status.HTTP_403_FORBIDDEN,
}

USER_NOT_FOUND_ERROR = {
    "key": "user_not_found_error_key",
    "message": "User not found.",
    "status_code": status.HTTP_404_NOT_FOUND,
}

PASSWORD_MISSING_DIGIT_ERROR = {
    "key": "password_missing_digit_error_key",
    "message": "Password must contain at least one digit.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

PASSWORD_MISSING_UPPERCASE_ERROR = {
    "key": "password_missing_uppercase_error_key",
    "message": "Password must contain at least one uppercase letter.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

PASSWORD_MISSING_LOWER_CASE_ERROR = {
    "key": "password_missing_lower_case_error_key",
    "message": "Password must contain at least one lowercase letter.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

PASSWORD_MISSING_SPECIAL_CHARACTER_ERROR = {
    "key": "password_missing_special_character_error_key",
    "message": "Password must contain at least one special character.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

INVALID_EMAIL_ERROR = {
    "key": "invalid_email_error_key",
    "message": "Invalid email.",
    "status_code": status.HTTP_400_BAD_REQUEST,
}

USER_NOT_ALLOWED_ERROR = {
    "key": "user_not_allowed_error_key",
    "message": "User not allowed.",
    "status_code": status.HTTP_403_FORBIDDEN,
}
