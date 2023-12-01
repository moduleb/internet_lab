![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
# UserManagementAPI
>API сервис для управления пользователями

## Содержание
+ [Описание](#description)
+ [Установка и запуск](#install)
+ [API Endpoints:](#api_endpoints)
  + [Register](#register)
  + [Login](#login)
  + [Logout](#logout)
  + [Get info](#get_info)
  + [Update](#update)
  + [Delete](#delete)
+ [Errors](#errors)
+ [Contacts](#contacts)


<a id="description"></a>
## Описание

API Сервис предоставляет возможность регистрации, обновления, удаления и получения информации о пользователях.

Сервис написан на языке `Python` с использование библиотеки `FastAPI`. Аутентификация происходит с помощью `JWT токена`. Деактивированные токены сохраняются в `Redis`. Данные пользователей хранятся в базе данных `MySQL`. API сервис и базы данных запускаются в `Docker` контейнерах с использованием `Docker Compose`.


<a id="install"></a>
## Установка и запуск
>Для запуска сервиса требуется установленный [Docker](https://www.docker.com/get-started/)

1. Клонировать репозиторий с GitHub:

  ```bash
  git clone https://github.com/moduleb/internet_lab.git
  ```
>альтернативный вариант - скачать архив проекта со страницы на [GitHub](https://github.com/moduleb/internet_lab)
2. Перейти в папку с проектом:

  ```bash
  cd internet_lab
  ```
3. Собрать Docker образ:

  ```bash
  docker compose build
  ```
4. Запустить Docker образ:

  ```bash
  docker compose up -d
  ```

5. Для остановки контейнера используйте команду:

  ```bash
  docker compose down
  ```
  
<a id="api_endpoints"></a>
# API Endpoints

 - Address: [0.0.0.0:8000](http://0.0.0.0:8000/users)
 - Документация Swagger [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

<a id="register"></a>
## Register
>Регистрация пользователя

#### Request

`POST /users/register`

```json
{
 "username": "exampleUser",
 "password": "examplePassword",
 "email": "example@example.com"
}
```

#### Response

`200 Successful`

```json
{
 "data": {
   "username": "exampleUser",
   "email": "example@example.com"
 },
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2",
 "token_type": "bearer"
}
```

<a id="update"></a>
## Update
>Обновление информации о пользователе

#### Request
**`PUT /users`**

```json
{
 "password": "examplePassword",
 "email": "example@example.com"
}
```

Требуется наличие токена в заголовке авторизации.

```
Authorization: <Bearer exampleToken>
```

#### Response

`200 Successful`

```json
{
  "data": {
    "username": "exampleUser",
    "email": "example@example.com",
    "registration_date": "2023-12-01T10:03:54"
  }
}
```

<a id="login"></a>
## Login
>Аутентификация пользователя

#### Request

**`POST /users/login`**

```json
{
 "username": "exampleUser",
 "password": "examplePassword"
}
```

#### Response

`200 Successful`

```json
{
   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2",
   "token_type": "bearer"
 }
```
<a id="logout"></a>
## Logout
>Выход из системы

#### Request

`POST /users/logout`

#### Response

`204 No Content`

## Delete
>Удаление пользователя

#### Request

`DELETE /users`

#### Response

`204 No Content`

<a id="get_info"></a>
## Get info
>Получение информации о пользователе

#### Request

`GET /users`

#### Response

`200 Successful`

```json
{
 "username": "exampleUser",
 "email": "example@example.com",
 "registration_date": "2023-12-01T07:34:21"
}
```
<a id="errors"></a>
## Errors

- **401 Unauthorized** - отсутствует или невалидный токен авторизации
- **404 Not Found** - пользователь не найден
- **409 Conflict** - пользователь уже существует
- **422 Unprocessable Entity** - поле содержит недопустимые символы
- **500 Internal Server Error** - внутренняя ошибка сервера

---
<a id="contacts"></a>
## Автор

**Яшин Роман Игоревич**

Контакты: | .
----------:| -----------
GitHub: | [github.com/moduleb](https://github.com/moduleb)
email: | t3841@yandex.ru
phone: | +79024127523
tg: | @popcorn138

