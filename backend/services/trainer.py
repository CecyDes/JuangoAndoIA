import logging
from core.models.collaborative import CollaborativeRecommender
from core.models.content import ContentBasedRecommender
from core.models.hybrid import HybridRecommender
from db.collections import interactions_col, games_col

logger = logging.getLogger("jugandoando_ia.trainer")

class ModelTrainer:
    def __init__(self):
        self.collaborative = CollaborativeRecommender()
        self.content = ContentBasedRecommender()
        self.hybrid = HybridRecommender()

    def train_all(self):
        # Entrenar filtrado colaborativo
        interactions = list(interactions_col.find({}))
        if len(interactions) < 100:
            logger.warning("Pocos datos de interacción para entrenamiento colaborativo")
        else:
            self.collaborative.train(interactions)
            logger.info("Modelo colaborativo entrenado")
        
        # Entrenar basado en contenido
        games = list(games_col.find({}))
        if len(games) < 50:
            logger.warning("Pocos juegos para entrenamiento de contenido")
        else:
            self.content.train(games)
            logger.info("Modelo de contenido entrenado")
        
        # Entrenar modelo híbrido (si aplica)
        self.hybrid.collab_model = self.collaborative
        self.hybrid.content_model = self.content
        logger.info("Modelo híbrido actualizado")

    def update_models(self):
        # Método para actualizar modelos periódicamente (puede usarse con un scheduler)
        self.train_all()
        logger.info("Todos los modelos han sido actualizados")
