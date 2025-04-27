# ml/hybrid.py

import numpy as np
from ml.collaborative import CollaborativeRecommender
from ml.content import ContentBasedRecommender

class HybridRecommender:
    def __init__(self, alpha=0.6):
        self.collaborative = CollaborativeRecommender()
        self.content = ContentBasedRecommender()
        self.alpha = alpha  # Peso del modelo colaborativo

    def load(self):
        self.collaborative.load()
        self.content.load()

    def recommend(self, user_id, game_ids, user_prefs, game_descriptions, top_n=5):
        """
        Combina scores de ambos modelos y retorna los mejores top_n juegos.
        """
        self.load()
        collab_scores = self.collaborative.predict(user_id, game_ids)
        content_scores = self.content.similarity(user_prefs, {gid: game_descriptions[gid] for gid in game_ids})

        hybrid_scores = {}
        for game_id in game_ids:
            c_score = collab_scores.get(game_id, 0)
            cont_score = content_scores.get(game_id, 0)
            hybrid_scores[game_id] = self.alpha * c_score + (1 - self.alpha) * cont_score

        # Ordenar y retornar los mejores
        ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        return [{"game_id": gid, "score": score} for gid, score in ranked[:top_n]]
