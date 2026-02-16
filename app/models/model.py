from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
import torch
import urllib.request
from PIL import Image
from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification

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
        preprocessor = EfficientNetImageProcessor.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
        model = EfficientNetForImageClassification.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")

      #  else:
       #     print(f'Ошибка загрузки модели')
        #    self._is_loaded = False
    
    def predict(self, input_data: str) -> str:
        """Прогноз модели для конкретного изображения"""    

        
        # Determining the file URL
        url = 'some url'

        # Opening the image using PIL
        img = Image.open(urllib.request.urlretrieve(url)[0])

        # Loading the model and preprocessor from HuggingFace

        # Preprocessing the input
        inputs = preprocessor(img, return_tensors="pt")

        # Running the inference
        with torch.no_grad():
            logits = model(**inputs).logits

        # Getting the predicted label
        predicted_label = logits.argmax(-1).item()
        result = model.config.id2label[predicted_label]
        
        return {
            "input": input_data,
            "output": result
        }