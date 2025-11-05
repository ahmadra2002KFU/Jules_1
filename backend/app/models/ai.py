"""AI-related models."""
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, ForeignKey
from backend.app.models.base import BaseModel


class AITrainingData(BaseModel):
    """AI Training Data model."""
    __tablename__ = "ai_training_data"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    data_type = Column(String, nullable=False, index=True)
    input_data = Column(String, nullable=False)  # JSON
    output_data = Column(String, nullable=False)  # JSON
    confidence_score = Column(Numeric(5, 4))
    is_validated = Column(Boolean, default=False, nullable=False)
    validated_by = Column(String)
    validated_at = Column(DateTime)


class AIPrediction(BaseModel):
    """AI Prediction model."""
    __tablename__ = "ai_predictions"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    prediction_type = Column(String, nullable=False, index=True)
    entity_type = Column(String)
    entity_id = Column(String)
    input_features = Column(String)  # JSON
    prediction_value = Column(String)  # JSON
    confidence_score = Column(Numeric(5, 4))
    model_version = Column(String)
    prediction_date = Column(DateTime)
    actual_value = Column(String)  # JSON
    accuracy_score = Column(Numeric(5, 4))


class AIChatHistory(BaseModel):
    """AI Chat History model."""
    __tablename__ = "ai_chat_history"

    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, nullable=False, index=True)
    message_type = Column(String, nullable=False)
    message_text = Column(String, nullable=False)
    message_metadata = Column(String)  # JSON
    timestamp = Column(DateTime)
