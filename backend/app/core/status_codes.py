from enum import IntEnum


class StatusCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNPROCESSABLE_ENTITY = 422
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500