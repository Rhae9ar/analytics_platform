from fastapi import FastAPI, Depends, HTTPException, status
from . import database, auth
from .models import Event, ReportQuery
from typing import List

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded



app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/reports/")
async def get_reports(query: ReportQuery, current_user: str = Depends(auth.get_current_user)):
    """Получение отчётов."""
    reports = database.get_reports(query)
    return reports

@app.get("/dashboard/")
async def get_dashboard(current_user: str = Depends(auth.get_current_user)):
    """Получение визуализаций."""
    
    events_by_type = database.get_events_by_type()
    return {"events_by_type": events_by_type}


@app.post("/events/", dependencies=[Depends(limiter.limit("10/minute"))])
async def create_event(event: Event, current_user: dict = Depends(auth.get_current_user)):
    """Приём событий с ограничением количества запросов."""
    # Логика сохранения события в базу данных и Kafka
    return {"status": "ok"}

# app/main.py
from fastapi import Depends, HTTPException, status, FastAPI
from . import auth

app = FastAPI()

@app.get("/users/")
async def get_users(current_user: dict = Depends(auth.get_current_user)):
    """Получение списка пользователей (только для администраторов)."""
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    # Здесь дописать логику получения списка пользователей из базы данных
    users = [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]
    return users


@app.get("/limited/", dependencies=[Depends(limiter.limit("5/minute"))])
async def limited():
    """Endpoint с ограничением количества запросов."""
    return {"message": "Limited access"}