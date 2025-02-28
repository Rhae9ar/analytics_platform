# Аналитическая платформа

Аналитическая платформа для сбора, хранения и анализа пользовательских событий в веб-приложениях. Позволяет собирать логи, строить отчёты и визуализировать данные.

## Технологический стек

-   Backend: FastAPI
-   Message Broker: Kafka
-   Storage: ClickHouse (аналитика), PostgreSQL (логирование)
-   Task Queue: Celery
-   Frontend: React + Recharts / Grafana
-   Deployment: Docker + Kubernetes
-   Monitoring: Prometheus + Grafana

## Запуск проекта

1.  Клонируйте репозиторий:

    ```bash
    git clone (https://github.com/Rhae9ar/analytics_platform.git)
    ```

2.  Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    venv\Scripts\activate # Windows
    ```

3.  Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4.  Настройте переменные окружения:

    -   Создайте файл `.env` в корне проекта и добавьте необходимые переменные.

5.  Запустите ClickHouse и Kafka с помощью Docker Compose:

    ```bash
    docker-compose up -d
    ```

6.  Запустите приложение:

    ```bash
    uvicorn app.main:app --reload
    ```

7.  Запустите Celery воркер:

    ```bash
    celery -A app.tasks worker --loglevel=info
    ```

8.  Запустите React приложение:

    ```bash
    cd dashboard
    npm install
    npm start
    ```

## Настройка ClickHouse

-   Для партиционирования данных по времени создайте таблицу `events` с партиционированием по месяцам:

    ```sql
    CREATE TABLE events (
        event_type String,
        user_id String,
        timestamp DateTime,
        metadata String
    )
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (timestamp);
    ```

-   Для автоматической очистки старых данных установите TTL:

    ```sql
    ALTER TABLE events
        MODIFY TTL timestamp + INTERVAL 1 YEAR;
    ```

-   Для подсчёта уникальных пользователей, событий и сессий используйте запросы:

    ```sql
    -- Уникальные пользователи
    SELECT COUNT(DISTINCT user_id) FROM events;
    
    -- Уникальные типы событий
    SELECT COUNT(DISTINCT event_type) FROM events;
    
    -- Уникальные сессии (если есть поле session_id)
    SELECT COUNT(DISTINCT session_id) FROM events;
    ```

## API endpoints

-   `POST /events/`: Приём событий.
-   `GET /reports/`: Получение отчётов.
-   `GET /dashboard/`: Получение визуализаций.
-   `GET /users/`: Получение списка пользователей (только для администраторов).
-   `POST /create_resource/`: Создание ресурса (с ограничением POST-запросов).
-   `GET /get_resource/`: Получение ресурса (с ограничением GET-запросов).

## Тестирование

-   Запустите тесты с помощью pytest:

    ```bash
    pytest --cov=app tests/
    ```

## Развёртывание

-   Для развёртывания приложения используйте Docker и Kubernetes.
-   Настройте мониторинг с помощью Prometheus и Grafana.


