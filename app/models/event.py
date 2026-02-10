from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# if TYPE_CHECKING:
from models.user import User
from models.model import Model

@dataclass
class Event:
    """
    Класс для представления события.
    
    Attributes:
        id (int): Уникальный идентификатор события
        title (str): Название события
        image (str): Путь к изображению события
        result(str): Результат модели
        description (str): Описание события
        amount (Decimal): Сумма для пополнения баланса
        creator (User): Создатель события
        report_dttm (datetime): Дата и время события
    """
    id: int
    title: str
    description: str
    creator: User
    image: Optional[str] = None
    result: Optional[str] = None
    amount: Optional[Decimal] = Decimal("0.00")
    report_dttm: datetime = field(default_factory=datetime.now)

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
            
    def action(self, model: Optional[Model]) -> None:
        if self.title == 'Пополнение баланса':
            if self.amount <= 0:
                raise ValueError("Value must be positive")
            else:
                self.creator.update_balance(self.amount)
            
        if self.title == 'Вызов модели':
            self.result = model.predict(self.image)
            self.amount = Decimal(os.getenv("MODEL_INFERENCE_COST"))
            self.creator.update_balance(self.amount) 