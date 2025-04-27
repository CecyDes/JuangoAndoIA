# ml/content.py

import numpy as np
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import joblib
import os

nltk.download('punkt')
nltk.download('stopwords')

MODEL_PATH = "ml/models/content_model.pkl"

class ContentBasedRecommender:
    def __init__(self):
        self.model = None
        self.stop_words = set(stopwords.words('spanish'))

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return [w for w in tokens if w.isalpha() and w not in self.stop_words]

    def train(self, descriptions):
        """
        descriptions: lista de strings (descripciones de juegos)
        """
        processed = [self.preprocess(desc) for desc in descriptions]
        self.model = Word2Vec(sentences=processed, vector_size=100, window=5, min_count=1, workers=4)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

    def load(self):
        self.model = joblib.load(MODEL_PATH)

    def get_vector(self, text):
        tokens = self.preprocess(text)
        vectors = [self.model.wv[w] for w in tokens if w in self.model.wv]
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.model.vector_size)

    def similarity(self, user_prefs, game_descriptions):
        """
        user_prefs: lista de palabras clave del usuario
        game_descriptions: dict {game_id: description}
        Devuelve {game_id: score}
        """
        if self.model is None:
            self.load()
        user_vec = np.mean([self.model.wv[w] for w in user_prefs if w in self.model.wv], axis=0)
        scores = {}
        for game_id, desc in game_descriptions.items():
            game_vec = self.get_vector(desc)
            if np.linalg.norm(user_vec) == 0 or np.linalg.norm(game_vec) == 0:
                scores[game_id] = 0
            else:
                scores[game_id] = float(np.dot(user_vec, game_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(game_vec)))
        return scores
