
from celery import Celery
from .database import ch_client

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def aggregate_metrics():
    """Фоновая агрегация метрик."""
    # Пример агрегации данных
    result = ch_client.query_dataframe("SELECT event_type, count() FROM events GROUP BY event_type")
    # ... (сохранение агрегированных данных)