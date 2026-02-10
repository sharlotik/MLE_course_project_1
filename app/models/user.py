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

if TYPE_CHECKING:
    from models.event import Event


@dataclass
class User:
    """
    Класс для представления пользователя в системе.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Пароль пользователя
        balance(Decimal): Баланс пользователя
        events (List[Event]): Список событий пользователя
    """
    id: int
    email: str
    password: str
    balance: Decimal 
    events: List['Event'] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_email()
        self._validate_password()

    def _validate_email(self) -> None:
        """Проверяет корректность email."""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self) -> None:
        """Проверяет минимальную длину пароля."""
        if len(self.password) <  int(os.getenv("MIN_PASSWORD_LENGTH", 8)):
            raise ValueError("Password must be at least 8 characters long")

    def add_event(self, event: 'Event') -> None:
        """Добавляет событие в список событий пользователя."""
        self.events.append(event)
        
    def update_balance(self, change_amount: Decimal):
        self.balance += change_amount
        
    def show_balance(self):
        print(f"Ваш текущий баланс: {self.balance}")
        print("История изменений баланса:")
        for idx, evnt in enumerate(self.events):
            print(f"{idx+1}. [{evnt.report_dttm.strftime('%Y-%m-%d %H:%M')}] {evnt.title}: {evnt.amount}")
    
    def show_history(self):
        print("История запросов к модели:")
        for idx, evnt in enumerate(self.events):
            if evnt.title == 'Вызов модели':
                print(f"{idx+1}. [{evnt.report_dttm.strftime('%Y-%m-%d %H:%M')}] Файл: {evnt.image}, Результат: {evnt.result}, Изменение баланса: {evnt.amount}")
        

