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
#### POST /short?url={url}
Преобразует длинный URL в короткий  
Пример запроса:
```
POST /short?url=avito.ru
```
Пример ответа:
```
{"short_url": "0.0.0.0:8000/LcFMv2n"}
```
Поддерживает разнообразные типы ссылок, в т.ч. https://www.avito.ru/ , https://www.avito.ru/moskva/transport?cd=1  
Имеется валидация URL
```
POST /short?url=not_valid_url
```
```
{"detail": "Bad URL"}
```
#### POST /short?url={url}&short_url={short_url}
Задать кастомную ссылку для длинного URL  
Пример запроса:
```
POST /short?url=https://www.avito.ru/moskva/transport?cd=1&short_url=avito-cars
```
Пример ответа:
```
{"short_url": "0.0.0.0:8000/avito-cars"}
```
Ссылку нельзя перезаписать  
```
POST /short?url=https://www.avito.ru/&short_url=avito-cars
```
```
{"detail": "Short URL already used"}
```
#### GET /{short_url}
redirect на исходный URL  
Пример запроса:
```
GET /avito-cars
```
### Нагрузочное тестирование
https://bit.ly/2ZBdkAx  
![test](/images/rps.png)
### Тесты
Coming soon
