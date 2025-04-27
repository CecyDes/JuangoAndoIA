import numpy as np
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import os
import joblib
from ..config import settings
from typing import List, Dict

nltk.download('punkt')
nltk.download('stopwords')

MODEL_PATH = "models/content_model.pkl"

class ContentBasedRecommender:
    def __init__(self):
        self.model = None
        self.stop_words = set(stopwords.words('spanish'))
        self.is_trained = False

    def preprocess_text(self, text: str) -> List[str]:
        """Procesamiento de texto para descripciones"""
        tokens = word_tokenize(text.lower())
        return [w for w in tokens if w.isalpha() and w not in self.stop_words]

    def train(self, games: List[Dict]):
        """Entrena modelo Word2Vec"""
        descriptions = [self.preprocess_text(g['description']) for g in games]
        
        self.model = Word2Vec(
            sentences=descriptions,
            vector_size=100,
            window=5,
            min_count=1,
            workers=4
        )
        self.is_trained = True
        joblib.dump(self.model, MODEL_PATH)
    
    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.is_trained = True
    
    def get_game_vector(self, description: str) -> np.ndarray:
        """Obtiene vector promedio para una descripción"""
        tokens = self.preprocess_text(description)
        vectors = [self.model.wv[word] for word in tokens if word in self.model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)
    
    def recommend(self, user_preferences: List[str], games: List[Dict], top_n=5) -> List[Dict]:
        """Genera recomendaciones basadas en preferencias"""
        if not self.is_trained:
            raise RuntimeError("Modelo no entrenado")
        
        # Lógica de recomendación
        user_vector = np.mean([self.model.wv[pref] for pref in user_preferences if pref in self.model.wv], axis=0)
        
        recommendations = []
        for game in games:
            game_vector = self.get_game_vector(game['description'])
            similarity = np.dot(user_vector, game_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(game_vector))
            recommendations.append({'game_id': game['_id'], 'score': similarity})
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:top_n]
