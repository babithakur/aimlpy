"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from aimlpy.entity.common import BaseRequest, BaseResponse
from aimlpy.entity.recommendation import Recommendation


class GetRecommendationRequest(BaseRequest):
    user_id: str = None
    top_k: int = 10


class GetRecommendationResponse(BaseResponse):
    recommendations: list[Recommendation] = None
