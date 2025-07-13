## Дипломный проект. Задание 2: API-тесты
<hr>

## Студент: Олег Шатохин

## <h>Когорта: #22</h>
<hr>

## <h>Project: API Stellar Burgers</h>

## <h>Инструкция по запуску:</h>

### <h>1. Установите зависимости:</h>

> pip install -r requirements.txt</h>

### <h>2. Запустить все тесты:</h>

> pytest -v

### <h>3. Посмотреть отчет по прогону html</h>

> allure serve allure_results


<hr>

<h3 align="left" style="color:green">Project files and description:</h3>

| Название файла          | Содержание файла              |
|-------------------------|-------------------------------|
| Tests dir               | Директория с тестами          |
| test_auth_register.py | Тесты регистрации пользователя |
| test_auth_login.py  | Тесты авторизации пользователя |
| conftest.py             | Фикстуры                      |
| helpers.py              | Хэлпер для тела запросов      |
| data.py                 | Файл с URL и body запросов    |
| auth.py         | Методы для работы с авторизацией и регистрацией     |
| order.py      | Методы для работы с заказами |
| generators.py           | Генератор данных              |
| requirements.txt        | Файл с зависимостями          |
| allure_results.dir      | Папка с отчетами Allure       |


