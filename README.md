# [![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=000000&random=false&width=600&height=70&lines=MediOn+-+%D0%A2%D0%B2%D0%BE%D0%B9+%D0%9E%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD+%D0%A2%D0%B5%D1%80%D0%B0%D0%BF%D0%B5%D0%B2%D1%82)](https://git.io/typing-svg)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


### 1. Разработка Telegram бота [@medionlinebot](https://t.me/medionlinebot "MediON")

#### 1.1 Функции бота:
- **Принятие данных от пользователя**: бот должен запросить у пользователя симптомы и подтвержденный диагноз, затем сохранить эти данные в формате JSON.
- **Получение предварительных диагнозов**: пользователь отправляет список симптомов, бот обрабатывает запрос через внешний API вашего сервера, который возвращает предварительный диагноз.

### 2. Backend с использованием Python и FastAPI
Backend будет включать в себя следующие компоненты:

#### 2.1 FastAPI приложение
- **API для получения данных от бота** и отправки их в базу данных.
- **API для обработки запросов на диагностику**, которое будет взаимодействовать с моделью машинного обучения.

#### 2.2 PostgreSQL
- Настройка базы данных для хранения пар "набор симптомов - диагноз".
- Использование SQLAlchemy для взаимодействия с базой данных из Python.

#### 2.3 Нейросеть
- Разработка и обучение нейросети на начальном наборе данных.
- Поддержка возможности дообучения нейросети на новых данных, полученных от пользователей.

### 3. Интеграция и тестирование
- Интеграция всех компонентов вместе.
- Тестирование системы в целом для убеждения в ее надежности и точности.

### 4. Развертывание
- Развертывание бэкенда на сервере (можно использовать облачные решения как Heroku, AWS и т.д.).
- Подключение бота к бэкенду через созданные API.

### Примерные технические решения:
1. **Python библиотеки**: `python-telegram-bot` для бота, `FastAPI` для API, `SQLAlchemy` для работы с базой данных, `PyTorch` или `TensorFlow` для работы с нейросетью.
2. **Токен бота**: Получение токена через BotFather в Telegram.
3. **База данных**: Настройка PostgreSQL на сервере или в облачном сервисе.
4. **API**: Создание эндпоинтов для приема данных от бота и для отправки запросов на диагностику.
