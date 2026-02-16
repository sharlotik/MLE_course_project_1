from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Dict
from sqlmodel import SQLModel, Field, Relationship
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime
import hashlib
from abc import ABC, abstractmethod

                 
@dataclass
class Transaction(SQLModel):
    """
    Класс для транзакций.
    
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

    def execute(self, wallet: 'Wallet'):
        if self.txn_type == 'Deposit':
            wallet.balance += self.amount
            wallet.history.append(self)
            
        elif self.txn_type == 'Service':
            if wallet.balance < self.amount:
                raise ValueError("Insufficient funds")
            wallet.balance -= self.amount
            wallet.history.append(self)