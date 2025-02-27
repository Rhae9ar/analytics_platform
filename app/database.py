from .models import Event, ReportQuery
from clickhouse_driver import Client
import psycopg2
from dotenv import load_dotenv
import os
import json

load_dotenv()

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

ch_client = Client(host=CLICKHOUSE_HOST, user=CLICKHOUSE_USER, password=CLICKHOUSE_PASSWORD)
pg_conn = psycopg2.connect(host=POSTGRES_HOST, user=POSTGRES_USER, password=POSTGRES_PASSWORD, database=POSTGRES_DB)

def save_event(event: Event):
    """Сохранение события в ClickHouse и PostgreSQL."""
    # Пример сохранения в ClickHouse
    ch_client.execute(
        'INSERT INTO events (event_type, user_id, timestamp, metadata) VALUES',
        [(event.event_type, event.user_id, event.timestamp, json.dumps(event.metadata))]
    )
    # Пример сохранения в PostgreSQL
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute(
        'INSERT INTO events (event_type, user_id, timestamp, metadata) VALUES (%s, %s, %s, %s)',
        (event.event_type, event.user_id, event.timestamp, json.dumps(event.metadata))
    )
    pg_conn.commit()

def get_reports(query: ReportQuery):
    """Получение отчётов из ClickHouse."""
    # Пример запроса к ClickHouse
    result = ch_client.query_dataframe(
        f"SELECT {query.group_by}, count() FROM events WHERE timestamp >= '{query.date_from}' AND timestamp <= '{query.date_to}' GROUP BY {query.group_by}"
    )
    return result.to_dict(orient='records')

def get_unique_users():
    """Подсчёт уникальных пользователей."""
    result = ch_client.execute("SELECT COUNT(DISTINCT user_id) FROM events")
    return result[0][0]

def get_unique_event_types():
    """Подсчёт уникальных типов событий."""
    result = ch_client.execute("SELECT COUNT(DISTINCT event_type) FROM events")
    return result[0][0]

# Аналогично для сессий