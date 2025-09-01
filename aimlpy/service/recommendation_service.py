"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from aimlpy.entity.common import ErrorCode
from aimlpy.entity.recommendation import Recommendation
from aimlpy.entity.recommendation_reqres import GetRecommendationRequest, GetRecommendationResponse
from aimlpy.util import strutil
import pandas as pd
from surprise import Dataset, Reader, SVD

#load and train once (outside class for demo)
#dummy csv file for 10 users, 10 notes
ratings_df = pd.read_csv('/home/babi/Desktop/aimlpy/aimlpy/service/ratings.csv')
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings_df[['userId', 'noteId', 'rating']], reader)
trainset = data.build_full_trainset()
model = SVD()
model.fit(trainset)

def get_top_n_recommendations(user_id: int, n: int = 5):
    all_item_ids = ratings_df['noteId'].unique()
    rated_items = ratings_df[ratings_df['userId'] == user_id]['noteId'].tolist()
    items_to_predict = [item for item in all_item_ids if item not in rated_items]

    predictions = [(item_id, model.predict(user_id, item_id).est) for item_id in items_to_predict]
    top_n = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    return top_n

class RecommendationService:
    def __init__(self):
        pass

    '''def get_recommendations(self, req: GetRecommendationRequest) -> GetRecommendationResponse:
        if strutil.is_empty(req.user_id):
            return GetRecommendationResponse(error=True, error_code=ErrorCode.BAD_REQUEST, message="Invalid input")

        recommendations = []
        recommendations.append(
            Recommendation(
                user_id=req.user_id,
                item_id="1",
                score=0.9,
            ))
        recommendations.append(
            Recommendation(
                user_id=req.user_id,
                item_id="2",
                score=0.8,
            ))
        res = GetRecommendationResponse(
            error=False,
            recommendations=recommendations
        )
        return res'''

    def get_recommendations(self, req: GetRecommendationRequest) -> GetRecommendationResponse:
        if strutil.is_empty(req.user_id):
            return GetRecommendationResponse(error=True, error_code=ErrorCode.BAD_REQUEST, message="Invalid input")

        try:
            user_id = int(req.user_id)
            top_items = get_top_n_recommendations(user_id, n=5)

            recommendations = [
                Recommendation(user_id=req.user_id, item_id=str(item_id), score=score)
                for item_id, score in top_items
            ]

            return GetRecommendationResponse(error=False, recommendations=recommendations)

        except Exception as e:
            return GetRecommendationResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))


