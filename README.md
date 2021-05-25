# Проектная работа 8 спринта

Проект содержит 2 сервиса: сервис аналитики и ETL сервис.

### Сервис аналитики
Принимает запросы от клиентов и сохраняет данные в Kafka.

### ETL сервис
Отправляет данные из Kafka в CLickhouse.

<hr>
Оба сервиса используют один общий docker-compose файл, но между собой они разделены.

## Развертывание
1. Для каждого сервиса требуется прописать переменные в .env файле рядом с директорий src.  
Пример переменных можно найти в example.env.

2. Создать сеть `ugc`:
   ```shell
   docker-network create ugc
    ```
3. Построить контейнеры:
    ```shell
    docker-compose build
    ```
   
4. Поднять контейнеры
    ```shell
    docker-compose up
    ```


<hr>

### Примеры запросов:
Создать событие об истории просмотра фильма:
```shell
curl --location --request POST 'http://127.0.0.1:8000/collect' \
--header 'Content-Type: application/json' \
--data-raw '{
    "payload": {
        "movie_timestamp": 1621932759,
        "movie_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2",
        "user_id": "1ec4cd73-2fd5-4f25-af68-b6595d279af2"
    },
    "timestamp": 1,
    "language": "RU",
    "timezone": "Europe/Moscow",
    "fingerprint": {},
    "ip": "192.168.1.1",
    "type": "history",
    "version": "1.1"
}'
```