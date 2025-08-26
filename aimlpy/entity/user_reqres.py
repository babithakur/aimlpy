"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""

from aimlpy.entity.common import BaseRequest, BaseResponse, Pagination
from aimlpy.entity.user import User


class AddUserRequest(BaseRequest):
    user: User = None


class AddUserResponse(BaseResponse):
    user: User = None


class UpdateUserRequest(BaseRequest):
    user_id: str = None
    username: str = None
    name: str = None
    email: str = None
    address: str = None
    phone: str = None


class UpdateUserResponse(BaseResponse):
    user: User = None


class GetUserRequest(BaseRequest):
    user_id: str = None


class GetUserResponse(BaseResponse):
    user: User = None


class ListUserRequest(BaseRequest):
    pagination: Pagination = None


class ListUserResponse(BaseResponse):
    users: list[User] = None
    pagination: Pagination = None
