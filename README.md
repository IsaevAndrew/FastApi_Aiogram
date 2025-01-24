# FastAPI + Aiogram Тестовое задание

## Описание проекта
Проект представляет собой API-сервис, разработанный с использованием FastAPI, и Telegram-бот на базе Aiogram. Сервис позволяет получать данные о товарах с Wildberries и управлять подписками на обновление информации о товарах.

### Основные возможности:
- Эндпоинт для получения данных о товаре и сохранения их в базе данных.
- Эндпоинт для подписки на обновления информации о товаре с периодичностью (каждые 30 минут).
- Telegram-бот, позволяющий:
  - Запрашивать информацию о товаре по его артикулу.

## Технологии
- **FastAPI**: Основной веб-фреймворк для реализации API.
- **Aiogram**: Фреймворк для создания Telegram-бота.
- **PostgreSQL**: В качестве базы данных.
- **SQLAlchemy + AsyncPG**: Для работы с базой данных.
- **APScheduler**: Для запуска периодических задач.
- **Docker + Docker Compose**: Для контейнеризации и удобного запуска приложения.

---

## Установка и запуск проекта

### Требования:
1. Docker и Docker Compose установлены на вашем компьютере.
2. Создан файл `.env.prod` с необходимыми переменными окружения.

Пример `.env.prod`:
```
DB_HOST=db
DB_USER=user
DB_PASSWORD=password
DB_NAME=db
DB_PORT=5432
SECRET_TOKEN=TOKEN
TOKEN=7513238570:JLGnn54GGHjNo834ie9fj2qfFNJjgjg3
```

### Запуск проекта:
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/IsaevAndrew/FastApi_Aiogram.git
   cd FastApi_Aiogram
   ```

2. Соберите и запустите проект с помощью Docker Compose:
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file .env.prod up --build
   ```

3. После запуска:
   - API будет доступен по адресу: `http://<IP-адрес>:8000`
   - Документация Swagger доступна по адресу: `http://<IP-адрес>:8000/docs`
   - Telegram-бот будет активен (используйте токен, указанный в `.env.prod`).

---

## Использование

### API
#### 1. **POST /api/v1/products**
**Описание:** Получить информацию о товаре с Wildberries и сохранить её в базу данных.

**Пример запроса:**
```json
{
  "artikul": 211695539
}
```

#### 2. **GET /api/v1/subscribe/{artikul}**
**Описание:** Подписаться на обновления товара. Если товара нет в базе данных, он будет автоматически добавлен.

**Пример:**
```
GET /api/v1/subscribe/211695539
```

#### 3. **Swagger-документация:**
Открыть в браузере: `http://<IP-адрес>:8000/docs`

### Telegram-бот
#### Основные команды:
- **/start**: Начало работы с ботом.
- **Получить данные по товару**: Запросить информацию о товаре по артикулу.

#### Пример работы:
1. Введите команду `/start`.
2. Нажмите кнопку «Получить данные по товару».
3. Введите артикул товара.
4. Бот отправит информацию о товаре (если он есть в базе данных).

---

## Структура проекта
```
FastApi_Aiogram/
├── app/
│   ├── auth.py               # Валидация токена для авторизации
│   ├── db/
│   │   ├── models.py         # Определение моделей базы данных
│   │   ├── session.py        # Настройка подключения к базе данных
│   │   └── init_db.py        # Инициализация базы данных
│   ├── main.py               # Основной файл приложения FastAPI
│   └── scheduler.py          # Планировщик задач (APScheduler)
├── bot/
│   ├── main.py               # Основной файл Telegram-бота
│   ├── consts.py             # Константы для бота
│   ├── keyboards.py          # Клавиатуры для бота
│   └── states.py             # Состояния для FSM бота
├── docker-compose.prod.yml   # Docker Compose для продакшн-среды
├── Dockerfile                # Dockerfile для приложения
├── .env.prod                 # Переменные окружения
└── README.md                 # Описание проекта
```

