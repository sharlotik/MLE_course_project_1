from dataclasses import dataclass, field
from typing import List
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime

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
        if len(self.password) < 8:
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
        

       
class Model:
    """
    Класс для вызова модели
    model_path (str): путь до модели
    """
    
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        self._load_model()
       
    def _load_model(self):
        if self.model_path.exists():
            self._is_loaded = True
        else:
            print(f'Ошибка загрузки модели')
            self._is_loaded = False
    
    def predict(self, input_data: str) -> str:
        """Прогноз модели для конкретного изображения"""    
        result = 'Model'.predict(input_data)
        
        return {
            "input": input_data,
            "output": result
        }

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
    image: Optional[str] = None
    result: Optional[str] = None
    description: str
    amount: Optional[Decimal] = Decimal("0.00")
    creator: User
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
            self.amount = Decimal("-0.01")
            self.creator.update_balance(self.amount) 


def main() -> None:
    try:
        ml_model = Model('model_path.txt')
        user = User(
            id=1,
            email="test@mail.ru",
            password="secure_password123",
            balance = Decimal("100.00")
        )
        
        event = Event(
            id=1,
            title="Вызов модели",
            image="image.jpg",
            description="Вызов модели",
            creator=user          
        )
        
        user.add_event(event)
        event.action(ml_model)
        print(f"Created user: {user}")
        print(f"Number of user events: {len(user.events)}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
