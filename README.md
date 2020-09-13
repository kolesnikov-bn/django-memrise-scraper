# django-memrise-scraper
Django приложение для скачивания, извлечения и управления учебными курсами memrise dashboard

В первую очередь проект создан по тому что сервис memrise, на момент написания приложения, не предоставляет API
для работы с данными курсов. А именно не возможно скачать имеющиеся курсы, слова, уровни 
в удобочитаемом для пользователя виде.
По этому был создан данный проект который позволит скачать все пользовательские данные (слова, курсы, уровни) в 
локальное хранилище и далее конвертировать эти данные в разные форматы CSV, PDF, JSON.

Так же приложение сможет делать поиск по всем словам, что позволит посмотреть наличие какого-то слова в БД или 
же быстро посмотреть значение слов.


## Настройка и запуск

- Обязательная регистрация в [Memrise](https://app.memrise.com/home/)
- Получение параметров cookies:
    - sessionid_2
    - csrftoken
- Скачать репозиторий `git clone ...`
- Перейти в директорию проекта "django-memrise-scraper"
- Создать виртуальное окружение c использованием [pipenv](https://pipenv.pypa.io/en/latest/) 
    ```pipenv --three --python 3.8```
- Установить все зависимости `pipenv install`
- Если запуск планируется из терминала, то создать и экспортировать переменные окружения
    - `export SESSION_ID=значение из cookies.sessionid_2`
    - `export CSRF_TOKEN=значение из cookies.csrftoken`
- Запуск сервиса `python manage.py runserver`



## ENVIRONMENT
- SESSION_ID [STR (required)]: значение из cookies.sessionid_2
- CSRF_TOKEN [STR (required)]: значение из cookies.csrftoken
- STORAGE [STR (optional)]: путь до хранения логов. В случае если не был передан параметр, будет 
установлено значение по умолчанию `django-memrise-scraper/resourses/logs`


## ENDPOINT
 - update/
 
**Пример запроса**

 ```http request
GET http://127.0.0.1:8000/update/
/
Accept: */*
Cache-Control: no-cache
Content-Type: application/json
```
 