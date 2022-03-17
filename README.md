### Проект Yandb_final

![example workflow](https://github.com/Vofkabob/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Описание проекта:

С помощью данного проекта можно развернуть образ приложения api_yamdb (проект по сбору отзывов о музыкальных произведениях) на своём сервере.
Принцип подключения следующий: 
1) с помощью настроек файла "yamdb_workflow.yml" происходит подключение к проекту на ресурсе GitHub, с помощью GitHub Actions производится автоматическая проверка кода линтером flake8, запусков тестов, а также сборка docker-образа и деплой проекта. При успешном выполнении всех шагов, на телеграм-бот приходит соответствующее сообщение;
2) сборка docker-образа происходит на основании файлов Dockerfile и docker-compose.yaml, где прописаны соответствующие инструкции. Образ собирается на интернет сервисе DockerHub, создаются 3 контейнера: web, db и nginx;
3) проект запускается из сервиса DockerHub, после успешного запуска всех 3-х контейнеров. 

Проект доступен по ссылке - http://localhost/redoc/

## Подготовка и запуск проекта:

Клонироваnm репозиторий:

```
git clone https://github.com/Vofkabob/yamdb_final.git
```

Запустить docker-compose:

```
docker-compose up -d --build
```

Выполнить миграции, создать суперпользователя, собрать статику.

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

Создать файл .env из директории infra/ и внестите в него данные:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD= # установите свой пароль
DB_HOST=db
DB_PORT=5432
```



## Страницы проекта:

Посмотреть все возможности можно по ссылке http://localhost/redoc/, а именно:
- регистрация пользователей
- получение JWT-токенов
- страница с музыкальными категориями
- страница с музыкальными жанрами
- работа с отзывами
- работа с комментариями к отзывам
- просмотр пользователей

## Автор:

Сергеев Владимир - https://github.com/Vofkabob
