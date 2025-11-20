"""
Простой тестовый скрипт для проверки Chat API
Использование: python test_client.py
"""
import asyncio
import websockets
import json
import requests
import time

BASE_URL = "http://localhost:8010"
WS_URL = "ws://localhost:8010"


def create_users():
    """Создать тестовых пользователей"""
    print("Создание пользователей...")
    
    user1 = requests.post(f"{BASE_URL}/users/", json={
        "username": "test_user1",
        "wallet_address": "0x1234567890123456789012345678901234567890"
    }).json()
    print(f"Создан пользователь 1: {user1}")
    
    user2 = requests.post(f"{BASE_URL}/users/", json={
        "username": "test_user2",
        "wallet_address": "0x0987654321098765432109876543210987654321"
    }).json()
    print(f"Создан пользователь 2: {user2}")
    
    return user1, user2


def create_chat(user1_id, user2_id):
    """Создать чат между пользователями"""
    print(f"\nСоздание чата между пользователями {user1_id} и {user2_id}...")
    
    chat = requests.post(f"{BASE_URL}/chats/", json={
        "user1_id": user1_id,
        "user2_id": user2_id
    }).json()
    print(f"Создан чат: {chat}")
    
    return chat


async def test_websocket(chat_id, user_id, messages_to_send):
    """Тестирование WebSocket соединения"""
    uri = f"{WS_URL}/ws/{chat_id}/{user_id}"
    print(f"\nПодключение к WebSocket: {uri}")
    
    async with websockets.connect(uri) as websocket:
        print(f"Подключено! Отправка {len(messages_to_send)} сообщений...")
        
        for i, message in enumerate(messages_to_send, 1):
            # Отправка сообщения
            await websocket.send(json.dumps({
                "type": "message",
                "content": message
            }))
            print(f"Отправлено сообщение {i}: {message}")
            
            # Получение ответа
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                data = json.loads(response)
                print(f"Получен ответ: {data}")
            except asyncio.TimeoutError:
                print("Таймаут при получении ответа")
            
            await asyncio.sleep(0.5)
        
        # Отправка уведомления о наборе текста
        await websocket.send(json.dumps({
            "type": "typing"
        }))
        print("Отправлено уведомление о наборе текста")
        
        await asyncio.sleep(1)
        
        # Отметка сообщений как прочитанных
        await websocket.send(json.dumps({
            "type": "read"
        }))
        print("Отправлена отметка о прочтении")


def get_messages(chat_id):
    """Получить сообщения чата через REST API"""
    print(f"\nПолучение сообщений чата {chat_id}...")
    messages = requests.get(f"{BASE_URL}/chats/{chat_id}/messages").json()
    print(f"Найдено сообщений: {len(messages)}")
    for msg in messages:
        print(f"  - [{msg['created_at']}] User {msg['sender_id']}: {msg['content']}")
    return messages


def main():
    print("=" * 50)
    print("Тестирование Chat API")
    print("=" * 50)
    
    try:
        # Создание пользователей
        user1, user2 = create_users()
        user1_id = user1["id"]
        user2_id = user2["id"]
        
        # Создание чата
        chat = create_chat(user1_id, user2_id)
        chat_id = chat["id"]
        
        # Тестирование WebSocket для первого пользователя
        print("\n" + "=" * 50)
        print("Тест WebSocket - Пользователь 1")
        print("=" * 50)
        asyncio.run(test_websocket(
            chat_id, 
            user1_id, 
            ["Привет!", "Как дела?", "Это тестовое сообщение"]
        ))
        
        time.sleep(1)
        
        # Получение сообщений через REST API
        get_messages(chat_id)
        
        # Получение списка чатов пользователя
        print(f"\nПолучение списка чатов пользователя {user1_id}...")
        chats = requests.get(f"{BASE_URL}/chats/user/{user1_id}").json()
        print(f"Найдено чатов: {len(chats)}")
        for c in chats:
            print(f"  - Чат {c['id']}: с пользователем {c.get('other_user', {}).get('username', 'Unknown')}")
        
        print("\n" + "=" * 50)
        print("Тестирование завершено!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\nОшибка: Не удалось подключиться к серверу.")
        print("Убедитесь, что сервер запущен: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

