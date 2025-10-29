import pytest # В pytest имена тестов должны начинаться с test_, чтобы pytest мог их автоматически найти и запустить.
import requests # Библиотека requests делает всю работу с JSON за нас.

BASE_URL = "https://petstore.swagger.io/v2" # Это официальный Base URL, указанный в самой документации API Petstore на https://petstore.swagger.io

@pytest.fixture # Вместо того чтобы создавать пользователя в каждом тесте, мы создаём фикстуру. Фикстура выполнит код один раз перед каждым тестом, который её использует, и очистит за собой после теста.
def created_user(): # Код внутри этой функции created_user будет выполнен, когда pytest вызовет фикстуру @pytest.fixture, и передаст результат тесту yield username.
    user_data = {
          "id": 460175840, # Создаем уникальный ID пользователя для теста (аналогично pet_id). ВНИМАНИЕ: может привести к конфликту на тестовом сервере.
          "username": "test_user_for_api_test", # Используем фиксированное имя пользователя для теста.
          "firstName": "Test",
          "lastName": "User",
          "email": "test_user_for_api_test@example.com", # Используем имя для email
          "password": "password123",
          "phone": "1234567890",
          "userStatus": 0  # 0 - default user status
        }
    response = requests.post(f"{BASE_URL}/user", json=user_data) # Создаём пользователя и сохраняем в переменную response - этот объект содержит всё, что вернул сервер: статус-код, заголовки, тело ответа. Предварительно requests.post(f"{BASE_URL}/user", json=user_data): отправляет HTTP-запрос методом POST. И json=user_data - этот именованный аргумент keyword argument говорит requests: "Возьми Python-словарь user_data, преобразуй его в JSON-строку и отправь как тело запроса. Также установи заголовок Content-Type: application/json.
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем сообщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    # ВАЖНО: Мы вручную извлекаем имя пользователя из данных, которые мы отправили, так как оно используется как ID для других операций (GET, PUT, DELETE)
    # (Сервер не возвращает username в ответе на POST /user)
    yield "test_user_for_api_test" # Когда интерпретатор доходит до строки yield "test_user_for_api_test", выполнение останавливается. И yield передаёт username в тест.
    requests.delete(f"{BASE_URL}/user/test_user_for_api_test") # Код очистки выполняется после завершения функции теста (с.м. yield).

# Выполняем ПЕРВЫЙ ТЕСТ для User API - GET (Проверяем, можно ли получить информацию о конкретном пользователе по его имени.)
def test_get_user_by_username(created_user): # Определяем функцию теста. Важно: имя функции начинается с test_ — это соглашение pytest, чтобы находить тесты автоматически. created_user — это имя фикстуры. pytest автоматически вызовет фикстуру и передаст возвращаемое ею значение (username) в этот параметр.
    """Тестирует GET /user/{username} - получение пользователя по имени.""" # Это документация к функции (docstring). Хорошая практика — кратко описывать, что делает тест.
    username = created_user # Получаем имя пользователя, созданного фикстурой.
    response = requests.get(f"{BASE_URL}/user/{username}") # Отправляем GET запрос к эндпоинту /user/{username}.
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем сообщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    assert response.json()["username"] == username # Проверяем, что сервер вернул имя пользователя в теле ответа совпадающее с username, который мы установили в фикстуре. Это подтверждает, что мы получили именно того пользователя, которого создали.