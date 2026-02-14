from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import re

if TYPE_CHECKING:
    from models.event import Event

class User(SQLModel, table=True): 
    """
    User model representing application users.
    
    Attributes:
        id (int): Primary key
        email (str): User's email address
        password (str): Hashed password
        created_at (datetime): Account creation timestamp
        events (List[Event]): List of user's events
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        ...,  # Required field
        unique=True,
        index=True,
        min_length=5,
        max_length=255
    )
    password_hash: str = Field(...,  min_length=4)    # init=False, repr=False,
    #wallet: Wallet = Field(default_factory=Wallet)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    events: List["Event"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )
    
    def __str__(self) -> str:
        return f"Id: {self.id}. Email: {self.email}"

    def validate_email(self) -> bool:
        """
        Validate email format.
        
        Returns:
            bool: True if email is valid
        
        Raises:
            ValueError: If email format is invalid
        """
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(self.email):
            raise ValueError("Invalid email format")
        return True

    def __post_init__(self, password : str) -> None:
        self._validate_email()
        self.password_hash = self._validate_password(password)
        
    def _validate_email(self) -> None:
        """Проверяет корректность email."""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self, password : str) -> str:
        """Проверяет минимальную длину пароля."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return hashlib.sha256(password.encode()).hexdigest()
        
    def check_password(self, password: str) -> bool:
        """Проверка соответствия пароля."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def add_event(self, event: 'Event') -> None:
        """Добавляет событие в список событий пользователя."""
        self.events.append(event)  
        
 #   def show_history(self):
  #      print("История запросов к модели:")
   #     for idx, evnt in enumerate(self.events):
    #        if evnt.title == 'Вызов модели':
     #           print(f"{idx+1}. [{evnt.report_dttm.strftime('%Y-%m-%d %H:%M')}] Файл: {evnt.image},
      #           Результат: {evnt.result}, Изменение баланса: {evnt.amount}")


    
    @property
    def event_count(self) -> int:
        """Number of events associated with user"""
        return len(self.events)

    class Config:
        """Model configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True
