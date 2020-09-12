# url_shortener
## HTTP сервис для сокращения URL на FastAPI + PostgreSQL
Тестовое задание на позицию стажера-бекендера в юнит Авито Авто.  
Задание: http://bit.ly/avito-auto-be
### Запуск
```
docker-compose up
```   
Сервис будет работать на http://0.0.0.0:8000/
### API
#### POST /app/{url}
Преобразует длинный URL в короткий  
Пример запроса:
```
POST /app/avito.ru/
```
Пример ответа:
```
{"short_url": "0.0.0.0:8000/y3jdq"}
```
Поддерживает разнообразные типы ссылок, в т.ч. https://www.avito.ru/ , https://www.avito.ru/moskva/transport?cd=1  
Имеется валидация URL
```
POST /app/not_valid_url
```
```
{"detail": "Bad URL"}
```
#### POST /app/{short_url}/convert_to/{url}
Задать кастомную ссылку для длинного URL  
Пример запроса:
```
POST /app/avito-cars/convert_to/https://www.avito.ru/moskva/transport?cd=1/
```
Пример ответа:
```
{"short_url": "0.0.0.0:8000/avito-cars"}
```
#### GET /app/{short_url}
redirect на исходный URL  
Пример запроса:
```
GET /app/avito-cars
```
