from enum import Enum


class ErrorMessages(Enum):
    USER_NOT_FOUND = "User not found"
    INSUFFICIENT_RIGHTS = "Insufficient rights"
    COULD_NOT_VALIDATE_CREDENTIALS = "Couldn't validate credentials"
    TOKEN_EXPIRED = "Token expired"
    INVALID_TOKEN = "Invalid token"

    BOOK_NOT_FOUND = "Book not found"
    ENTITY_NOT_FOUND = "Entity not found"

    INCORRECT_CREDENTIALS = "Incorrect credentials"

    ID_SHOULD_NOT_BE_NULL = "ID shouldn't be NULL"

