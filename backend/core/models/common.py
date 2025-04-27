from pydantic import BaseModel
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorCollection

class Recommendation(BaseModel):
    game_id: str
    score: float
    algorithm: str
    metadata: Dict = {}

async def get_user_interactions(user_col: AsyncIOMotorCollection, user_id: str) -> List[Dict]:
    return await user_col.find_one(
        {"_id": user_id},
        {"interactions": 1}
    )

async def get_popular_games(games_col: AsyncIOMotorCollection, limit=5) -> List[Dict]:
    return await games_col.find().sort("popularity", -1).limit(limit).to_list(length=limit)
