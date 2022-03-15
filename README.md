### Описание проекта:

С помощью данного проекта можно развернуть образ приложения api_yamdb (проект по сбору отзывов о музыкальных произведениях) на сервере sergeev-cloud (подключен к Yandex Cloud).
Принцип подключения следующий: 
1) с помощью настроек файла "yamdb_workflow.yml" происходит подключение к проекту на ресурсе GitHub, с помощью GitHub Actions производится автоматическая проверка кода линтером flake8, запусков тестов, а также сборка docker-образа и деплой проекта. При успешном выполнении всех шагов, на телеграм-бот приходит соответствующее сообщение;
2) сборка docker-образа происходит на основании файлов Dockerfile и docker-compose.yaml, где прописаны соответствующие инструкции. Образ собирается на интернет сервисе DockerHub, создаются 3 контейнера: web, db и nginx;
3) проект запускается из сервиса DockerHub, после успешного запуска всех 3-х контейнеров. 

### Как запустить проект локально:

## Создайте файл _.env_ в директории _infra/_ и внестите в него данные:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD= # установите свой пароль
DB_HOST=db
DB_PORT=5432
```

## Проверьте настройки в _setting.py_, раздел _DATABASES_:

```
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default=None),
        'USER': os.getenv('POSTGRES_USER', default=None),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default=None),
        'HOST': os.getenv('DB_HOST', default=None),
        'PORT': os.getenv('DB_PORT', default=None)
    }
}
```

### Доступные ссылки к приложению:

Основная ссылка http://localhost .
Посмотреть все возможности можно по ссылке http://localhost/redoc/, а именно:
- регистрация пользователей
- получение JWT-токенов
- страница с музыкальными категориями
- страница с музыкальными жанрами
- работа с отзывами
- работа с комментариями к отзывам
- просмотр пользователей


## Статус рабочих процессов:

![example workflow](https://github.com/Vofkabob/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)