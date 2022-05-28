## Демонстрация токена доступа

- Создаем продукт

![post without token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/post-wt.png)

- Регистрируем нового пользователя

![register user](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/register.png)

- Создаем продукт, указав полученный токен доступа

![post with token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/post-t.png)

- Получаем список продуктов, доступных всем (то есть только 1 продукт)

![getAll without token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/get-all-wt.png)

- Получаем список продуктов, указав токен доступа (теперь уже 2 продукта)

![getAll without token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/get-all-t.png)

## Демонстрация отправки e-mail

- Регистрируем нового пользователя с нужной почтой

![register user](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/register-me.png)

- Делаем несколько запросов получения списка продуктов, не указывая полученный токен доступа.

![getAll without token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/get-all-wt-me.png)

- Через некоторое время, как и ожадалось, на почту приходит единственное письмо

![getAll without token](https://github.com/IdeaSeeker/NetworkCourse/blob/main/RestService2/example/email.png)
