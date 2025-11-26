# Systemd сервисы для Devsy Web Server

Этот каталог содержит systemd unit файлы для запуска серверов Devsy в качестве системных сервисов Ubuntu.

## Файлы сервисов

- `devsy-web-server.service` - Основной API сервер (порт 8000)
- `devsy-chat-server.service` - Сервер чата (порт 8010)

## Установка и настройка

### 1. Настройка путей в файлах сервисов

Перед установкой необходимо отредактировать оба файла `.service` и заменить `/path/to/devsy_web_server` на реальный путь к вашему проекту.

Например, если проект находится в `/var/www/devsy_web_server`, выполните:

```bash
sed -i 's|/path/to/devsy_web_server|/var/www/devsy_web_server|g' devsy-web-server.service
sed -i 's|/path/to/devsy_web_server|/var/www/devsy_web_server|g' devsy-chat-server.service
```

Также проверьте и при необходимости измените:
- `User=www-data` - пользователь, от имени которого будет запускаться сервис
- `Group=www-data` - группа пользователя

### 2. Создание виртуального окружения (если еще не создано)

```bash
cd /var/www/devsy_web_server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Установка сервисов

Скопируйте файлы сервисов в директорию systemd:

```bash
sudo cp devsy-web-server.service /etc/systemd/system/
sudo cp devsy-chat-server.service /etc/systemd/system/
```

### 4. Перезагрузка systemd

```bash
sudo systemctl daemon-reload
```

### 5. Включение автозапуска при загрузке системы

```bash
sudo systemctl enable devsy-web-server.service
sudo systemctl enable devsy-chat-server.service
```

## Управление сервисами

### Запуск сервисов

```bash
# Основной сервер
sudo systemctl start devsy-web-server

# Сервер чата
sudo systemctl start devsy-chat-server

# Оба сервиса одновременно
sudo systemctl start devsy-web-server devsy-chat-server
```

### Остановка сервисов

```bash
# Основной сервер
sudo systemctl stop devsy-web-server

# Сервер чата
sudo systemctl stop devsy-chat-server

# Оба сервиса одновременно
sudo systemctl stop devsy-web-server devsy-chat-server
```

### Перезапуск сервисов

```bash
# Основной сервер
sudo systemctl restart devsy-web-server

# Сервер чата
sudo systemctl restart devsy-chat-server

# Оба сервиса одновременно
sudo systemctl restart devsy-web-server devsy-chat-server
```

### Проверка статуса

```bash
# Статус основного сервера
sudo systemctl status devsy-web-server

# Статус сервера чата
sudo systemctl status devsy-chat-server

# Краткий статус обоих
sudo systemctl status devsy-web-server devsy-chat-server
```

### Просмотр логов

```bash
# Логи основного сервера
sudo journalctl -u devsy-web-server -f

# Логи сервера чата
sudo journalctl -u devsy-chat-server -f

# Последние 100 строк логов
sudo journalctl -u devsy-web-server -n 100
sudo journalctl -u devsy-chat-server -n 100
```

### Включение/отключение автозапуска

```bash
# Включить автозапуск
sudo systemctl enable devsy-web-server
sudo systemctl enable devsy-chat-server

# Отключить автозапуск
sudo systemctl disable devsy-web-server
sudo systemctl disable devsy-chat-server

# Проверить, включен ли автозапуск
sudo systemctl is-enabled devsy-web-server
sudo systemctl is-enabled devsy-chat-server
```

## Отладка

### Проверка конфигурации перед запуском

```bash
# Проверить синтаксис файлов сервисов
sudo systemd-analyze verify /etc/systemd/system/devsy-web-server.service
sudo systemd-analyze verify /etc/systemd/system/devsy-chat-server.service
```

### Проверка зависимостей

```bash
# Показать зависимости сервиса
systemctl list-dependencies devsy-web-server
systemctl list-dependencies devsy-chat-server
```

### Ручной запуск для проверки

Если сервис не запускается, попробуйте запустить команду вручную:

```bash
# Для основного сервера
cd /var/www/devsy_web_server
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4

# Для сервера чата
cd /var/www/devsy_web_server/chat-api
../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8010
```

### Проверка прав доступа

Убедитесь, что у пользователя сервиса (обычно `www-data`) есть права на:
- Чтение файлов проекта
- Запись в директории с базами данных и логами
- Доступ к виртуальному окружению

```bash
# Проверить права
ls -la /var/www/devsy_web_server

# Установить правильные права (пример)
sudo chown -R www-data:www-data /var/www/devsy_web_server
sudo chmod -R 755 /var/www/devsy_web_server
```

## Удаление сервисов

Если нужно удалить сервисы:

```bash
# Остановить и отключить
sudo systemctl stop devsy-web-server devsy-chat-server
sudo systemctl disable devsy-web-server devsy-chat-server

# Удалить файлы
sudo rm /etc/systemd/system/devsy-web-server.service
sudo rm /etc/systemd/system/devsy-chat-server.service

# Перезагрузить systemd
sudo systemctl daemon-reload
```

