import numpy as np
from typing import List, Dict
from .collaborative import CollaborativeRecommender
from .content import ContentBasedRecommender
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate

HYBRID_MODEL_PATH = "models/hybrid_model.h5"

class HybridRecommender:
    def __init__(self):
        self.collab_model = CollaborativeRecommender()
        self.content_model = ContentBasedRecommender()
        self.neural_model = None
        self.is_trained = False
    
    def build_neural_model(self, num_users: int, num_games: int):
        """Construye modelo de red neuronal para combinar scores"""
        user_input = Input(shape=(1,))
        game_input = Input(shape=(1,))
        
        user_embed = Flatten()(Embedding(num_users, 50)(user_input))
        game_embed = Flatten()(Embedding(num_games, 50)(game_input))
        
        concat = Concatenate()([user_embed, game_embed])
        dense = Dense(128, activation='relu')(concat)
        output = Dense(1, activation='sigmoid')(dense)
        
        self.neural_model = Model(inputs=[user_input, game_input], outputs=output)
        self.neural_model.compile(optimizer='adam', loss='mse')
    
    def recommend(self, user_id: str, games: List[Dict], top_n=5) -> List[Dict]:
        """Genera recomendaciones híbridas"""
        collab_recs = self.collab_model.predict(user_id, len(games))
        content_recs = self.content_model.recommend(user_id, games, len(games))
        
        # Combinar scores usando red neuronal
        hybrid_scores = {}
        for game in games:
            collab_score = next(r['score'] for r in collab_recs if r['game_id'] == game['_id'])
            content_score = next(r['score'] for r in content_recs if r['game_id'] == game['_id'])
            
            # Predecir con modelo neuronal
            nn_input = [np.array([user_id]), np.array([game['_id']])]
            hybrid_score = self.neural_model.predict(nn_input)[0][0]
            
            hybrid_scores[game['_id']] = {
                'final_score': 0.6 * collab_score + 0.4 * content_score + 0.2 * hybrid_score,
                'metadata': {
                    'collab_score': collab_score,
                    'content_score': content_score
                }
            }
        
        return sorted(hybrid_scores.items(), key=lambda x: x[1]['final_score'], reverse=True)[:top_n]

