# API результатов торгов СПбМТСБ

![](https://img.shields.io/badge/language-python_3.10-blue?logo=python&logoColor=f5f5f5)
![](https://img.shields.io/badge/license-MIT-blue?logo=mit&logoColor=f5f5f5)

Этот проект предоставляет API на базе фреймворка FastAPI для получения и управления результатами торгов на Санкт-Петербургской международной товарно-сырьевой бирже (СПбМТСБ).

## Функции


1. get_last_trading_dates:

limit (обязательный): Количество последних торговых дней. Это обязательный параметр, так как нам нужно знать, сколько дат возвращать. Мы установили значение по умолчанию 10 и ограничили его от 1 до 100, чтобы избежать слишком больших запросов. 

2.get_dynamics: 

oil_id, delivery_type_id, delivery_basis_id (необязательные): Эти параметры позволяют фильтровать результаты, но не являются обязательными, так как пользователь может захотеть получить все данные без фильтрации. 
start_date, end_date (необязательные): Позволяют задать временной диапазон, но также не обязательны, если пользователь хочет получить данные за весь доступный период. 

3. get_trading_results:

oil_id, delivery_type_id, delivery_basis_id (необязательные): Как и в get_dynamics, эти параметры позволяют фильтровать результаты, но не являются обязательными. 
limit (необязательный): Количество возвращаемых результатов. Мы установили значение по умолчанию 10, чтобы ограничить объем данных, но пользователь может изменить это значение при необходимости.

4. check_and_update_data:

start (обязательный): Целое число, представляющее начальную дату для проверки и обновления данных. Это обязательный параметр, так как он определяет нижнюю границу временного диапазона для поиска новых отчетов.
end (обязательный): Целое число, представляющее конечную дату для проверки и обновления данных. Это обязательный параметр, так как он определяет верхнюю границу временного диапазона для поиска новых отчетов.

## Деплой

1. Установите Python 3.10, если он не установлен. [Python.org](https://www.python.org/downloads/)
Создайте и заполните данными файл .env по примеру .env_example

2. Склонируйте репозиторий:
     ```bash
   git clone https://github.com/PavelShaura/spimex-app-fastAPI

3. Сборка Docker-образа. 
Перейдите в корневую директорию проекта:
    ```bash
   cd spimex-app-fastAPI

4. Затем выполните команду: 

    ```bash
   docker-compose build
    
При условии, что у вас уже установлен doker. Инструкция по установке <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru">тут</a> .

5. Запуск контейнера. После успешной сборки Docker-образа запустите контейнер, выполнив команду:
    ```bash
   docker-compose up -d

API будет доступен по адресу `http://localhost:8000`.

## Документация по API

После запуска приложения вы можете получить доступ к документации API по адресу:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- 
<div id="header">
  <img src="https://github.com/PavelShaura/spimex-app-FastAPI/blob/main/screen/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202024-07-02%2016-23-41.png?raw=true" width="100"/>
</div>

## Запланированные задачи

Проект использует Celery Beat для планирования следующих задач:

- Ежедневная очистка кэша (выполняется каждые 24 часа в 14:11)