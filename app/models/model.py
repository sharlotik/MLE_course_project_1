from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
import re
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime

if TYPE_CHECKING:
    from models.user import User

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