# Chat API

Chat API проект с использованием FastAPI, SQLite и WebSocket для реализации чата в реальном времени.

## Возможности

- ✅ REST API для управления чатами и сообщениями
- ✅ WebSocket для обмена сообщениями в реальном времени
- ✅ SQLite база данных
- ✅ Поддержка нескольких чатов между пользователями
- ✅ Отметка сообщений как прочитанных
- ✅ Уведомления о наборе текста (typing indicators)
- ✅ Автоматическое создание таблиц в БД

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу: http://localhost:8000

Документация API: http://localhost:8000/docs

## Структура проекта

```
chat-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа приложения
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py          # Роутер для чата (REST + WebSocket)
│   │   ├── users.py         # Роутер для пользователей
│   │   └── deps.py          # Зависимости (DB сессии)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Конфигурация приложения
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── chat.py          # CRUD операции для чата
│   │   └── user.py          # CRUD операции для пользователей
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # Базовый класс для моделей
│   │   └── session.py       # Настройка сессии БД
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py          # Модели Chat и Message
│   │   └── user.py          # Модель User
│   └── schemas/
│       ├── __init__.py
│       ├── chat.py          # Pydantic схемы для чата
│       └── user.py          # Pydantic схемы для пользователей
├── requirements.txt
└── README.md
```

## API Endpoints

### Пользователи

- `POST /users/` - Создать пользователя
- `GET /users/{user_id}` - Получить пользователя по ID
- `GET /users/` - Получить всех пользователей

### Чаты

- `POST /chats/` - Создать чат между двумя пользователями
- `GET /chats/{chat_id}` - Получить чат по ID
- `GET /chats/user/{user_id}` - Получить все чаты пользователя
- `GET /chats/{chat_id}/messages` - Получить сообщения чата
- `POST /chats/{chat_id}/read` - Отметить сообщения как прочитанные

### WebSocket

- `WS /ws/{chat_id}/{user_id}` - WebSocket соединение для чата

## Использование WebSocket

### Подключение

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/1/1');
// где 1 - chat_id, второй 1 - user_id
```

### Отправка сообщения

```javascript
ws.send(JSON.stringify({
    type: "message",
    content: "Привет! Как дела?"
}));
```

### Отправка уведомления о наборе текста

```javascript
ws.send(JSON.stringify({
    type: "typing"
}));
```

### Отметка сообщений как прочитанных

```javascript
ws.send(JSON.stringify({
    type: "read"
}));
```

### Получение сообщений

```javascript
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === "message") {
        console.log("Новое сообщение:", data.content);
    } else if (data.type === "typing") {
        console.log("Пользователь печатает...");
    } else if (data.type === "read") {
        console.log("Сообщения прочитаны");
    }
};
```

## Пример использования

### 1. Создать пользователей

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com"}'

curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "user2", "email": "user2@example.com"}'
```

### 2. Создать чат

```bash
curl -X POST "http://localhost:8000/chats/" \
  -H "Content-Type: application/json" \
  -d '{"user1_id": 1, "user2_id": 2}'
```

### 3. Подключиться через WebSocket

Используйте любой WebSocket клиент или JavaScript:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/1/1');

ws.onopen = () => {
    console.log('Connected');
    ws.send(JSON.stringify({
        type: "message",
        content: "Привет!"
    }));
};

ws.onmessage = (event) => {
    console.log('Message:', JSON.parse(event.data));
};
```

## База данных

По умолчанию используется SQLite база данных `chat.db` в корне проекта. 

Чтобы изменить настройки БД, создайте файл `.env`:

```
DATABASE_URL=sqlite:///./chat.db
```

## Лицензия

MIT

