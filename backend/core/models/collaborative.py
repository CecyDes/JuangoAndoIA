from surprise import SVD, Dataset, Reader
from typing import Dict, List
import pandas as pd
import joblib
import os
from ..config import settings
from prometheus_client import Summary

MODEL_PATH = "models/collaborative_model.pkl"
TRAIN_TIME = Summary('collaborative_train_seconds', 'Tiempo de entrenamiento modelo colaborativo')

class CollaborativeRecommender:
    def __init__(self):
        self.model = None
        self.is_trained = False

    @TRAIN_TIME.time()
    def train(self, interactions: List[Dict]):
        """Entrena modelo usando factorización matricial"""
        df = pd.DataFrame([{
            'user_id': i['user_id'],
            'game_id': i['game_id'],
            'rating': i['rating']
        } for i in interactions])
        
        if len(df) < 100:
            raise ValueError("Insuficientes datos para entrenamiento colaborativo")
        
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user_id', 'game_id', 'rating']], reader)
        trainset = data.build_full_trainset()
        
        self.model = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
        self.model.fit(trainset)
        self.is_trained = True
        
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
    
    def load(self):
        """Carga modelo pre-entrenado"""
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.is_trained = True
    
    def predict(self, user_id: str, top_n: int = 5) -> List[Dict]:
        """Genera recomendaciones para un usuario"""
        if not self.is_trained:
            raise RuntimeError("Modelo no entrenado")
        
        # Lógica de predicción
        all_games = self._get_all_games()
        predictions = []
        
        for game_id in all_games:
            pred = self.model.predict(user_id, game_id)
            predictions.append({'game_id': game_id, 'score': pred.est})
        
        return sorted(predictions, key=lambda x: x['score'], reverse=True)[:top_n]

    def _get_all_games(self):
        """Obtiene lista de todos los juegos desde MongoDB"""
        # Implementar conexión a MongoDB
        return []
