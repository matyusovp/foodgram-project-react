#  Foodgram - продуктовый помощник
![workflow](https://github.com/matyusovp/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание проекта
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Сервис позволяет пользователям просматривать рецепты любимых блюд, а также публиковать собственные. При регистрации пользователь указывает свой email, который будет использоваться при авторизации.

Зарегестрированные пользователи могут подписываться на авторов рецептов или добавлять рецепты в корзину, в избранное. Есть возможность фильтрации рецептов по тегам, поиск по началу названия ингредиента при добавлении или редактировании рецепта.


## Описание Workflow
##### Workflow состоит из четырёх шагов:
###### tests
- Проверка кода на соответствие PEP8.
###### Push Docker image to Docker Hub
- Сборка и публикация образа на DockerHub.
###### deploy 
- Автоматический деплой на боевой сервер при пуше в главную ветку.
###### send_massage
- Отправка уведомления в телеграм-чат.

## Подготовка и запуск проекта
##### Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone git@github.com:matyusovp/foodgram-project-react.git
```

## Установка на удаленном сервере (Ubuntu):
##### Шаг 1. Выполните вход на свой удаленный сервер
Прежде, чем приступать к работе, необходимо выполнить вход на свой удаленный сервер:
```bash
ssh <USERNAME>@<IP_ADDRESS>
```

##### Шаг 2. Установите docker на сервер:
Введите команду:
```bash
sudo apt install docker.io 
```

##### Шаг 3. Установите docker-compose на сервер:
Введите команды:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### Шаг 4. Локально отредактируйте файл nginx.conf
Локально отредактируйте файл `infra/nginx.conf` и в строке `server_name` впишите свой IP.

##### Шаг 5. Скопируйте подготовленные файлы из каталога infra:
Скопируйте подготовленные файлы `infra/docker-compose.yml` и `infra/nginx.conf` из вашего проекта на сервер в `home/<ваш_username>/docker-compose.yml` и `home/<ваш_username>/nginx.conf` соответственно.
Введите команду из корневой папки проекта:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

##### Шаг 6. Cоздайте .env файл:
На сервере создайте файл `nano .env` и заполните переменные окружения (или создайте этот файл локально и скопируйте файл по аналогии с предыдущим шагом):
```bash
SECRET_KEY=<SECRET_KEY>
DEBUG=<True/False>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

##### Шаг 7. Добавьте Secrets:
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

##### Шаг 8. После успешного деплоя:
Зайдите на боевой сервер и выполните команды:

###### На сервере соберите docker-compose:
```bash
sudo docker-compose up -d --build
```

###### Создаем и применяем миграции:
```bash
sudo docker-compose exec backend python manage.py makemigrations --noinput
sudo docker-compose exec backend python manage.py migrate --noinput
```
###### Подгружаем статику
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput 
```
###### Заполнить базу данных:
```bash
sudo docker-compose exec backend python manage.py loaddata ../data/ingredients.json
```
###### Создать суперпользователя Django:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

##### Шаг 9. Проект запущен:
Проект будет доступен по вашему IP-адресу.


##  Запуск проекта локально
##### Склонировать проект и перейти в папку проекта
git clone git clone git@github.com:matyusovp/foodgram-project-react.git
cd foodgram-project-react
##### Установить Python 3.8.3 в случае если он не установлен
##### Установить и активировать виртуальное окружение, или создать новый проект в PyCharm
python3 -m venv venv
source venv\bin\activate
##### Установить зависимости из файла requirements.txt
pip install -r requirements.txt
##### В папке с файлом manage.py выполнить команды:
python manage.py makemigrations
python manage.py migrate
##### Создать пользователя с неограниченными правами:
python manage.py createsuperuser
##### Запустить web-сервер на локальной машине:
python manage.py runserver --settings=foodgram.settings-dev


Автор - Матюсов Павел tg - bizewka
