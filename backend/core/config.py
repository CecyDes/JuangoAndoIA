import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field
from typing import List

# Carga variables de entorno desde .env si existe
load_dotenv()

class Settings(BaseSettings):
    # Información general del proyecto
    PROJECT_NAME: str = Field("JugandoAndo IA", env="PROJECT_NAME")
    API_V1_STR: str = "/api"
    
    # Seguridad y autenticación
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 7, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # 1 semana

    # Configuración de la base de datos MongoDB
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    MONGODB_DB: str = Field("jugandoando", env="MONGODB_DB")
    MAX_CONNECTIONS_COUNT: int = Field(10, env="MAX_CONNECTIONS_COUNT")
    MIN_CONNECTIONS_COUNT: int = Field(1, env="MIN_CONNECTIONS_COUNT")

    # CORS y hosts permitidos
    ALLOWED_HOSTS: List[str] = Field(["*"], env="ALLOWED_HOSTS")

    # Otras configuraciones (Kafka, métricas, etc.)
    KAFKA_BROKER_URL: str = Field("localhost:9092", env="KAFKA_BROKER_URL")
    PROMETHEUS_ENABLED: bool = Field(True, env="PROMETHEUS_ENABLED")

    class Config:
        case_sensitive = True

settings = Settings()
