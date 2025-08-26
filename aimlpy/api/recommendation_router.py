"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from fastapi import APIRouter

from aimlpy.entity.common import ErrorCode
from aimlpy.entity.recommendation_reqres import GetRecommendationResponse, GetRecommendationRequest
from aimlpy.service.recommendation_service import RecommendationService
from aimlpy.util import loggerutil

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Recommendation"])

service = RecommendationService()


@router.get("/ml/recommend", response_model=GetRecommendationResponse)
async def get_recommendation(user_id: str, top_n: int = 10):
    try:
        req = GetRecommendationRequest(user_id=user_id)
        res = service.get_recommendations(req)
        return res
    except Exception as e:
        logger.exception(f"Error: {e}")
        return GetRecommendationResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))
