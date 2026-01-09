import asyncio
import json
import websockets
import requests

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws"

USER1_ID = 1
USER2_ID = 2

def test_rest():
    print("=== REST API TEST ===")

    # 1. Создать чат
    chat_data = {"user1_id": USER1_ID, "user2_id": USER2_ID}
    res = requests.post(f"{BASE_URL}/chats/", json=chat_data)
    chat = res.json()
    chat_id = chat["id"]
    print("Chat created:", chat)

    # 2. Получить список чатов пользователя
    res = requests.get(f"{BASE_URL}/chats/user/{USER1_ID}")
    print("User chats:", res.json())

    # 3. Получить сообщения (пусто)
    res = requests.get(f"{BASE_URL}/chats/{chat_id}/messages")
    print("Messages:", res.json())

    return chat_id

# ---------------- WEBSOCKET TEST ----------------
async def test_ws(chat_id):
    print("\n=== WEBSOCKET TEST ===")

    async with websockets.connect(f"{WS_URL}/{chat_id}/{USER1_ID}") as ws1, \
               websockets.connect(f"{WS_URL}/{chat_id}/{USER2_ID}") as ws2:

        # User1 отправляет сообщение
        await ws1.send(json.dumps({"type": "text", "content": "Hello User2!"}))

        # User2 получает сообщение
        msg = await ws2.recv()
        print("User2 received:", msg)

        # User2 отправляет typing
        await ws2.send(json.dumps({"type": "typing"}))
        event = await ws1.recv()
        print("User1 received typing:", event)

        # User2 пометил сообщение как прочитанное
        await ws2.send(json.dumps({"type": "read"}))
        event = await ws1.recv()
        print("User1 received read:", event)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    chat_id = test_rest()
    asyncio.run(test_ws(chat_id))
