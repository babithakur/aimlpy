"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from enum import Enum

from pydantic import BaseModel


class ErrorCode(Enum):
    UNKNOWN = 0
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class BaseRequest(BaseModel):
    authorization: str = None
    debug_id: str = None


class BaseResponse(BaseModel):
    error: bool = False
    error_code: ErrorCode = ErrorCode.UNKNOWN
    message: str = None


class Pagination(BaseModel):
    page: int = 0
    page_size: int = 20
    total_count: int = 0
