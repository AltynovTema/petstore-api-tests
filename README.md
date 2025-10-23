# petstore-api-tests

Проект Python/Pytest для автоматизации API тестов сервиса Petstore (Swagger).

## 🤖 **CI/CD:** 

- Интегрирован GitHub Actions. Автоматический запуск тестов `pytest` осуществляется при каждом `push` в репозиторий и при создании `pull request` через workflow файл `.github/workflows/test.yml`.

## 🚀 Возможности

- ✅ Покрывает методы GET, POST, PUT, DELETE с разными параметрами для сущности Pet.
- ✅ Включает фикстуры для подготовки и очистки данных.
- ✅ Проверяет статусы ответов и содержимое данных.

## 🛠 Стек 

1. **Python 3.x**
2. **pytest**
3. **requests**

## 📋 Тест кейсы

* **Pet API:** Покрывает следующие эндпоинты:
    * `POST /pet`: Создание нового питомца (через фикстуру).
    * `GET /pet/{petId}`: Получение данных питомца по ID.
    * `PUT /pet`: Обновление данных питомца (в формате JSON).
    * `POST /pet/{petId}`: Обновление данных питомца (в формате form data).
    * `GET /pet/findByStatus`: Поиск питомцев по статусу.
    * `DELETE /pet/{petId}`: Удаление питомца.

## 📆 Планы

* Добавить тесты для User API и Store API. 

## 📥 Установка

1.  Убедитесь, что у вас установлен Python 3.x.
2.  Рекомендуется использовать виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows: venv\Scripts\activate
    ```
3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Запуск тестов

```bash
# Запуск mock сервера (терминал 1)
python tests/mocks/mock_server.py

# Запуск Playwright тестов (терминал 2)
python tests/test_qiwi_playwright.py

# Или через главный скрипт
python main.py
```

## 📁 Структура проекта

```
petstore-api-tests/
│
├── README.md
├── requirements.txt
├── tests/
│   └── test_pet_api.py
│   └── test_store_api.py
│   └── test_user_api.py
└── .github/
    └── workflows/
        └── test.yml
```

## 📞 Поддержка

Если возникли вопросы - создайте issue в репозитории.
