from core.models.collaborative import CollaborativeRecommender
from core.models.content import ContentBasedRecommender
from core.models.hybrid import HybridRecommender
from db.collections import users_col, games_col, interactions_col

class RecommendationEngine:
    def __init__(self):
        self.collaborative = CollaborativeRecommender()
        self.content = ContentBasedRecommender()
        self.hybrid = HybridRecommender()

    def recommend(self, user_id: str, top_n: int = 5):
        user = users_col.find_one({"_id": user_id})
        games = list(games_col.find({}))
        
        # Cold start: usuario nuevo
        if not user or not user.get("preferences"):
            return self._popular_games(top_n)
        
        # Preferencia por modelo híbrido
        self.collaborative.load()
        self.content.load()
        self.hybrid.collab_model = self.collaborative
        self.hybrid.content_model = self.content

        recommendations = self.hybrid.recommend(user_id, games, top_n)
        return recommendations

    def _popular_games(self, top_n):
        # Devuelve juegos más populares por ventas/interacciones
        games = list(games_col.find({}).sort("popularity", -1).limit(top_n))
        return [
            {"game_id": str(game["_id"]), "name": game["name"], "score": 1.0}
            for game in games
        ]
