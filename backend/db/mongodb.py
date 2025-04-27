import os
from pymongo import MongoClient
from core.config import settings

def get_client():
    """
    Devuelve una instancia de MongoClient conectada a la URL de MongoDB definida en la configuración.
    """
    return MongoClient(settings.MONGODB_URL)

def get_database():
    """
    Devuelve la base de datos principal del sistema.
    """
    client = get_client()
    return client[settings.MONGODB_DB]
