from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from models.user import User

class EventBase(SQLModel):
    """
    Base Event model with common fields.
    
    Attributes:
        title (str): Event title
        image (str): URL or path to event image
        description (str): Event description
        location (Optional[str]): Event location
        tags (Optional[List[str]]): Event tags
    """
    title: str = Field(..., min_length=1, max_length=100)
    image: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1, max_length=1000)


class Event(EventBase, table=True):
    """
    Event model representing events in the system.
    
    Attributes:
        id (Optional[int]): Primary key
        creator_id (Optional[int]): Foreign key to User
        creator (Optional[User]): Relationship to User
        created_at (datetime): Event creation timestamp
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional["User"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    description: Optional[str]
    result: Optional[str] = None
    amount: Optional[Decimal] = Decimal("0.00")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def __str__(self) -> str:
        result = (f"Id: {self.id}. Title: {self.title}. Creator: {self.creator.email}")
        return result

    def __post_init__(self) -> None:
        self._validate_title()
        self._validate_description()

    def _validate_title(self) -> None:
        """Проверяет длину названия события."""
        if not 1 <= len(self.title) <= 100:
            raise ValueError("Title must be between 1 and 100 characters")

    def _validate_description(self) -> None:
        """Проверяет длину описания события."""
        if len(self.description) > 500:
            raise ValueError("Description must not exceed 500 characters")            
           
 ##   def action(self, model: Optional[Model], billing : BillingService) -> None:
 ##       if self.title == 'Пополнение баланса':
 ##           if self.amount <= 0:
  ##              raise ValueError("Deposit amount must be positive")
    ##        billing.execute_transaction(self.creator, self.amount, 'Deposit')
            
      ##  elif self.title == 'Вызов модели':
        ##    if not model:
          ##      raise ValueError("Model is required for this action")
           ## prediction = model.predict(self.image)
           ## self.result = prediction["output"]
            ##self.amount = Decimal("0.01") 
            ##billing.execute_transaction(self.creator, self.amount, 'Service')
                        
          ##  pred_record = PredictionRecord(
           ##     prediction_id = len(HistoryManager.predictions) + 1,
           ##     user_id = self.creator.id,
            ##    input_image = self.image,
            ##    output_result = self.result
            ##)
            ##HistoryManager.add_prediction(pred_record)
    
    @property
    def short_description(self) -> str:
        """Returns truncated description for preview"""
        max_length = 100
        return (f"{self.description[:max_length]}..."
                if len(self.description) > max_length
                else self.description)

class EventCreate(EventBase):
    """Schema for creating new events"""
    pass

class EventUpdate(EventBase):
    """Schema for updating existing events"""
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        """Model configuration"""
        validate_assignment = True