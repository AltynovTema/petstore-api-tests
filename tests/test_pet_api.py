import pytest # В pytest имена тестов должны начинаться с test_, чтобы pytest мог их автоматически найти и запустить.
import requests # Библиотека requests делает всю работу с JSON за нас.

BASE_URL = "https://petstore.swagger.io/v2" # Это официальный Base URL, указанный в самой документации API Petstore на https://petstore.swagger.io

@pytest.fixture # Вместо того чтобы создавать питомца в каждом тесте, мы создаём фикстуру. Фикстура выполнит код один раз перед каждым тестом, который её использует, и очистит за собой после теста.
def created_pet(): # Код внутри этой функции created_pet будет выполнен, когда pytest вызовет фикстуру @pytest.fixture, и передаст результат тесту yield pet_id. ВНИМАНИЕ: может привести к конфликту на тестовом сервере.
    pet_data = {
          "id": 460175839, # Создаем уникальный ID питомца для теста.
          "category": {
            "id": 2,
            "name": "cats"
          }, # Значения (как id: 2 для категории «cats») мы выбираем произвольно, так как API не требует строгого соответствия внешнему справочнику (как в случае со status).
          "name": "Fluffy", # Добавляем рандомайзер к имени петомца
          "photoUrls": [
            "®http://example.com/fluffy.jpg"
          ],
          "tags": [
            {
              "id": 1,
              "name": "test"
            }
          ],
          "status": "available"
        }
    response = requests.post(f"{BASE_URL}/pet", json=pet_data) # Создаём питомца и сохраняем в переменную response - этот объект содержит всё, что вернул сервер: статус-код, заголовки, тело ответа. Предварительно requests.post(f"{BASE_URL}/pet", json=pet_data): отправляет HTTP-запрос методом POST. И json=pet_data - этот именованный аргумент keyword argument говорит requests: "Возьми Python-словарь pet_data, преобразуй его в JSON-строку и отправь как тело запроса. Также установи заголовок Content-Type: application/json.
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    pet_id = response.json()["id"] # Извлекаем ID созданного питомца из ответа для yield.
    yield pet_id # Когда интерпретатор доходит до строки yield pet_id, выполнение останавливается. И yield передаёт pet_id в тест.
    requests.delete(f"{BASE_URL}/pet/{pet_id}") # Код после yield выполняется ПОСЛЕ теста - очистка

# Выполняем ПЕРВЫЙ ТЕСТ - GET (Проверяем, можно ли получить информацию о конкретном питомце по его ID.)
def test_get_pet_by_id(created_pet): # Определяем функцию теста. Важно: имя функции начинается с test_ — это соглашение pytest, чтобы находить тесты автоматически. created_pet — это имя фикстуры. pytest автоматически вызовет фикстуру и передаст возвращаемое ею значение (pet_id) в этот параметр.
    """Тестирует GET /pet/{petId} - получение питомца по ID.""" # Это документация к функции (docstring). Хорошая практика — кратко описывать, что делает тест.
    pet_id = created_pet # Получаем ID петомца, созданного фикстурой.
    response = requests.get(f"{BASE_URL}/pet/{pet_id}") # Отправляем GET запрос к эндпоинту /pet/{pet_id}.
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    assert response.json()["id"] == pet_id # Проверяем, что сервер вернул ID питомца в теле ответа совпадающий с pet_id, который мы установили в фикстуре. Это подтверждает, что мы получили именно того питомца, которого создали.

# Выполняем ВТОРОЙ ТЕСТ - PUT (Проверяем, можно ли изменить информацию о существующем питомце.)
def test_update_pet(created_pet):
    """Тестирует PUT /pet - обновление данных питомца."""
    pet_id = created_pet
    # Подготовим обновлённые данные.
    updated_pet_data = {
          "id": pet_id, # Обязательно указываем ID питомца, которого обновляем.
          "category": {
            "id": 2,
            "name": "cats"
          }, # Значения id: 2 для категории «cats» оставляем без изменений.
          "name": "Fluffy_Updated", # Изменяем имя.
          "photoUrls": [
            "http://example.com/fluffy_updated.jpg" # Изменяем фото.
          ],
          "tags": [
            {
              "id": 1,
              "name": "test"
            },
            {
                "id": 2,
                "name": "updated" # Добавляем новый тег.
            }
          ],
          "status": "sold" # Изменяем статус.
        }
    response = requests.put(f"{BASE_URL}/pet", json=updated_pet_data) # Отправляем PUT запрос с обнавленными данными.
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    assert response.json()["name"] == "Fluffy_Updated" # Проверяем, что имя на бэке изменилось.

# Выполняем ТРЕТИЙ ТЕСТ - FIND BY STATUS (Проверяем, можно ли найти питомцев с определённым статусом (меняем query parameters).)
def test_find_pets_by_status(): # Тест Без Параметра created_pet. Он не зависит от конкретного питомца, созданного в фикстуре, а ищет питомцев по статусу.
    """Тестирует GET /pet/findByStatus - поиск питомцев по статусу."""
    status = "avaible" # Укажем искомый статус в переменной status.
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})
    # Проверяем, что сервер присылает корректный ответ 200, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
    pets = response.json() # Получаем список питомцев из ответа.
    # print(pets) # Что бы посмотреть список (раскоментить если нужно).
    assert isinstance(pets, list) # Проверяем является ли ответ списком.
    # Проверяем, что в нашем списке есть хотя бы одно животное со статусом avaible.
    if pets:
        # Важно: Если сервер нашёл питомцев со статусом available, он вернёт 200 и список с этими питомцами.
        # НО Если сервер не нашёл питомцев со статусом available, он всё равно должен вернуть 200, но с пустым списком [], по этому код assert pets[0]["status"] == status приведет к ошибке IndexError.
        # ПО ЭТОМУ Если список пуст мы защищаем тест через if [] -> False, и наш код assert pets[0]["status"] == status не выполняется, и ошибка IndexError не возникает.
        assert pets[0]["status"] == status # Проверяем, что чтатус первого питомца в списке avaible.

# Выполняем ЧЕТВЕРТЫЙ ТЕСТ - DELETE (Проверяем, что питомец удален. ВНИМАНИЕ, фикстура уже удаляет питомца после теста, но мы можем протестировать этот вызов DELETE и проверить его результат.)
def test_delete_pet(created_pet): #
    """Тестирует DELETE /pet/{petId} - удаление питомца."""
    pet_id = created_pet
    response = requests.delete(f"{BASE_URL}/pet/{pet_id}") # Отправляем Delete запрос.
    assert response.status_code in [200, 204], f"Expected 200 or 204 for DELETE, got {response.status_code}. Response: {response.text}" # 200 или 204 - статус-коды при успешном удалении, а так же пишем ссобщение которое уведомит если тест упал.
    # Проверяем что в ответ на GET запрос по удаленному питомцу мы получим статус-код 404.
    get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    # Проверяем, что сервер присылает корректный ответ 404, а так же пишем ссобщение которое уведомит если тест упал.
    assert get_response.status_code == 404, f"Expected 404 status code after DELETE, got {response.status_code}. Response: {response.text}"

# Выполняем ПЯТЫЙ ТЕСТ - invalid_id (Проверяем, как API реагирует на запрос несуществующего ID.)
def test_get_pet_not_found(): #
    """Тестирует GET /pet/{petId} для несуществующего ID."""
    invalid_pet_id = 9999999999 # Используем в запросе заведомо несуществующий ID.
    response = requests.get(f"{BASE_URL}/pet/{invalid_pet_id}")
    # Проверяем, что сервер присылает корректный ответ 404, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 404, f"Expected 404 status code, got {response.status_code}. Response: {response.text}"

# Выполняем ШЕСТОЙ ТЕСТ - updete_from_data (Проверяем, как API обновляет питомца через другой формат данных (раньше - json/ сейчас - from_data). Да, это функциональность дублирующая PUT /pet, но ЭТО ОТДЕЛЬНЫЙ ЭНДПОЙНТ с собственной логикой на сервере.)
def test_updete_pet_with_from_data(created_pet):
    """Тестирует POST /pet/{petId} - тест на обновление через form data."""
    pet_id = created_pet
    # Подготавливаем новые данные в формате from data (как строки). Согласно Swagger UI, принимаются только
    from_data = {
        "name": "Fluffy_FormUpdated", # Обновляем имя.
        "status": "pending" # Обновляем статус.
        # category, photoUrls, tags не передаются через этот эндпоинт.
    }
    # Отправляем POST запрос к /pet/{pet_id} с form data
    response = requests.post(f"{BASE_URL}/pet/{pet_id}", data=from_data) # Отправляем POST запрос к /pet/{pet_id} с form data
    # Проверяем, что статус-код 200 при успешном обновлении, а так же пишем ссобщение которое уведомит если тест упал.
    assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Rеsponse: {response.text}"
    # Через GET /pet/{pet_id} проверяем, что данные были успешно обновлены.
    get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    # Проверяем, что статус-код 200 при успешном обновлении, а так же пишем ссобщение которое уведомит если тест упал.
    assert get_response.status_code == 200, f"Expected 200 status code, got {get_response.status_code}. Response: {get_response.text}"
    # Проверяем, что данные были успешно обновлены.
    updated_pet_data = get_response.json()
    assert updated_pet_data["name"] == "Fluffy_FormUpdated"
    assert updated_pet_data["status"] == "pending"