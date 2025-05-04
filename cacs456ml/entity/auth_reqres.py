"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from cacs456ml.entity.auth import Session
from cacs456ml.entity.common import BaseRequest, BaseResponse


class LoginRequest(BaseRequest):
    username: str = None
    email: str = None
    password: str = None


class LoginResponse(BaseResponse):
    session: Session = None


class LogoutRequest(BaseRequest):
    session_id: str = None
    user_id: str = None


class LogoutResponse(BaseResponse):
    pass
