## Запуск

- `python server.py 8` - запускаем сервер с 8 потоками

## Пример работы

**GET**
- `python server.py`
- [2022-03-19 22:21:00.288227] Server started
- _делаем запрос на http://localhost:12321/https://ya.ru через браузер_
- [2022-03-19 22:21:31.591854] Connection to ('127.0.0.1', 63084) opened
- [2022-03-19 22:21:31.591854] Requested URL: https://ya.ru
- [2022-03-19 22:21:31.783157] Response code: 200
- [2022-03-19 22:21:31.784172] Connection to ('127.0.0.1', 63084) closed

**POST**
- `python server.py`
- [2022-03-19 22:28:25.096363] Server started
- _делаем POST-запрос на http://localhost:12321/https://reqres.in/api/users через Postmann_
- [2022-03-19 22:28:36.178231] Connection to ('127.0.0.1', 63229) opened
- [2022-03-19 22:28:36.178231] Requested URL: https://reqres.in/api/users
- [2022-03-19 22:28:36.178231] Request body:
{
    "name": "name",
    "job": "job name"
}
- [2022-03-19 22:28:36.453061] Response code: 201
- [2022-03-19 22:28:36.455060] Connection to ('127.0.0.1', 63229) closed
