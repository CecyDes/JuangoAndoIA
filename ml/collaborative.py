# ml/collaborative.py

import pandas as pd
from surprise import Dataset, Reader, SVD
import joblib
import os

MODEL_PATH = "ml/models/collaborative_model.pkl"

class CollaborativeRecommender:
    def __init__(self):
        self.model = None

    def train(self, interactions: pd.DataFrame):
        """
        Entrena el modelo SVD con los datos de interacciones.
        interactions: DataFrame con columnas ['user_id', 'game_id', 'rating']
        """
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(interactions[['user_id', 'game_id', 'rating']], reader)
        trainset = data.build_full_trainset()
        self.model = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
        self.model.fit(trainset)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

    def load(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, user_id, game_ids):
        """
        Devuelve un diccionario {game_id: score} para los juegos dados.
        """
        if self.model is None:
            self.load()
        return {game_id: self.model.predict(user_id, game_id).est for game_id in game_ids}
