from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Dict
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime
import hashlib
from abc import ABC, abstractmethod

                 
@dataclass
class Transaction(ABC):
    """
    Абстрактный класс для транзакций.
    
    Attributes:
        id (int): Уникальный идентификатор транзакции
        txn_type (str): Тип транзакции
        amount (Decimal): Сумма транзакции
        report_dttm: datetime Время транзакции
    """
    id: int
    txn_type: str
    amount: Decimal
    report_dttm: datetime = field(default_factory=datetime.now)

    @abstractmethod
    def execute(self, wallet: 'Wallet'):
        pass

class DepositTransaction(Transaction):
    """
    Класс для пополнения баланса (наследование от Transaction)
    
    Переопределяем excute - полиморфизм.
    """
    def execute(self, wallet: 'Wallet'):
        wallet.balance += self.amount
        wallet.history.append(self)

class ServiceTransaction(Transaction):
    """
    Класс для списаний за пользование сервисом (наследование от Transaction)
    
    Переопределяем excute - полиморфизм.
    """
    def execute(self, wallet: 'Wallet'):
        if wallet.balance < self.amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= self.amount
        wallet.history.append(self)
        
@dataclass
class Wallet:
    """
    Класс для кошелька.
    
    Attributes:
        balance (Decimal): Баланс
        history: История транзакций
    """
    balance: Decimal = Decimal("0.00")
    history: List[Transaction] = field(default_factory=list)

    @property
    def balance_amount(self) -> Decimal:
        return self.balance
        
    @property            
    def balance_history(self):
        print("История изменений баланса:")
        for idx, txn in enumerate(self.history):
            print(f"{idx+1}. [{txn.report_dttm.strftime('%Y-%m-%d %H:%M')}] {txn.txn_type}: {txn.amount}")
            

       
@dataclass
class User:
    """
    Класс для представления пользователя в системе.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): пароль пользователя, для инициализации
        password_hash(str): Hash пароля пользователя
        wallet: Данные по балансу пользователя
        events (List[Event]): Список событий пользователя
    """
    id: int
    email: str
    password: InitVar[str]
    password_hash: str = field(init=False, repr=False)
    wallet: Wallet = field(default_factory=Wallet)
    events: List['Event'] = field(default_factory=list)

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
        
    def show_history(self):
        print("История запросов к модели:")
        for idx, evnt in enumerate(self.events):
            if evnt.title == 'Вызов модели':
                print(f"{idx+1}. [{evnt.report_dttm.strftime('%Y-%m-%d %H:%M')}] Файл: {evnt.image}, Результат: {evnt.result}, Изменение баланса: {evnt.amount}")


@dataclass
class Admin(User):
    """
    Класс администратора (наследование от User).
   
    Attributes:
        role (str): Роль пользователя
        admin_logs: Логи администратора
    
    """
    
    role: str = field(default="admin", init=False)
    admin_logs: List[str] = field(default_factory=list, init=False)

    def log_action(self, action: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.admin_logs.append(f"[{timestamp}] Admin ID {self.id}: {action}")

    def delete_user(self, user: User) -> None:
        self.log_action(f"Deleted user {user.id}")
        print(f"User {user.email} removed.")
     

class BillingService:
    """ Класс для обработки транзакций"""
    
    @staticmethod
    def execute_transaction(user: User, amount: Decimal, txn_class: type):
        txn_id = len(user.wallet.history) + 1
        txn = txn_class(id = txn_id, amount = amount, txn_type = txn_class.__name__)
        
        txn.execute(user.wallet)
        
        record = TransactionRecord(
            txn_id = txn.id,
            user_id = user.id,
            txn_type = txn.txn_type,
            amount = txn.amount
        )
        HistoryManager.add_transaction(record)

        
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
        creator (User): Создатель события
        description (str): Описание события
        image (str): Путь к изображению события
        result(str): Результат модели
        amount (Decimal): Сумма для пополнения баланса        
        report_dttm (datetime): Дата и время события
    """
    id: int
    title: str
    creator: User
    description: str
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
           
    def action(self, model: Optional[Model], billing : BillingService) -> None:
        if self.title == 'Пополнение баланса':
            if self.amount <= 0:
                raise ValueError("Deposit amount must be positive")
            billing.execute_transaction(self.creator, self.amount, DepositTransaction)
            
        elif self.title == 'Вызов модели':
            if not model:
                raise ValueError("Model is required for this action")
            prediction = model.predict(self.image)
            self.result = prediction["output"]
            self.amount = Decimal("0.01") 
            billing.execute_transaction(self.creator, self.amount, ServiceTransaction)
                        
            pred_record = PredictionRecord(
                prediction_id = len(HistoryManager.predictions) + 1,
                user_id = self.creator.id,
                input_image = self.image,
                output_result = self.result
            )
            HistoryManager.add_prediction(pred_record)
        

@dataclass(frozen=True)
class TransactionRecord:
    
    """Класс записи истории транзакций
    
    Attributes:
        txn_id (int): id транзакции
        user_id (int): id пользователя
        txn_type (str): тип транзакции
        amount (Decimal): сумма транзакции
        timestamp (datetime): время совершения транзакции
        status (str) : статус
    """
    
    txn_id: int
    user_id: int
    txn_type: str
    amount: Decimal
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "success"

    def __repr__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] TXN-{self.txn_id}: {self.txn_type} | {self.amount} | User: {self.user_id}"
        

@dataclass(frozen=True)
class PredictionRecord:
        """Класс записи истории предсказаний
    
    Attributes:
        prediction_id (int): id предсказания
        user_id (int): id пользователя
        input_image (str): изображение
        output_result (str): результат модели
        timestamp (datetime): время совершения транзакции
    """
    prediction_id: int
    user_id: int
    input_image: str
    output_result: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] PREDICT-{self.prediction_id}: User {self.user_id} | Res: {self.output_result}"


class HistoryManager:
    
    """ Класс для хранения истории событий 
    
    Attributes:
        transactions: Транзакции
        predictions: Предсказания
    """
    
    transactions: List[TransactionRecord] = []
    predictions: List[PredictionRecord] = []

    @classmethod
    def add_transaction(cls, record: TransactionRecord):
        cls.transactions.append(record)

    @classmethod
    def add_prediction(cls, record: PredictionRecord):
        cls.predictions.append(record)


            
def main() -> None:
    try:
        ml_model = Model('model_path.txt')
        billing = BillingService()
        
        user = User(
            id=1,
            email="test@mail.ru",
            password = "secure_password123"
        )
        
        dep_event = Event(
            id=1, 
            title="Пополнение баланса", 
            amount = Decimal("10.00"), 
            description="Initial deposit", 
            creator=user)
        user.add_event(dep_event)
        dep_event.action(None, billing)
        
        model_event = Event(
            id=2,
            title="Вызов модели",
            image="image.jpg",
            description="Birds recognition",
            creator=user          
        )
        user.add_event(model_event)
        model_event.action(ml_model, billing)
        
        
        print(f"Created user: {user}")
        print(f"Number of user events: {len(user.events)}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()


