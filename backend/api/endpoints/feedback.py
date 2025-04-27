from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from api.core.security import get_current_user
from db.mongodb import get_db
import prometheus_client as prom

router = APIRouter(prefix="/feedback", tags=["feedback"])

# Métricas Prometheus
FEEDBACK_COUNTER = prom.Counter(
    'feedback_submissions_total',
    'Total feedback submissions',
    ['interaction_type', 'rating_category']
)

class FeedbackRequest(BaseModel):
    game_id: str
    rating: float = Field(..., ge=1, le=5)
    interaction_type: str = "click"
    context: dict = None

@router.post("/")
async def submit_feedback(
    feedback: FeedbackRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Endpoint para registrar interacciones de usuarios con las recomendaciones"""
    try:
        # Validar rating
        rating_category = "positive" if feedback.rating >= 4 else "neutral" if feedback.rating >= 2 else "negative"
        
        # Registrar en MongoDB
        feedback_data = {
            "user_id": current_user["sub"],
            "timestamp": datetime.utcnow(),
            **feedback.dict()
        }
        
        result = await db.interactions.insert_one(feedback_data)
        
        # Encolar en Kafka para procesamiento en tiempo real
        # await kafka_producer.send("user_feedback", feedback_data)
        
        # Actualizar métricas
        FEEDBACK_COUNTER.labels(
            interaction_type=feedback.interaction_type,
            rating_category=rating_category
        ).inc()
        
        return {"status": "success", "feedback_id": str(result.inserted_id)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")
