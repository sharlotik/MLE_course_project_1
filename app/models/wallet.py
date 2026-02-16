from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from models.transaction import Transaction

class Wallet(SQLModel, table=True):
    """
    Класс для кошелька.
    
    Attributes:
        balance (Decimal): Баланс
        history: История транзакций
    """
    balance: Decimal = Decimal("0.00")
    history: List[Transaction] = Field(default_factory=list)

    @property
    def balance_amount(self) -> Decimal:
        return self.balance
        
      
    def balance_history(self):
        print("История изменений баланса:")
        for idx, txn in enumerate(self.history):
            print(f"{idx+1}. [{txn.report_dttm.strftime('%Y-%m-%d %H:%M')}] {txn.txn_type}: {txn.amount}")