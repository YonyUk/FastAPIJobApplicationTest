from fastapi import HTTPException,status

USER_ALREADY_EXISTS_ECXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Username already exists'
)

EMAIL_ALREADY_REGISTERED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Email already registered'
)

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='You must be admin to call this endpoint'
)