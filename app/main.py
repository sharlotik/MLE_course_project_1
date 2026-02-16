from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, List, TYPE_CHECKING
import models.user
import uvicorn
import logging
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Optional
from datetime import datetime


#if TYPE_CHECKING:
from models.user import User
from models.event import Event
from models.model import Model

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Сервисное API",
    description="API для управления событиями",
    version="1.0.0"
)
#app.state.model = getmodel()
@app.get("/", response_model=Dict[str, str])
#async def index(request: Request) -> Dict[str, str]:
async def index() -> Dict[str, str]:
    """
    Корневой эндпоинт, возвращающий приветственное сообщение с информацией о пользователе.
    
    Returns:
        Dict[str, str]: Приветственное сообщение с информацией о пользователе
    """
    try:
       # model = request.app.state.model
        user = User(id=1, email="Nick@gmail.com", password="12345678",
        balance = 0.00) 
        event = Event(
            id=1,
            title="Вызов модели",
            image="image.jpg",
            description="Вызов модели",
            creator=user          
        )
        user.add_event(event)
        logger.info(f"Успешное выполнение маршрута index для пользователя: {user}")
        # event.action(ml_model)
        #print(f"Created user: {user}")
        #print(f"Number of user events: {len(user.events)}")
        return {"message": f"Hello! User: {user}"}
    except Exception as e:
        logger.error(f"Ошибка в маршруте index: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

        

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Эндпоинт проверки работоспособности для мониторинга.
    
    Returns:
        Dict[str, str]: Сообщение о статусе
    """
    logger.info("Эндпоинт health_check успешно вызван")
    return {"status": "healthy"}

# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTPException: {exc.detail} для запроса {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
        log_level="debug"
    )

