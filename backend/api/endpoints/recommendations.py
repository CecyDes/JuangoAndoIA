from fastapi import APIRouter, Depends, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.security import get_current_user
from db.mongodb import get_db
from backend.models.recommendation import GameRecommendation
from services.recommender import HybridRecommender
import prometheus_client as prom

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Métricas Prometheus
RECOMMENDATION_COUNTER = prom.Counter(
    'recommendation_requests_total',
    'Total recommendation requests',
    ['user_type', 'status']
)
LATENCY_HISTOGRAM = prom.Histogram(
    'recommendation_latency_seconds',
    'Recommendation processing latency'
)

@router.get("/{user_id}", response_model=List[GameRecommendation])
async def get_recommendations(
    user_id: str,
    limit: int = 5,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Endpoint principal para obtener recomendaciones personalizadas"""
    with LATENCY_HISTOGRAM.time():
        try:
            # Verificar permisos
            if current_user["sub"] != user_id:
                raise HTTPException(status_code=403, detail="Unauthorized access")
            
            # Obtener recomendaciones
            recommender = HybridRecommender(db)
            recommendations = await recommender.generate(user_id, limit)
            
            # Registrar métricas
            user_type = "new" if await db.users.count_documents({"_id": user_id}) == 0 else "existing"
            RECOMMENDATION_COUNTER.labels(user_type=user_type, status="success").inc()
            
            return recommendations

        except HTTPException as he:
            RECOMMENDATION_COUNTER.labels(user_type="unknown", status="error").inc()
            raise he
        except Exception as e:
            RECOMMENDATION_COUNTER.labels(user_type="unknown", status="error").inc()
            raise HTTPException(status_code=500, detail=str(e))

