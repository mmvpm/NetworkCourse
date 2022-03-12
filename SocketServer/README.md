## Запуск

- `python server.py 8` - запускаем сервер с 8 потоками
- `python client.py localhost 12321 responce.py` - запрашиваем файл `responce.py`, обращаясь к `localhost:12321`

## Пример работы

- (server) > `python server.py 8`
- (server) < Server started
- (client) > `python client.py localhost 12321 response.py`
- (server) < Connection to ('127.0.0.1', 58703) opened
- (server) < Request: response.py
- (server) < Connection to ('127.0.0.1', 58703) closed
- (client) < HTTP/1.1 200 OK Content-Length: 271 (Содержимое файла)
